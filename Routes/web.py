from Controllers.home import HomeController
from Libs.Route import Route


class web(Route):

    def __init__(self, app, conf):
        super(web, self).__init__(app, self.__class__.__name__, conf)

        @self.route("/version")
        def version():
            return "ZeroX Web version 1.0"

        self.get("/",HomeController,"index",None,"home")
        self.get("home",HomeController,"index",None,"home")
        self.get("index",HomeController,"index",None,"home")


