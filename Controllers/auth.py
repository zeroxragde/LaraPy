import hashlib
import base64
import time
from Models.token import Token
from Models.usuario import Usuario
from Libs.Controlador import Controlador
from datetime import datetime
import pdb
class AuthController(Controlador):
    def __init__(self):
        super(AuthController, self).__init__()

    def generate_token(self, user_id, expiration_time):
        # Definir la clave secreta para firmar el token
        secret_key = self._config.get("app", "SECRET_KEY")
        # Obtener la marca de tiempo actual en segundos
        current_time = int(time.time())
        if expiration_time == -1:
            expiration_timestamp = None  # Sin fecha de expiración
        else:
            expiration_timestamp = current_time + expiration_time
        # Concatenar el ID de usuario y la marca de tiempo de expiración
        data = f'{user_id}.{expiration_timestamp}'
        # Calcular el hash SHA-1 del dato utilizando la clave secreta
        hash_object = hashlib.sha1(secret_key.encode() + data.encode())
        signature = hash_object.hexdigest()
        # Codificar el dato y la firma en base64
        token = base64.urlsafe_b64encode(f'{data}.{signature}'.encode()).decode()
        # Retornar el token generado
        return token

    def login(self):
        # Obtener los datos enviados en el cuerpo de la solicitud POST
            data = self.request.json
            # Acceder a los valores enviados
            user = data.get('user')
            password = data.get('pass')
            objUser= Usuario()
            respuesta = objUser.where({
                'username': {
                    'value': user
                },
                'password': {
                    'value': password
                }
            })
            if len(respuesta.get()) > 0:
                objUser = respuesta.get()[0]
                token_serial = self.generate_token(objUser.id, int(self._config.get("app","TOKEN_EXPIRATION_TIME_SEG")))
                token = Token()
                token.iduser = objUser.id
                token.token = token_serial
                token.expiration = int(self._config.get("app","TOKEN_EXPIRATION_TIME_SEG"))
                token.create_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                token.saveToken()
                return  self.response.responseUser(objUser.toDIC(), token.toDIC())
            else:
                return  self.response.responseError('No se encontró el usuario')
    def logout(self):
        data = self.request.json
        token = data.get('token')
        objtoken = Token()
        respuesta = objtoken.where({
            'token': {
                'value': token
            }
        })

        if len(respuesta.get()) > 0:
            respuesta.get()[0].revoke = 1
            respuesta.get()[0].save()
            return self.response.responseAceptada('Sesion cerrada')
        else:
            return self.response.responseError('Error al cerrar sesion')
    def checktoken(self):
        return self.response.responseAceptada('Correcto')