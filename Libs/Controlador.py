import json
import os
import importlib.util
from functools import wraps
from Libs.Config import Config
from Libs.View import View
from Response.ApiRespnse import ApiResponse
from flask import request


class Controlador:
    def __init__(self):
        # print("nuevo controlador")
        self.funciones = [func for func in dir(self) if callable(getattr(self, func)) and
                          (not func.startswith('__') or not func.endswith('__'))]
        self._config = Config()
        self.View = View()
        self.response = ApiResponse()
        self.request = request

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def request_model(self, model_cls):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    data = request.json

                    module_path = os.path.join('Models', model_cls.lower() + '.py')
                    spec = importlib.util.spec_from_file_location(model_cls, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    modelo = getattr(module, model_cls)()
                    modelo.from_json(json.dumps(data))
                    kwargs['model_instance'] = modelo
                    return func(modelo)
                except ValueError as e:
                    print(e)
                    return self.response.responseError('Invalid data format')

            return wrapper

        return decorator
