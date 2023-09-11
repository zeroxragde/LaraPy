import schedule
import time
import threading
from Enums.TimeUnit import TimeUnit
from Libs.Tarea import Tarea


class Scheduler:
    def __init__(self):
        self.unidades = []
        self.tasks = []

    def add_task(self, task_object: Tarea):
        interval_in_seconds = task_object.time * task_object.unidad.value
        self.tasks.append(
            {"interval": interval_in_seconds, "task_object": task_object, "task_method": task_object.worked})

    def schedule_tasks(self):
        for task in self.tasks:
            interval = task["interval"]
            task_object = task["task_object"]
            task_method = task["task_method"]
            print(f"Programando tarea: {task_object} - Método: {task_method} - Intervalo: {interval} segundos")
            schedule.every(interval).seconds.do(self.execute_task, task)

    @staticmethod
    def execute_task(task):
        task_object = task["task_object"]
        task_method = task["task_method"]
        getattr(task_object, task_method)()

    def run(self):
        # Creamos un hilo para ejecutar las tareas
        thread = threading.Thread(target=self._run_tasks)
        thread.start()

    @staticmethod
    def _run_tasks():
        while True:
            schedule.run_pending()
            time.sleep(1)
