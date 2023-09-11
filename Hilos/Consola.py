from Models.hilo import Hilo


class Consola(Hilo):
    def __init__(self):
        super(Consola, self).__init__()
        self.name = "Consola"
        self.funcion = self.RunCommand

    def RunCommand(self):
        while True:
            print("edgasr")

