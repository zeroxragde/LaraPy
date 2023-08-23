from Enums.HttpStatus import HttpStatus
from Models.token import Token
from Libs.Response import Response
from flask import request
class authMiddleware:

    def __init__(self):
        self.func_actual= None

    def setFunc(self, f):
        self.func_actual = f
    @staticmethod
    def tokenCheck(func, **kwargs):
        token=request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]  # Obtenemos solo el valor del token sin el prefijo 'Bearer '
            if authMiddleware._verify_token(token):
                    return func(**kwargs)
        response = Response('Error de autenticacion. Se requiere un token valido.',
                            HttpStatus.HTTP_NO_AUTORIZADO)
        return response.jsonResponse()

    @staticmethod
    def _verify_token(tok):
        # Aquí puedes implementar tu lógica de verificación del token
        # Puedes utilizar librerías como PyJWT para verificar y decodificar el token
        token = Token()
        token = token.where({
                'token': {
                    'value': tok
                }
            })
        if len(token.get()) > 0:
            return True
        return False