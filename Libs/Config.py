import sys
import os
from dotenv import load_dotenv
import importlib.util


class Config:

    def __init__(self):
        self._data = {}
        self.load_env()
        self.load_configs()

    @staticmethod
    def load_env():
        try:
            load_dotenv('.env')  # Cargamos el archivo env
        except Exception as e:
            print("Error: No fue posible cargar el archivo .env")
            print(e)
            sys.exit(1)

    def load_configs(self):
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.getenv("DIR_CONFIGURATIONS"))
        files = os.listdir(path)
        for file in files:
            # Ignorar archivos que no son configuraciones
            if not file.endswith(".py"):
                continue
            # Importar la configuracion
            module_name = file[:-3]  # Quitar la extensión .py
            module_path = os.path.join(path, file)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            variables = module.__dict__
            for variable_name, variable_value in variables.items():
                if not variable_name.startswith("__") and not variable_name == "Tools":  # Ignorar variables especiales
                    self._data[variable_name] = variable_value



    def get(self,config,prop):
        try:
         return self._data[config][prop]
        except (Exception,):
            return None