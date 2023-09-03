import re
import os
import mimetypes
from Libs.Controlador import Controlador


class ResourcesController(Controlador):
    def __init__(self):
        super(ResourcesController, self).__init__()

    def index(self, tipo, resource):
        extension = re.search(r'\.([^.]+)$', resource).group(1) if '.' in resource else ''
        # Obtener la lista de archivos en el directorio
        archivos_web = [archivo for archivo in os.listdir("Assets/web/" + tipo) if archivo.endswith(extension)]
        # Leer el contenido de los archivos .web y almacenarlos en el diccionario
        for archivo in archivos_web:
            nombre_archivo = os.path.splitext(archivo)[0]  # Obtener el nombre sin extensión
            ruta_archivo = os.path.join("Assets/web/" + tipo, archivo)
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                contenido_archivo = f.read()
                mimetype = mimetypes.guess_type(archivo)[0] if extension else None
                if mimetype is None:
                    if extension == 'tag':
                        mimetype = 'riot'
                return self.response.responseResource(contenido_archivo, mimetype)
        return self.response.responseWeb("404 No se encontro recurso")
    
