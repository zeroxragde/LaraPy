import uuid
import sqlite3

from dbutils.persistent_db import PersistentDB

from Libs.Config import Config
from Libs.Controlador import Controlador
from Libs.Iniciador import Iniciador
import threading


class dbController(Controlador):
    _conn = None

    def __init__(self, db=None):
        super(dbController, self).__init__()
        try:
            dbController._conn = Iniciador.pool.connection()
        except(Exception,):

            self.config = Config()
            self._dir_path = self.config.get("app", "DB_PATH")
            self._dbname = self.config.get("app", "DB_NAME")
            self._maxusage = int(self.config.get("app", "DB_MAX_USE"))
            self._id = str(uuid.uuid4())

            def create_connection():
                conn = sqlite3.connect(self._dir_path + "/" + self._dbname.lower() + '.db')
                conn.row_factory = sqlite3.Row
                return conn

            dbController._conn = PersistentDB(creator=create_connection, maxusage=self._maxusage)

        self._conn = dbController._conn
        if db is None:
            # if  dbController._conn is None:
            self._resultados = []
            # Crea la tabla solo si no existe
            cursor = self._conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS migrations(id INTEGER PRIMARY KEY AUTOINCREMENT,
                  file TEXT NOT NULL,
                  state TEXT NOT NULL)''')
            self._conn.commit()
        else:
            self._conn = db
        self._mycursor = self._conn.cursor()

    def close(self):
        self._conn.close()

    def insertar(self, tabla, campos, tvalores, valores):
        sql = "INSERT INTO " + tabla + " (" + campos + ") VALUES (" + tvalores + ")"

        try:
            cursor = self._conn.cursor()
            cursor.execute(sql, valores)
            self._conn.commit()
        except sqlite3.Error as error:
            print("Error al Insertar datos")
            self._conn.rollback()

    def updateWhere(self, tabla, campos, valores, condicion):
        cv = ', '.join([f'{campo}=?' for campo in campos.split(",")])
        query = f"UPDATE {tabla} SET {cv} WHERE "
        query_values = []

        # Construir la consulta dinámicamente
        for idx, (column, data) in enumerate(condicion.items()):
            operator = data.get('operator', '=')  # Si no se especifica un operador, por defecto es igual (=)
            value = data.get('value')
            query += f"{column} {operator} ?"
            query_values.append(value)

            # Agregar operador lógico si hay más condiciones
            if idx < len(condicion) - 1:
                logical_operator = data.get('logical_operator', 'AND')  # Si no se especifica, por defecto es AND
                query += f" {logical_operator} "

        try:
            cursor = self._conn.cursor()
            cursor.execute(query, tuple(valores + query_values))
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            print(f"Error en la actualización: {str(e)}")

    def set(self, prop, value):
        setattr(self, prop, value)

    def first(self):
        return self._resultados[0]

    def last(self):
        return self._resultados[self._resultados.count() - 1]

    def get(self):
        return self._resultados

    def where(self, table, filters):
        # Crear un cursor
        cursor = self._conn.cursor()
        cursor.row_factory = sqlite3.Row
        # Crear la consulta
        query = f"SELECT * FROM {table} WHERE "
        values = []
        # Construir la consulta dinámicamente
        for idx, (column, data) in enumerate(filters.items()):
            operator = data.get('operator', '=')  # Si no se especifica un operador, por defecto es igual (=)
            value = data.get('value')
            query += f"{column} {operator} ?"
            values.append(value)
            # Agregar operador lógico si hay más condiciones
            if idx < len(filters) - 1:
                logical_operator = data.get('logical_operator', 'AND')  # Si no se especifica, por defecto es AND
                query += f" {logical_operator} "
        # Ejecutar la consulta
        cursor.execute(query, values)
        # Obtener los resultados
        rows = cursor.fetchall()
        # Retornar los resultados
        return rows

    def existe_tabla(self, nombre_tabla):
        """
        Verifica si existe una tabla con el nombre especificado en la base de datos indicada.
        Retorna True si la tabla existe, False en caso contrario.
        """

        # Crea un cursor para ejecutar sentencias SQL
        cursor = self._conn.cursor()

        # Ejecuta una consulta para verificar si la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nombre_tabla,))

        # Obtiene el resultado de la consulta
        resultado = cursor.fetchone()

        # Cierra la conexión y el cursor
        cursor.close()

        # Retorna True si se encontró un resultado, False en caso contrario
        return resultado is not None

    def selectcomplete(self, tabla, condiciones, joins=""):
        sql = "SELECT * FROM " + tabla
        tmp = ""
        for c in condiciones:
            tmp += " " + c["campo"] + c["accion"] + "'" + c["valor"] + "' " + c["condicion"]
        join = ""
        if joins != "":
            for j in joins:
                join += j["tipo"] + " " + j["tabla"] + " ON " + j["campo"] + j["accion"] + "'" + j["valor"] + "'"
        if join != "":
            sql = sql + " " + join
        if tmp != "":
            sql = sql + " WHERE " + tmp

        self._mycursor.execute(sql)
        return self._mycursor.fetchall()

    def select(self, tabla, simbolo, campo, valor):
        sql = "SELECT * FROM " + tabla + " WHERE " + campo + simbolo + "'" + valor + "'"
        self._mycursor.execute(sql)
        return self._mycursor.fetchall()

    def selectall(self, tabla):
        sql = "SELECT * FROM " + tabla
        self._mycursor.execute(sql)
        return self._mycursor.fetchall()

    def getColType(self, tabla, col):
        sql = "SELECT DATA_TYPE " \
              "FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '" + tabla + "' AND COLUMN_NAME = '" + col + "'"
        self._mycursor.execute(sql)
        return self._mycursor.fetchall()

    def getCols(self, tabla):
        sql = "SELECT COLUMN_NAME, DATA_TYPE " \
              "FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + tabla + "' AND TABLE_SCHEMA = '" + self._dbname + "'"
        self._mycursor.execute(sql)
        return self._mycursor.fetchall()

    def getColPrimaryKey(self, tabla):
        sql = "SELECT COLUMN_NAME, DATA_TYPE " \
              "FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + tabla + \
              "' AND TABLE_SCHEMA = '" + self._dbname + \
              "' AND CONSTRAINT_TYPE='PRIMARY KEY'"
        self._mycursor.execute(sql)
        return self._mycursor.fetchall()

    def getFields(self, table):
        cursor = self._conn.cursor()
        query = f"SELECT * FROM {table} LIMIT 0"
        cursor.execute(query)
        return [description[0] for description in cursor.description]
