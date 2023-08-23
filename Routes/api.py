from Controllers.auth import AuthController
from Controllers.youtube import YoutubeController
from Controllers.youtubeplaylist import YoutubePlaylistController
from Libs.Route import Route
from Response.ApiRespnse import ApiResponse

class api(Route):

    def __init__(self, app,conf):
        super(api,self).__init__(app, self.__class__.__name__, conf, )

        # Definir ruta
        @self.route("/")
        def hello():
            return "Hola, mundo!"

        @self.route("/version")
        def version():
            return "ZeroX API version 1.0"

        self.group("auth",[
            {"endpoint":'login',"controller":AuthController,'func':"login", "method":"POST"},
            {"endpoint":'logout',"controller":AuthController,'func':"logout", "method":"POST"},
            {"endpoint":'check',"controller":AuthController,'func':"checktoken", "method":"POST",
             "middleware":"authMiddleware:tokenCheck"}
        ])

        self.group("youtube",[
            {"endpoint": 'categorias/<idpais>', "controller": YoutubeController, 'func': "categorias", "method": "GET"},
            {"endpoint": 'q/<query>', "controller": YoutubeController, 'func': "buscar", "method": "GET",
             "middleware":"authMiddleware:tokenCheck"},
            {"endpoint": 'detail/<videoid>', "controller": YoutubeController, 'func': "getVideoData", "method": "GET"},
            {"endpoint": 'stream/<videoid>', "controller": YoutubeController, 'func': "stream", "method": "GET"},
            {"endpoint": 'streaming/<videoid>', "controller": YoutubeController, 'func': "streamingVideo", "method": "GET"}
        ])

        #DEJAR PENDIENTE ESTO
        self.group("perfil",[
           {"endpoint": 'listas', "controller": YoutubePlaylistController, 'func': "obtenerListas", "method": "GET",
            "middleware": "authMiddleware:tokenCheck"},
        ])
        # CREAR API PARA CONSULTAR VIDEO DESDE LA VPN

