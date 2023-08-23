import os
class Tools:
    def __init__(self):
        pass

    @staticmethod
    def env(key):
      return os.getenv(key)