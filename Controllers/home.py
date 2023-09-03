from Libs.Controlador import Controlador


class HomeController(Controlador):
    def __init__(self):
        super(HomeController, self).__init__()

    def index(self):
        return self.response.responseWeb(self.View.showView("home",{"username": "edgar"}))
