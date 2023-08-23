from datetime import timedelta, datetime

from Libs.Modelo import Modelo


class Token(Modelo):
    def __init__(self):
        super().__init__("tokens")

    def saveToken(self):
        # checar si se va updatear
        res = self.where({
            'iduser': {
                "value": self.iduser
            }
        })

        if len(res.get()) == 0:
            self.save()
        else:
            token_user = res.get()[0]
            fecha_actual = datetime.now() #
            fecha_row = datetime.strptime(token_user.create_date, "%Y-%m-%d %H:%M:%S")

            # Fecha de expiración
            fecha_expiracion = fecha_row + timedelta(seconds=int(token_user.expiration))

            # Verificar si ha pasado la expiración
            ha_pasado_expiracion = fecha_actual > fecha_expiracion
            if ha_pasado_expiracion or token_user.revoke == "1":
                token_user.revoke = "1"
                token_user.save()
                self.save()
            else:
                self.iduser = token_user.iduser
                self.id = token_user.id
                self.token = token_user.token
                self.expiration = token_user.expiration
                self.create_date = token_user.create_date
