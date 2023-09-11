import sys
import os
from flask import Flask, redirect
from flask_cors import CORS
from flask_caching import Cache


class ZeroXAPI:

    def __init__(self, port=41, middlewares=None):
        self._port = port
        self.middleware = middlewares
        # Directorio de trabajo actual
        cwd = os.getcwd()
        sys.path.append(cwd)
        # Crear instancia de Flask
        self._api = Flask(__name__)
        CORS(self._api, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "OPTIONS"])
        self.cache = Cache(self._api, config={'CACHE_TYPE': 'simple'})
        os.environ['WERKZEUG_RUN_MAIN'] = 'True'

    def getFlesk(self):
        return self._api

    def start(self):
        self._api.run(port=self._port, threaded=True)

    # Configuración de la aplicación para mod_wsgi
    def application(self, environ, start_response):
        # Asegúrate de que las solicitudes con URL sin barras invertidas sean redirigidas a la versión con barras invertidas
        if not environ['PATH_INFO'].endswith('/'):
            return redirect(environ['PATH_INFO'] + '/', code=301)

        # Configurar la variable de entorno "SCRIPT_NAME"
        script_name = os.path.dirname(os.path.abspath(__file__))
        environ['SCRIPT_NAME'] = script_name

        # Cargar la aplicación
        myapi = Flask(__name__)

        # Devolver la respuesta de la aplicación
        return myapi(environ, start_response)
