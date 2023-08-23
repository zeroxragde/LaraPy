class ZeroXException(Exception):
    def __init__(self, m):
        self.mensaje = m

    def __str__(self):
        return f"Error: {self.mensaje}"