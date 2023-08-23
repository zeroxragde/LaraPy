import uuid
import sqlite3
import os
from dbutils.persistent_db import PersistentDB
import importlib.util

from Libs.Config import Config
from Libs.Middleware import Middleware
from Libs.Scheduler import Scheduler
from Libs.ZeroXAPI import ZeroXAPI


class Iniciador:
    pool = None
    def __init__(self, funcion):
        self.config = Config()
        self.listTareas = []
        self._dir_path = self.config.get("app","DB_PATH")
        self._dbname = self.config.get("app","DB_NAME")
        self._maxusage = int(self.config.get("app","DB_MAX_USE"))
        self._id = str(uuid.uuid4())
        # Crear el Connection Pool con la función de fábrica y el máximo de uso
        def create_connection():
            conn = sqlite3.connect(self._dir_path + "/" + self._dbname.lower() + '.db')
            conn.row_factory = sqlite3.Row
            return conn
        Iniciador.pool = PersistentDB(creator=create_connection, maxusage=self._maxusage)
        # Registrar Middles
        self.middleware = Middleware()
        self.api = ZeroXAPI(int(self.config.get("app", "API_PORT")),self.middleware)

        # Iniciar rutas
        directory =  os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.getenv("DIR_ROUTES"))
        files = os.listdir(directory)
        for file in files:
            # Ignorar archivos que no son rutas
            if not file.endswith(".py"):
                continue
            module_name = file[:-3]  # Quitar la extensión .py
            module_path = os.path.join(directory, file)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            route = getattr(module, module_name)(self.api,self.config)
            route.register()

        # Crear instancia de Scheduler y programar las tareas usando el objeto y el nombre del método
        # Iniciar tareas
        directory =  os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            os.getenv("DIR_TAREAS"))
        scheduler = Scheduler()
        files = os.listdir(directory)
        for file in files:
            # Ignorar archivos que no son tareas
            if not file.endswith(".py"):
                continue
            module_name = file[:-3]  # Quitar la extensión .py
            module_path = os.path.join(directory, file)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            tarea = getattr(module, module_name)(self.config)
            if tarea.estado:
                self.listTareas.append(tarea)
                scheduler.add_task(tarea)

        scheduler.schedule_tasks()
        scheduler.run()


        self._funcion = funcion
        # Iniciamos el servidor flesk


    def start(self, api=True):
        self._funcion(self)
        if api:
            self.api.start()