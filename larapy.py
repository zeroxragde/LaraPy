import argparse
import os
import datetime
import re
import importlib.util
import pdb

from Libs.Iniciador import Iniciador
from Libs.ZeroXException import ZeroXException

template_migration = '''
from Libs.Schema import Schema
form Libs.fieldType import fieldType


class {MIGRATION_NAME}(Schema):
    def __init__(self):
        super({MIGRATION_NAME}, self).__init__()

    def up(self):
        return self

    def down(self):
        return self
  
'''

template_middleware = '''

from Enums.HttpStatus import HttpStatus
from Libs.Response import Response

class authMiddleware:

    @staticmethod
    def ejemplo(request,func):
        response = Response('REspuesta',HttpStatus.HTTP_NO_AUTORIZADO)
        return response.jsonResponse()
    @staticmethod
    def ejemplo2(request,func):
        return func()

'''

template_migration_new_table = '''
from Libs.Schema import Schema
from Libs.fieldType import fieldType


class {MIGRATION_NAME}(Schema):
    def __init__(self):
        super({MIGRATION_NAME}, self).__init__()

    def up(self):
        return self.create_table("{MIGRATION_NAME}", [
           {"Campo": "id", "Tipo": fieldType.INTEGER, "ISPRIMARY": True}
        ])

    def down(self):
        return self.drop_table("{MIGRATION_NAME}")
'''

template_migration_add_fields = '''
from Libs.Schema import Schema
from Libs.fieldType import fieldType


class {MIGRATION_NAME}(Schema):
    def __init__(self):
        super({MIGRATION_NAME}, self).__init__()

    def up(self):
        return self.add_field("{TABLE_NAME}", "{MIGRATION_NAME}", fieldType.TEXT)

    def down(self):
        return self.remove_field("{TABLE_NAME}", "{MIGRATION_NAME}")
'''

template_methods = '''
    def index(self):
        return self
    def update(self,):
        return self
'''

template_model = '''
from Libs.Modelo import Modelo


class {MODEL_NAME}(Modelo):
    def __init__(self):
        super().__init__("{MODEL_NAME_LOWER}")

'''

template_controller = '''
from Libs.Controlador import Controlador


class {MODEL_NAME}Controller(Controlador):
    def __init__(self):
        super({MODEL_NAME}Controller, self).__init__()
    {METODOS}
'''

template_route ='''
from Libs.Route import Route

class {ROUTE_NAME}(Route):

    def __init__(self, app, conf, cache):
         super(api,self).__init__(app, self.__class__.__name__, conf, cache)

        # Definir ruta
        @self.route("/")
        def hello():
            return "Hola, mundo!"
'''

template_tarea ='''
from Enums.TimeUnit import TimeUnit
from Libs.Tarea import Tarea

class bitsoTarea(Tarea):
    def __init__(self, config):
        super.__init__(config)
        self.unidad=TimeUnit.minutos
        self.time = 3
        self.worked="MetodoPrueba"
        self.estado = True

    def MetodoPrueba(self):
        print("holita")
        return self

'''

def makeModal(nombre, flag=False):
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Models")
    if not os.path.exists(directory):
        os.makedirs(directory)
    # pdb.set_trace()
    with open(directory + "/" + nombre.lower().strip() + ".py", "w") as archivo:
        contenido = template_model.replace("{MODEL_NAME}", nombre).replace("{MODEL_NAME_LOWER}", nombre.lower())
        archivo.write(contenido)
    return True


def makeRoute(nombre, flag=False):
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Routes")
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory + "/" + nombre.lower().strip() + ".py", "w") as archivo:
        contenido = template_route.replace("{ROUTE_NAME}", nombre)
        archivo.write(contenido)
    return True

def makeController(nombre, flag=False):
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Controllers")
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory + "/" + nombre.lower().strip() + ".py", "w") as archivo:
        contenido = template_controller.replace("{MODEL_NAME}", nombre)
        if flag is not False:
            if flag == "-r":
                contenido = contenido.replace("{METODOS}", template_methods)
            else:
                contenido = contenido.replace("{METODOS}", "")
        else:
            contenido = contenido.replace("{METODOS}", "")
        archivo.write(contenido)
    return True

def makeTarea(nombre, flag=False):
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Controllers")
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory + "/" + nombre.lower().strip() + ".py", "w") as archivo:
        contenido = template_controller.replace("{MODEL_NAME}", nombre)
        if flag is not False:
            if flag == "-r":
                contenido = contenido.replace("{METODOS}", template_methods)
            else:
                contenido = contenido.replace("{METODOS}", "")
        else:
            contenido = contenido.replace("{METODOS}", "")
        archivo.write(contenido)
    return True


