import threading
import os
from future.moves import subprocess
from Libs.Iniciador import Iniciador


def init(myapp):
    pass


# Para arrancar el servidor de forma local
if __name__ == '__main__':
    app = Iniciador(init)
    app.start()
