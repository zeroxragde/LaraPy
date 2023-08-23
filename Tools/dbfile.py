import pickle


class dbfile:
    @staticmethod
    def save(obj, archivo):
        with open(archivo, 'wb') as file:
            pickle.dump(obj, file)

    @staticmethod
    def load(archivo):
        with open(archivo, 'rb') as file:
            obj = pickle.load(file)
            return obj
