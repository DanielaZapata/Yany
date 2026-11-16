"""Adaptador web de YANY."""
import json, os, re
from datetime import datetime
from functools import wraps
from flask import Flask, jsonify, request, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash

from estructuras.lista import Lista
from estructuras.cola import Cola
from estructuras.pila import Pila
from estructuras.arbol import Arbol
from yany.pasajera import Pasajera
from yany.pasajeraPremium import PasajeraPremium
from yany.conductora import Conductora
from yany.vehiculo import Vehiculo
from yany.viaje import Viaje
from yany.ViajeConAcompanante import ViajeConAcompanante

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, 'datos')
DATA_FILE = os.path.join(DATA_DIR, 'yany_web.json')
os.makedirs(DATA_DIR, exist_ok=True)
app = Flask(__name__)
app.config.update(SECRET_KEY=os.environ.get('YANY_SECRET_KEY', 'yany-clave-local-cambiar-en-produccion'), SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')

# Se utilizan las estructuras implementadas por el equipo.
lista_pasajeras, lista_conductoras, lista_viajes = Lista(), Lista(), Lista()
cola_solicitudes, cola_alertas, pila_historial, arbol_zonas = Cola(), Cola(), Pila(), Arbol()
usuarios, viajes_data = [], []
objetos_pasajeras, objetos_conductoras = {}, {}

def cargar_datos():
    global usuarios, viajes_data
    if not os.path.exists(DATA_FILE): return
    try:
        with open(DATA_FILE, encoding='utf-8') as f: data = json.load(f)
    except (OSError, json.JSONDecodeError): return
    usuarios = data.get('usuarios', [])
    for p in data.get('pasajeras', []):
        obj = PasajeraPremium(p['id'],p['nombre'],p['telefono'],p.get('contacto_emergencia','Contacto pendiente')) if p.get('premium') else Pasajera(p['id'],p['nombre'],p['telefono'],p.get('contacto_emergencia','Contacto pendiente'))
        objetos_pasajeras[p['id']] = obj; lista_pasajeras.agregar(obj)
    for d in data.get('conductoras', []):
        vdata=d.get('vehiculo') or {}; veh=Vehiculo(vdata.get('placa','PENDIENTE'),vdata.get('color','No registrado'),int(vdata.get('anio',2020)))
        obj=Conductora(d['id'],d['nombre'],d['telefono'],bool(d.get('certificada',True)),bool(d.get('disponible',True)),veh)
        objetos_conductoras[d['id']]=obj; lista_conductoras.agregar(obj)
    viajes_data=data.get('viajes', [])
    for t in viajes_data:
        p=objetos_pasajeras.get(t.get('pasajera_id'))
        if not p: continue
        c=objetos_conductoras.get(t.get('conductora_id'))
        obj=ViajeConAcompanante(t['id'],p,c,t['origen'],t['destino'],int(t.get('acompanante',{}).get('cantidad',0)),False,t.get('estado','Solicitado'))
        lista_viajes.agregar(obj)
        if obj.estado == 'Finalizado': pila_historial.agregar_pila(obj)
        elif obj.estado == 'Pendiente': cola_solicitudes.agregar_cola(obj)

def guardar_datos():
    data={'usuarios':usuarios,'pasajeras':[],'conductoras':[],'viajes':viajes_data}
    for u in usuarios:
        if u['rol']=='pasajera':
            data['pasajeras'].append({'id':u['perfil_id'],'nombre':u['nombre'],'telefono':u['telefono'],'contacto_emergencia':u.get('contacto_emergencia','Contacto pendiente'),'premium':u.get('premium',False)})
        else:
            data['conductoras'].append({'id':u['perfil_id'],'nombre':u['nombre'],'telefono':u['telefono'],'certificada':True,'disponible':True,'vehiculo':u.get('vehiculo',{})})
    tmp=DATA_FILE+'.tmp'
    with open(tmp,'w',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=2)
    os.replace(tmp,DATA_FILE)

def actual_user():
    uid=session.get('uid')
    return next((u for u in usuarios if u['id']==uid),None)
def public_user(u):
    return {k:u.get(k) for k in ('id','nombre','correo','telefono','contacto_emergencia','rol','tipo_cuenta','vehiculo')}
def login_required(fn):
    @wraps(fn)
    def wrapper(*a,**kw):
        if not actual_user(): return jsonify(error='Inicia sesión para continuar.'),401
        return fn(*a,**kw)
    return wrapper

def tarifa(distancia, usuario, acomp=0):
    base=4500+max(0,float(distancia))*1900
    premium=bool(usuario.get('premium'))
    pct=5 if premium else 2
    descuento=base*pct/100
    recargo=max(0,int(acomp))*2000
    total=round(base-descuento+recargo)
    return {'base':round(base),'descuento':round(descuento),'descuento_porcentaje':pct,'recargo_acompanante':recargo,'total_estimado':total,'nota':'Tarifa aproximada; puede variar según el recorrido y las condiciones del servicio.'}

def viaje_json(t):
    tarifa_data=t.get('tarifa') or {}
    return {'id':t['id'],'origen':t['origen'],'destino':t['destino'],'estado':t['estado'],'fecha_solicitud':t.get('fecha_solicitud'),'pasajera_id':t.get('pasajera_id'),'conductora_id':t.get('conductora_id'),'distancia_km':t.get('distancia_km',0),'pasajeras':t.get('pasajeras',1),'tipo_servicio':t.get('tipo_servicio','Viaje'),'tarifa':tarifa_data,'acompanante':t.get('acompanante',{})}

@app.get('/')
def home(): return send_from_directory(BASE, 'index.html')

@app.get('/img/<path:filename>')
def imagenes(filename): return send_from_directory(os.path.join(BASE, 'img'), filename)

@app.post('/api/auth/registro')
def registro():
    d=request.get_json(silent=True) or {}; nombre=str(d.get('nombre','')).strip(); telefono=str(d.get('telefono','')).strip(); correo=str(d.get('correo','')).strip().lower(); password=str(d.get('contrasena','')); rol=d.get('rol','pasajera')
    if not nombre or not telefono or not correo or not password: return jsonify(error='Completa todos los campos obligatorios.'),400
    if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+',correo): return jsonify(error='Escribe un correo electrónico válido.'),400
    if len(password)<8: return jsonify(error='La contraseña debe tener al menos 8 caracteres.'),400
    if rol not in ('pasajera','conductora'): return jsonify(error='Selecciona un tipo de cuenta válido.'),400
    if any(u['correo']==correo for u in usuarios): return jsonify(error='Ya existe una cuenta con ese correo.'),409
    pid=max([u.get('perfil_id',0) for u in usuarios] or [0])+1; uid=max([u.get('id',0) for u in usuarios] or [0])+1
    u={'id':uid,'perfil_id':pid,'nombre':nombre,'telefono':telefono,'correo':correo,'password_hash':generate_password_hash(password),'rol':rol}
    if rol=='pasajera':
        u['contacto_emergencia']=str(d.get('contacto_emergencia','')).strip()
        if not u['contacto_emergencia']: return jsonify(error='Ingresa tu contacto de emergencia.'),400
        u['premium']=str(d.get('premium','false')).lower()=='true'; u['tipo_cuenta']='Pasajera premium' if u['premium'] else 'Pasajera normal'
        obj=PasajeraPremium(pid,nombre,telefono,u['contacto_emergencia']) if u['premium'] else Pasajera(pid,nombre,telefono,u['contacto_emergencia'])
        objetos_pasajeras[pid]=obj; lista_pasajeras.agregar(obj)
    else:
        placa=str(d.get('placa','')).strip(); marca=str(d.get('marca','')).strip(); modelo=str(d.get('modelo','')).strip(); capacidad=int(d.get('capacidad') or 4)
        if not placa or not marca or not modelo: return jsonify(error='Completa los datos del vehículo.'),400
        u['vehiculo']={'placa':placa,'marca':marca,'modelo':modelo,'capacidad':capacidad}; u['tipo_cuenta']='Conductora'
        veh=Vehiculo(placa,marca,2020); obj=Conductora(pid,nombre,telefono,True,True,veh); objetos_conductoras[pid]=obj; lista_conductoras.agregar(obj)
    usuarios.append(u); guardar_datos(); session['uid']=uid
    return jsonify(ok=True,usuario=public_user(u)),201

@app.post('/api/auth/login')
def login():
    d=request.get_json(silent=True) or {}; correo=str(d.get('correo','')).strip().lower(); password=str(d.get('contrasena',''))
    # Si hay registros antiguos con el mismo correo en roles distintos,
    # identifica la cuenta usando también la contraseña.
    u=next((x for x in usuarios if x['correo']==correo and check_password_hash(x['password_hash'],password)),None)
    if not u: return jsonify(error='Correo o contraseña incorrectos.'),401
    session['uid']=u['id']; return jsonify(ok=True,usuario=public_user(u))
@app.post('/api/auth/logout')
def logout(): session.clear(); return jsonify(ok=True)
@app.get('/api/auth/me')
def me():
    u=actual_user(); return jsonify(autenticada=bool(u),usuario=public_user(u) if u else None)

@app.get('/api/tarifa')
@login_required
def cotizar():
    u=actual_user(); km=request.args.get('distancia_km',0,type=float); return jsonify(**tarifa(km,u))

@app.route('/api/viajes',methods=['GET','POST'])
@login_required
def viajes():
    u=actual_user()
    if request.method=='GET': return jsonify([viaje_json(t) for t in viajes_data])
    if u['rol']!='pasajera': return jsonify(error='Solo una pasajera puede solicitar viajes.'),403
    d=request.get_json(silent=True) or {}; origen=str(d.get('origen','')).strip(); destino=str(d.get('destino','')).strip()
    if not origen or not destino: return jsonify(error='Ingresa el origen y el destino.'),400
    acomp=d.get('acompanante') or {}; cantidad=int(acomp.get('cantidad',0) or 0) if acomp.get('viaja_acompanada') else 0
    km=float(d.get('distancia_km',0) or 0); tid=max([t['id'] for t in viajes_data] or [0])+1
    t={'id':tid,'pasajera_id':u['perfil_id'],'conductora_id':None,'origen':origen,'destino':destino,'estado':'Pendiente','fecha_solicitud':datetime.now().strftime('%Y-%m-%d %H:%M'),'distancia_km':km,'pasajeras':int(d.get('pasajeras',1) or 1),'tipo_servicio':d.get('tipo_servicio','Viaje'),'acompanante':{'viaja_acompanada':bool(cantidad),'relacion':acomp.get('relacion'),'cantidad':cantidad,'notas':acomp.get('notas','')},'tarifa':tarifa(km,u,cantidad)}
    viajes_data.append(t); cola_solicitudes.agregar_cola(t); guardar_datos()
    # Se instancia el modelo original y se conserva en la lista enlazada.
    p=objetos_pasajeras.get(u['perfil_id']); obj=ViajeConAcompanante(tid,p,None,origen,destino,cantidad) if p else None
    if obj: lista_viajes.agregar(obj)
    return jsonify(ok=True,viaje=viaje_json(t)),201

@app.get('/api/conductora/solicitudes')
@login_required
def solicitudes():
    u=actual_user()
    if u['rol']!='conductora': return jsonify(error='Esta sección es solo para conductoras.'),403
    cap=int((u.get('vehiculo') or {}).get('capacidad',4))
    # "pasajeras" ya representa el TOTAL de personas (incluye a la conductora
    # de la solicitud y sus acompañantes); no se debe sumar acompañante otra vez.
    return jsonify(solicitudes=[
        viaje_json(t) for t in viajes_data
        if t['estado']=='Pendiente' and int(t.get('pasajeras',1))<=cap
    ])

@app.get('/api/mis-viajes')
@login_required
def mis_viajes():
    u=actual_user(); mine=[]
    for t in viajes_data:
        if (u['rol']=='pasajera' and t.get('pasajera_id')==u['perfil_id']) or (u['rol']=='conductora' and t.get('conductora_id')==u['perfil_id']): mine.append(viaje_json(t))
    activos=[t for t in mine if t['estado'] not in ('Finalizado','Cancelado')]; historial=[t for t in mine if t['estado'] in ('Finalizado','Cancelado')]
    return jsonify(activos=activos,historial=historial,total=len(mine))

@app.get('/api/resumen')
@login_required
def resumen(): return jsonify(total_viajes=len(viajes_data),total_pendientes=sum(t['estado']=='Pendiente' for t in viajes_data),total_alertas=len(cola_alertas.mostrar()))
@app.get('/api/conductoras')
def conductoras():
    out=[]
    for u in usuarios:
        if u['rol']=='conductora': out.append({'id':u['perfil_id'],'nombre':u['nombre'],'telefono':u['telefono'],'disponible':True,'vehiculo':u.get('vehiculo',{})})
    return jsonify(out)
@app.get('/api/pasajeras')
def pasajeras(): return jsonify([{'id':u['perfil_id'],'nombre':u['nombre']} for u in usuarios if u['rol']=='pasajera'])

@app.post('/api/viajes/<int:tid>/aceptar')
@login_required
def aceptar(tid):
    u=actual_user()
    if u['rol']!='conductora': return jsonify(error='Solo una conductora puede aceptar solicitudes.'),403
    t=next((x for x in viajes_data if x['id']==tid),None)
    if not t or t['estado']!='Pendiente': return jsonify(error='La solicitud ya no está disponible.'),404
    capacidad=int((u.get('vehiculo') or {}).get('capacidad',4))
    if int(t.get('pasajeras',1))>capacidad:
        return jsonify(error='Este viaje supera la capacidad de tu vehículo.'),400
    t['conductora_id']=u['perfil_id']; t['estado']='Conductora asignada'; guardar_datos(); return jsonify(ok=True,viaje=viaje_json(t))
@app.post('/api/viajes/<int:tid>/iniciar')
@login_required
def iniciar(tid):
    u=actual_user(); t=next((x for x in viajes_data if x['id']==tid),None)
    if not t or t.get('conductora_id')!=u['perfil_id'] or t['estado']!='Conductora asignada': return jsonify(error='No puedes iniciar este viaje.'),400
    t['estado']='En curso'; guardar_datos(); return jsonify(ok=True,viaje=viaje_json(t))
@app.post('/api/viajes/<int:tid>/finalizar')
@login_required
def finalizar(tid):
    u=actual_user(); t=next((x for x in viajes_data if x['id']==tid),None)
    if not t or (u['rol']=='conductora' and t.get('conductora_id')!=u['perfil_id']) or (u['rol']=='pasajera' and t.get('pasajera_id')!=u['perfil_id']) or t['estado']!='En curso': return jsonify(error='No puedes finalizar este viaje.'),400
    t['estado']='Finalizado'; pila_historial.agregar_pila(t); guardar_datos(); return jsonify(ok=True,viaje=viaje_json(t))
@app.get('/api/alertas')
def alertas(): return jsonify([])
@app.get('/api/salud')
def salud(): return jsonify(ok=True,servicio='YANY',estructuras=['Lista','Cola','Pila','Arbol'])

cargar_datos()
if __name__=='__main__': app.run(debug=True)
