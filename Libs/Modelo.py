import importlib
import json
import os
import sys

from pattern.text.en import singularize
from Controllers.dbController import dbController
import inspect

from Libs.ZeroXException import ZeroXException


class Modelo:
    def __init__(self,  *args):
        self._fields = []
        self._idModel = "id"
        self._ruta = __file__
        if len(args) > 0:
            self._table = args[0]
            self._db = dbController()

            super(Modelo, self).__init__()
            self._fields = self._db.getFields(self._table)
            for field in self._fields:
                setattr(self, field, None)
        else: #Los modelos que tiene por default sus propiedades
            for field in self.__dict__:
                self._fields.append(field)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def findOne(self, idt):
        rows = self._db.where(self._table, {
            self._idModel: {
                'value': idt
            }
        })
        for row in rows:
            for prop in self.props():
                setattr(self, prop, row[prop])
        return self

    def hasMany(self, related_model, foreign_key=None, local_key=None):
        """
        Define a one-to-many relationship.
        """
        if isinstance(related_model, str):
            clase = getattr(globals()[related_model], related_model)()
        else:
            clase = related_model
        if foreign_key is None:
            foreign_key = 'id'
        if local_key is None:
            local_key = self._idModel

        return clase.where({local_key: {'value': getattr(self, foreign_key)}}).get()

    def belongsTo(self, related_model, foreign_key=None, local_key=None):
        """
        Define an inverse one-to-one or one-to-many relationship.
        """
        if isinstance(related_model, str):
            clase = getattr(globals()[related_model], related_model)()
        else:
            clase = related_model
        if foreign_key is None:
            foreign_key = clase.__name__.lower() + '_id'
        if local_key is None:
            local_key = 'id'

        return clase.where({local_key: {'value': getattr(self, foreign_key)}}).first()

    def hasOne(self, related_model, foreign_key=None, local_key=None):
        """
        Define a one-to-one relationship.
        """
        if foreign_key is None:
            foreign_key = self.__class__.__name__.lower() + '_id'
        if local_key is None:
            local_key = 'id'

        # Get the rows from the related model where the foreign key matches
        # the value of the local key of this model
        where_dict = {foreign_key: {'value': getattr(self, local_key)}}
        rows = related_model.where(where_dict).get()

        # Return the first row as an instance of the related model
        if len(rows) > 0:
            related_obj = related_model()
            related_obj.__dict__.update(rows[0])
            return related_obj
        else:
            return None

    '''
    {
        'nombre': {'value': 'Juan'},
        'edad': {'value': 25, 'operator': '>'},
        'logical_operator': 'OR'
    },
    {
        'nombre': {'value': 'María'},
        'edad': {'value': 30}
    }
    '''

    def where(self, dic_where):
        rows = self._db.where(self._table, dic_where)
        resultados = []
        for row in rows:
            obj = self.__class__()  # crear una instancia del objeto actual
            for prop in self.props():
                setattr(obj, prop, row[prop])
            resultados.append(obj)
        self._db.set("_resultados", resultados)
        return self._db

    def toDIC(self):
        diccionario = {}
        for props in self._fields:
            if props[:1] != '_':
                if type(getattr(self,props)) == list:
                    lista=[]
                    for irow in getattr(self,props):
                        if isinstance(irow, str):
                           continue
                        elif isinstance(irow, int):
                            continue
                        else:
                            valor = irow.toDIC()
                            lista.append(valor)
                    diccionario[props] = lista
                else:

                    if isinstance(getattr(self, props), str):
                        diccionario[props] = getattr(self, props)
                    elif isinstance(getattr(self, props), int):
                        diccionario[props] = getattr(self, props)
                    else:
                        try:
                            data = getattr(self, props).toDIC()
                        except(Exception, ):
                            data = getattr(self, props)
                        diccionario[props] = data
        return diccionario
    def toJSON(self):
        jsonx = {}
        for props in self.__dict__:
            if props[:1] != '_':
                jsonx[props]= self.__dict__[props]
        return json.dumps(jsonx)
    def from_json(self, json_str: str):
        json_dict = json.loads(json_str)
        model_dict = self.__dict__

        # Si es windows es \ si es linux es /
        if sys.platform.startswith('win'):
            try:
                pathScript = inspect.getfile(self.__class__)
            except (Exception,):
                pathScript = '\\Models\\'
            carpetas = pathScript.split('\\Models\\')[1].split('\\')[:-1]
        else:
            try:
                pathScript = inspect.getfile(self.__class__)
            except (Exception,):
                pathScript = '/Models/'
            carpetas = pathScript.split('/Models/')[1].split('/')[:-1]
        carpetas = '.'.join(carpetas)
        # .__class__.__name__
        for key in model_dict.keys():
            # if key == "fees" or key == "fees":
              # print("fees")
            if key in json_dict:
                tipo = type(json_dict[key])
                if tipo == list or tipo == dict:
                    clase = -1
                    llave = singularize(key)  # key[:-1]
                    try:
                        n_real = model_dict[key].__class__.__name__
                        if n_real != llave:
                            try:
                                clase = self.class_for_name("Models." + n_real.capitalize(), n_real)
                            except(Exception,):
                                clase = self.class_for_name("Models." + carpetas + "." + n_real.capitalize(), n_real)
                        else:
                            clase = self.class_for_name("Models." + llave.capitalize(), llave)
                    except (Exception,):
                        try:
                            clase = self.class_for_name("Models." + carpetas + "." + llave.capitalize(), llave)
                        except (Exception,):
                            try:
                                for path in os.listdir("Models/"):
                                    isfile = os.path.isfile("Models/" + path)
                                    if type(clase) != int:
                                        break
                                    if not isfile:
                                        modulename = "Models." + path + "." + llave.capitalize()
                                        clase = self.class_for_name(modulename, llave)

                            except(Exception,):
                                try:
                                    modulename = "Models." + path + "." + key.capitalize()
                                    clase = self.class_for_name(modulename, key)
                                except (Exception,):
                                    clase = -2
                    if type(clase) != int:
                        data_op = json_dict[key]
                        lista = []
                        if type(data_op) == dict:
                            data_json = json.dumps(data_op)
                            lista = clase().from_json(data_json)
                        if type(data_op) == list:
                            for data in data_op:
                                data_json = json.dumps(data)
                                objeto = clase().from_json(data_json)
                                lista.append(objeto)
                        setattr(self, key, lista)
                    else:
                        setattr(self, key, json_dict[key])
                else:
                    setattr(self, key, json_dict[key])

        return self

    def from_json_go(self, json_str: str):
        json_dict = json.loads(json_str)
        model_dict = self.__dict__
        pathScript = inspect.getfile(self.__class__)

        # Si es windows es \ si es linux es /
        if sys.platform.startswith('win'):
            carpetas = pathScript.split('\\Models\\')[1].split('\\')[:-1]
        else:
            carpetas = pathScript.split('/Models/')[1].split('/')[:-1]
        carpetas = '.'.join(carpetas)

        for key in model_dict.keys():
            if key in json_dict:
                tipo = type(json_dict[key])
                if tipo == list or tipo == dict:
                    clase = None
                    llave = singularize(key)
                    try:
                        clase = self.class_for_name("Models." + llave.capitalize(), llave)
                    except (Exception,):
                        try:
                            clase = self.class_for_name("Models." + carpetas + "." + llave.capitalize(), llave)
                        except (Exception,):
                            pass

                    if clase is not None:
                        data_op = json_dict[key]
                        lista = []
                        if type(data_op) == dict:
                            data_json = json.dumps(data_op)
                            lista = clase().from_json(data_json)
                        if type(data_op) == list:
                            for data in data_op:
                                data_json = json.dumps(data)
                                objeto = clase().from_json(data_json)
                                lista.append(objeto)
                        setattr(self, key, lista)
                    else:
                        setattr(self, key, json_dict[key])
                else:
                    setattr(self, key, json_dict[key])

        return self
    @staticmethod
    def class_for_name(module_name, class_name):
        # load the module, will raise ImportError if module cannot be loaded
        m = importlib.import_module(module_name)
        # get the class, will raise AttributeError if class cannot be found
        c = getattr(m, class_name)
        return c

    def props(self):
        return [i for i in self.__dict__.keys() if i[:1] != '_']

    def get(self):
        return self._db.get()

    def all(self):
        return self._db.selectall(self._table)

    def save(self):
        props = vars(self)
        columnas = ""
        valores = []
        registros = []
        tvalores = ""
        # checar si se va updatear
        res = self.where({
            self._idModel: {
                "value": getattr(self, self._idModel)
            }
        })
        isUpdate=False
        if len(res.get()) == 0:
            isUpdate=False
        else:
            isUpdate=True
        for prop in props:
            if prop.startswith("_"):
                continue
            else:
                if not isUpdate:
                    if prop == self._idModel:
                        continue
                col = prop
                val = self.__getattribute__(prop)
                if columnas == "":
                    columnas = col
                    tvalores = "?"
                else:
                    columnas = columnas + "," + col
                    tvalores = tvalores + "," + "?"
                valores.append(val)
        registros.append(valores)

        if not isUpdate:
            self._db.insertar(self._table, columnas, tvalores, valores)
        else:
            self._db.updateWhere(self._table, columnas, valores,
                                 {self._idModel: {"value": getattr(self, self._idModel)}})
