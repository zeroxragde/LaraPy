from Controllers.auth import AuthController
from Libs.Route import Route

class api(Route):

    def __init__(self, app, conf):
        super(api, self).__init__(app, self.__class__.__name__, conf)

        # Definir ruta

        @self.route("/API/version")
        def version():
            return "ZeroX API version 1.0"

        self.group("auth", [
            {"endpoint": 'login', "controller": AuthController, 'func': "login", "method": "POST"},
            {"endpoint": 'logout', "controller": AuthController, 'func': "logout", "method": "POST"},
            {"endpoint": 'check', "controller": AuthController, 'func': "checktoken", "method": "POST",
             "middleware": "authMiddleware:tokenCheck"}
        ])
