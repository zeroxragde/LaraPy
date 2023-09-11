from Enums.HttpStatus import HttpStatus
from Libs.Response import Response
from flask import Response as FResponse


class ApiResponse(Response):
    def __init__(self):
        super().__init__()

    def responseError(self, mensaje):
        return self.jsonCustomResponse({
            'error': mensaje
        }, HttpStatus.HTTP_NO_AUTORIZADO)

    def responseAceptada(self, mensaje):
        return self.jsonCustomResponse({
            'data': mensaje
        }, HttpStatus.HTTP_OK)

    @staticmethod
    def responseWeb(web):
        response = FResponse(web, mimetype='text/html')
        return response

    @staticmethod
    def responseResource(resource,type):
        response = FResponse(resource, mimetype=type)
        return response

    @staticmethod
    def responseVideo(func):
        response = FResponse(func, mimetype='video/mp4')
        response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache durante 1 hora en el navegador del usuario
        return response

    def responseUser(self, user, token):
        return self.jsonCustomResponse({
            'data': user,
            'tokendata': token
        }, HttpStatus.HTTP_OK)