def splitNameMigrate(cadena):
    # Extraer "users"
    matches = re.search(r'add_field_([a-zA-Z_]+)_into_table_', cadena)
    data = []
    if matches:
        users = matches.group(1)
        data.append(users)
    # Extraer todo después de "table"
    matches = re.search(r'_table_(.*)', cadena)
    if matches:
        table = matches.group(1)
        data.append(table)
    #pdb.set_trace()
    try:
        if len(data) == 0:
            raise ZeroXException("Revisar el en nombre de la migracion")
        else:
            return data
    except:
        raise ZeroXException("Revisar el en nombre de la migracion")

def makeMigration(nombre, flag=False):
    # Obtener fecha y hora actual
    now = datetime.datetime.now()
    # Formatear fecha y hora en formato deseado
    formatted_date = now.strftime("%Y_%m_%d_%H%M%S")
    # Definimos el patrón que queremos buscar en la cadena
    patron = r"\d{4}_\d{2}_\d{2}_(create_table|add_field\w+)_\w+(_into_\w+)?"
    pattern1 = r'^\d{4}_\d{2}_\d{2}_\d{6}_create_table_\w+$'
    pattern2 = r'^\d{4}_\d{2}_\d{2}_\d{6}_add_\w+_into_\w+$'
    file_name = nombre
    if re.match(pattern1, formatted_date + "_" + nombre) or re.match(pattern2, formatted_date + "_" + nombre):
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DB/Migrations")
        if not os.path.exists(directory):
            os.makedirs(directory)
        contenido = template_migration
        if "create" in nombre.lower():
            contenido = template_migration_new_table
            nombre_final = nombre.replace("create_table_", "")
            tabla = ""
        if "add" in nombre.lower():
            contenido = template_migration_add_fields
            partes = splitNameMigrate(nombre)

            # La palabra "users" estaría en el índice 2 de la lista "partes"
            nombre = partes[0]
            # La palabra "usuarios" estaría en el índice 4 de la lista "partes"
            tabla = partes[1]
            nombre_final = nombre

        with open(directory + "/" + formatted_date + "_" + file_name.lower().strip() + ".py", "w") as archivo:
            archivo.write(contenido.replace("{MIGRATION_NAME}", nombre_final).replace("{TABLE_NAME}", tabla))
        return True
    else:
        print(
            "El nombre tiene un formato erroneo, debe ser  create_table_nombre o add_field_nombrecampo_into_table_nombretabla");
        return False


function_tipo = {
    "model": makeModal,
    "controller": makeController,
    "migration": makeMigration,
    "route": makeRoute,
    "tarea":makeTarea
}


# Define el comando personalizado y sus argumentos
def make(param1, param2, flag1=False):
    function_tipo[param1.lower()](param2, flag1)


def migrate(flag=False):
    # Obtener la lista de archivos en la carpeta
    path = "DB/Migrations"
    files = os.listdir(path)
    # Iterar sobre los archivos
    for file in files:
        # Ignorar archivos que no son migraciones
        if not file.endswith(".py"):
            continue
        # Importar la migración
        module_name = file[:-3]  # Quitar la extensión .py
        new_filename = re.sub(r"\d{4}_\d{2}_\d{2}_\d{6}_", "", module_name)
        new_filename = splitNameMigrate(new_filename)
        print(new_filename)
        module_path = os.path.join(path, file)
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Ejecutar la función up de la migración
        migration = getattr(module, new_filename[0])()  # Cambiar el nombre de la clase según corresponda
        if not migration.revisar_estado(file):
            if flag == "-rollback":
                estado = migration.down()
                print(f"Migracion {file} executando rollback, estado: {estado}")
            else:
                estado = migration.up()
                print(f"Migracion {file} executando, estado: {estado}")
                if estado:
                    migration.actualizar_estado(file)



    print(f"Migracion Completa")


# Configura el analizador de argumentos
parser = argparse.ArgumentParser(description="Crea modelos, controladores, rutas o comandos")
subparsers = parser.add_subparsers(title='Comandos disponibles', dest='command')

# Comando "make"
parser_make = subparsers.add_parser('make', help='Crea un modelo o un controlador')
parser_make.add_argument('tipo', choices=['model', 'controller', 'migration', 'route'], help='Tipo de archivo a crear')
parser_make.add_argument('nombre', help='Nombre del archivo a crear')
parser_make.add_argument('-r', '--resources', action='store_const', const='M', default=False,
                         help='Agregar métodos de CRUD', dest="r")

# Comando "migrate"
parser_migrate = subparsers.add_parser('migrate', help='Realiza migraciones')
parser_migrate.add_argument('-m', '--modelo', action='store_const', const='-m', default=False,
                            help='Realizar migración de modelo', dest="m")

# Analiza los argumentos de línea de comando
args = parser.parse_args()

# Ejecuta el comando personalizado correspondiente
if args.command == 'make':
    make(args.tipo, args.nombre, flag1=args.r)

elif args.command == 'migrate':
    migrate(flag=args.m)


