import sys
import os
from dotenv import load_dotenv
import importlib.util

from Models.Minion import Minion


class Middleware:
    def __init__(self):
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            os.getenv("DIR_MIDDLEWARE"))
        files = os.listdir(path)
        self.minions = {}
        for file in files:
            # Ignorar archivos que no son middles
            if not file.endswith(".py"):
                continue
            # Importar la configuracion
            module_name = file[:-3]  # Quitar la extensión .py
            module_path = os.path.join(path, file)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            middleware = getattr(module, module_name)()
            minion = Minion()
            minion.Worked = middleware
            minion.path = module_path
            minion.funcName= [func for func in dir(middleware) if callable(getattr(middleware, func)) and
                                  (not func.startswith('__') or not func.endswith('__'))]

            self.minions[module_name] = minion