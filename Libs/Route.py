from flask import Blueprint, request
import importlib.util
import os
import types
import re
import string
import random
from Models.Minion import Minion


class Route:
    def __init__(self, app, name, cof):
        self.api = app.getFlesk()
        self.app = app
        self._config = cof
        self.request = request
        self._control = Blueprint(name, __name__)
        self.route = self._control.route
        self.cache = self.app.cache

    def register(self):
        # Registra el blueprint en tu aplicación Flask
        self.api.register_blueprint(self._control)

    def resource(self, endpoint, controller):
        control = controller()
        if hasattr(controller, 'index'):
            self.api.add_url_rule(f'/{endpoint}', 'index', control.index, methods=['GET'])
        if hasattr(controller, 'create'):
            self.api.add_url_rule(f'/{endpoint}/create', 'create', control.create, methods=['GET'])
        if hasattr(controller, 'store'):
            self.api.add_url_rule(f'/{endpoint}', 'store', control.store, methods=['POST'])
        if hasattr(controller, 'show'):
            self.api.add_url_rule(f'/{endpoint}/<int:id>', 'show', control.show, methods=['GET'])
        if hasattr(controller, 'edit'):
            self.api.add_url_rule(f'/{endpoint}/<int:id>/edit', 'edit', control.edit, methods=['GET'])
        if hasattr(controller, 'update'):
            self.api.add_url_rule(f'/{endpoint}/<int:id>', 'update', control.update, methods=['PUT'])
        if hasattr(controller, 'destroy'):
            self.api.add_url_rule(f'/{endpoint}/<int:id>', 'destroy', control.destroy, methods=['DELETE'])

    def group(self, groupname, funcRoutes):
        for funcs in funcRoutes:
            middleware = None
            endpoint_clear = re.sub(r'<[^>]*>', '', funcs["endpoint"])
            endpoint_clear = endpoint_clear.replace("/", "")
            if funcs.get("middleware"):
                middleware = [funcs["middleware"]]
            if funcs["method"].lower() == "get":
                self.get("/" + groupname + "/" + funcs["endpoint"], funcs["controller"], funcs["func"], middleware,
                         endpoint_clear)
            if funcs["method"].lower() == "post":
                self.post("/" + groupname + "/" + funcs["endpoint"], funcs["controller"], funcs["func"], middleware,
                          endpoint_clear)

    @staticmethod
    def generar_clave_aleatoria(longitud):
        alfabeto = string.ascii_letters
        return ''.join(random.choice(alfabeto) for _ in range(longitud))

    def get(self, endpoint, controller, func, middleware=None, endpointfree=""):
        control = controller()
        method = getattr(control, func)

        if middleware is not None and len(middleware) > 0:
            for namefunc in middleware:
                splitData = namefunc.split(":")
                nameMiddle = splitData[0]
                nameFunc = splitData[1]
                realNameFunc = '_middleFor_' + endpointfree + '_' + nameFunc  # nombre de la nueva funcion
                inMiddle: Minion = self.app.middleware.minions[nameMiddle]

                # Crear una función de envoltorio con el middleware aplicado
                def wrapped_function(middleware_method=getattr(inMiddle.Worked, nameFunc), **kwargs):
                    methodo = getattr(control, func)
                    middleware_methodo = getattr(inMiddle.Worked, nameFunc)
                    return middleware_methodo(methodo, **kwargs)

                # Asignar el nombre de la función envuelta al nombre asignado
                wrapped_function.__name__ = realNameFunc
                # Crear un nuevo método con el nombre asignado y la función envuelta
                new_method = types.MethodType(wrapped_function, control)
                # Asignar el nuevo método a la instancia de la clase control
                setattr(control, realNameFunc, new_method)
                # Utilizar el nuevo método en lugar del original
                method = new_method
                self.api.add_url_rule(f'/{endpoint}', view_func=method, methods=['GET'])
                return self

        realNameFunc = self.generar_clave_aleatoria(16)

        # Crear una función de envoltorio con el middleware aplicado
        def wrapped_function(_method=method,f=func, **kwargs):
            methodo = getattr(_method, f)
            return methodo(**kwargs)

        # Asignar el nombre de la función envuelta al nombre asignado
        wrapped_function.__name__ = realNameFunc
        # Crear un nuevo método con el nombre asignado y la función envuelta
        new_method = types.MethodType(wrapped_function, control)
        # Asignar el nuevo método a la instancia de la clase control
        setattr(control, realNameFunc, new_method)
        # Utilizar el nuevo método en lugar del original
        method = new_method
        self.api.add_url_rule(f'/{endpoint}', view_func=method, methods=['GET'])

    def post(self, endpoint, controller, func, middleware=None, endpointfree=""):
        control = controller()
        method = getattr(control, func)
        if middleware is not None and len(middleware) > 0:
            for namefunc in middleware:
                splitData = namefunc.split(":")
                nameMiddle = splitData[0]
                nameFunc = splitData[1]
                realNameFunc = '_middleFor_' + endpointfree + '_' + nameFunc  # nombre de la nueva funcion
                inMiddle: Minion = self.app.middleware.minions[nameMiddle]

                # Crear una función de envoltorio con el middleware aplicado
                def wrapped_function(middleware_method=getattr(inMiddle.Worked, nameFunc), **kwargs):
                    methodo = getattr(control, func)
                    middleware_methodo = getattr(inMiddle.Worked, nameFunc)
                    return middleware_methodo(methodo, **kwargs)

                # Asignar el nombre de la función envuelta al nombre asignado
                wrapped_function.__name__ = realNameFunc
                # Crea un nuevo método con el nombre asignado y la función envuelta
                new_method = types.MethodType(wrapped_function, control)
                # Asignar el nuevo método a la instancia de la clase control
                setattr(control, realNameFunc, new_method)
                # Utilizar el nuevo método en lugar del original
                method = new_method
                self.api.add_url_rule(f'/{endpoint}', view_func=method, methods=['POST'])
                return self

        realNameFunc = self.generar_clave_aleatoria(16)

        # Crear una función de envoltorio con el middleware aplicado
        def wrapped_function(_method=method,f=func, **kwargs):
            methodo = getattr(_method, f)
            return methodo(**kwargs)

        # Asignar el nombre de la función envuelta al nombre asignado
        wrapped_function.__name__ = realNameFunc
        # Crear un nuevo método con el nombre asignado y la función envuelta
        new_method = types.MethodType(wrapped_function, control)
        # Asignar el nuevo método a la instancia de la clase control
        setattr(control, realNameFunc, new_method)
        # Utilizar el nuevo método en lugar del original
        method = new_method
        self.api.add_url_rule(f'/{endpoint}', view_func=method, methods=['POST'])
        return self
