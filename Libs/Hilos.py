import os
import importlib.util
import threading


class Hilos:

    def __init__(self):
        self._Hilos = []

    def iniciar(self):
        print("INICIANDO")
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            os.getenv("DIR_HILOS"))
        files = os.listdir(path)
        for file in files:
            # Ignorar archivos que no son hilos
            if not file.endswith(".py"):
                continue
            module_name = file[:-3]  # Quitar la extensión .py
            module_path = os.path.join(path, file)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            myhilo = getattr(module, module_name)()
            if myhilo.funcion is not None:
                hilo1 = threading.Thread(target=myhilo.funcion)
                hilo1.daemon = True
                hilo1.start()
                # hilo1.join()
                self._Hilos.append(hilo1)
        return self
