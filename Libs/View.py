import os
import re


class View:

    def __init__(self):
        self._views = {}
        directorio_web = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                      os.getenv("DIR_VIEWS"))
        files = os.listdir(directorio_web)
        for archivo in files:
            # Ignorar archivos que no son webs
            if not archivo.endswith(".web"):
                continue
            nombre_archivo = os.path.splitext(archivo)[0]  # Obtener el nombre sin extensión
            ruta_archivo = os.path.join(directorio_web, archivo)
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                contenido_archivo = f.read()
                self._views[nombre_archivo] = contenido_archivo

    def showView(self, web, data=None):
        if data is None:
            data = {}
        webactual = self._views[web]
        if not webactual:
            return webactual
        else:
            def reemplazo(match):
                variable = match.group(1)
                return data.get(variable, match.group(0))

            return re.sub(r'\{([^}]+)\}', reemplazo, webactual)
