class Resena:
    def __init__(self, id: int, calificacion: int, comentario: str = ""):
        self.__id = id
        self.calificacion = calificacion  
        self.comentario = comentario

    #GETTERS
    @property
    def id(self):
        return self.__id
    @property
    def calificacion(self):
        return self.__calificacion
    @property
    def comentario(self):
        return self.__comentario
    
    #SETTERS
    @id.setter
    def id(self, id):
        self.__id = id 
    @calificacion.setter
    def calificacion(self, calificacion: int):
        if not isinstance(calificacion, int) or not 1 <= calificacion <= 5: #SI LA CALIFICACIÓN NO ES UN NÚMERO ENTERO, O NO ESTÁ ENTRE 1 Y 5 ENTONCES ES UN ERROR.
            raise ValueError("La calificación debe ser un entero entre 1 y 5")
        self.__calificacion = calificacion
    @comentario.setter
    def comentario(self, comentario: str):
        self.__comentario = comentario

    #MÉTODO MOSTRAR INFO
    def mostrar_info(self):
        return f"Reseña {self.id}: {self.calificacion}/5 - {self.comentario}"
        