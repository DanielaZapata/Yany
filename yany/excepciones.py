class YANYError(Exception):
    """Excepción base para todos los errores del sistema YANY."""
    pass


class PasajeraNoEncontrada(YANYError):
    pass


class ConductoraNoEncontrada(YANYError):
    pass


class ViajeNoEncontrado(YANYError):
    pass


class ConductoraNoDisponible(YANYError):
    pass


class ConductoraNoCertificada(YANYError):
    pass


class ColaVaciaError(YANYError):
    pass


class PilaVaciaError(YANYError):
    pass


class ArchivoInvalidoError(YANYError):
    pass