from cachetools import TTLCache


class Session:

    def __init__(self):
        self.cache = TTLCache(maxsize=128, ttl=3600)  # Caché con un máximo de 128 elementos y tiempo de vida de 1 hora

    def get(self, clave):
        if clave in self.cache:
            return self.cache[clave]
        else:
            return None

    def set(self, clave, datos):
        if datos != "":
            self.cache[clave] = datos
            return self
        return False

    def session(self, clave, datos=""):
        if clave in self.cache:
            return self.cache[clave]
        else:
            if datos != "":
                self.cache[clave] = datos
                return datos
            return None
