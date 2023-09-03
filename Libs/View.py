import os
import re

from Libs.Config import Config


class View:

    def __init__(self):
        self._views = {}
        self._template = ""
        self._config = Config()

        self.generarTemplate()
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

    def generarTemplate(self):
        directorio_web_template = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                               os.getenv("FILE_PATH_INDEX_TEMPLATE"))
        with open(directorio_web_template, "r", encoding="utf-8") as f:
            contenido_archivo = f.read()
            self._template = contenido_archivo

    def showView(self, web, data=None):
        if data is None:
            data = {}
        try:
            self.FrameWorkPreparacion()
            webactual = self._views[web]
            if not webactual:
                return webactual
            else:
                def reemplazo(match):
                    variable = match.group(1)
                    return data.get(variable, match.group(0))

            webf = re.sub(r'\{([^}]+)\}', reemplazo, webactual)
            webFinal = self._template.replace("[@WEBContent]", webf)
            return webFinal
        except (Exception, ):
            if "404" in self._views:
                return self._views["404"]
            else:
                return '404 WebNotFound'

    def FrameWorkPreparacion(self):
        try:
            archivos_framework = [archivo for archivo in os.listdir(self._config.get("app", "DIR_FRAMEWORK_FILES"))]
            # Leer el contenido de los archivos .web y almacenarlos en el diccionario
            files_framework_paths = []
            for archivo in archivos_framework:
                nombre_archivo = os.path.splitext(archivo)[0]  # Obtener el nombre sin extensión
                files_framework_paths.append(nombre_archivo)
            riotjs_scripts = ""
            riotjs_scripts_tagname = ""
            if self._config.get("app", "WEB_FRAMEWORK") == "RIOTJS":
                for filename in files_framework_paths:
                    riotjs_scripts += "<script type='riot' src='/susi/web/riotjs/" + filename + ".tag'></script>"
                    riotjs_scripts_tagname += "riot.mount('login-form')"

            if riotjs_scripts != "":
                self._template = self._template.replace("[@scriptTags]", riotjs_scripts)
                self._template = self._template.replace("[@scriptTagsMount]", riotjs_scripts_tagname)
        except (Exception,):
            if "404" in self._views:
                return self._views["404"]
            else:
                return '404 WebNotFound'
