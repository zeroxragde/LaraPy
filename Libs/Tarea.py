from Enums.TimeUnit import TimeUnit
from Libs.Config import Config


class Tarea:

    def __init__(self, _config:Config):
        self.unidad: TimeUnit = TimeUnit.segundos
        self.time=1
        self.worked=""
        self.estado = True
        self._config = _config
        self.name = "Tarea"
        self.description = "Tarea programada"
