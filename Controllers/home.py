from Libs.Controlador import Controlador


class HomeController(Controlador):
    def __init__(self):
        super(HomeController, self).__init__()

    def index(self):
        vista = self.View.showView("home",{"username": "edgar"})
        return self.response.responseWeb(vista)
