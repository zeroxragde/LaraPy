from Controllers.auth import AuthController
from Controllers.youtube import YoutubeController
from Controllers.youtubeplaylist import YoutubePlaylistController
from Libs.Route import Route
from Response.ApiRespnse import ApiResponse


class api(Route):

    def __init__(self, app, conf):
        super(api, self).__init__(app, self.__class__.__name__, conf, )

        # Definir ruta
        @self.route("/")
        def hello():
            return "Hola, mundo!"

        @self.route("/version")
        def version():
            return "ZeroX API version 1.0"

        self.group("auth", [
            {"endpoint": 'login', "controller": AuthController, 'func': "login", "method": "POST"},
            {"endpoint": 'logout', "controller": AuthController, 'func': "logout", "method": "POST"},
            {"endpoint": 'check', "controller": AuthController, 'func': "checktoken", "method": "POST",
             "middleware": "authMiddleware:tokenCheck"}
        ])
