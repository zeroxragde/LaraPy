import uuid
import sqlite3
from Controllers.dbController import dbController


class Schema(dbController):

    def __init__(self):
        self._dir_path = 'DB'
        self._dbname = "ZeroXAPI"
        self._maxusage = 20
        self._id = str(uuid.uuid4())
        conn = sqlite3.connect(self._dir_path + "/" + self._dbname.lower() + '.db')
        super(Schema, self).__init__(conn)

    def drop_table(self, table):
        # Crear un cursor para ejecutar comandos SQL
        c = self._conn.cursor()
        # Eliminar la tabla
        c.execute(f"DROP TABLE IF EXISTS {table}")
        self._conn.commit()
        return True

    def create_table(self, table, fields):
        if self.existe_tabla(table):
            return False
        # Crear un cursor para ejecutar comandos SQL
        c = self._conn.cursor()
        # Crear la tabla de usuarios
        table_definition = ''
        primary_key = ''
        for field in fields:
            if table_definition == "":
                table_definition = f'CREATE TABLE {table} (\n'
                table_definition += '  {} {}'.format(field['Campo'], field['Tipo'].value)
            else:
                table_definition += ', {} {}\n'.format(field['Campo'], field['Tipo'].value)
            if field['ISPRIMARY']:
                primary_key = field['Campo']

        if primary_key:
            table_definition += ' ,PRIMARY KEY ({}))'.format(field["Campo"])
        else:
            table_definition += ')'

        # print("Tabla:"+table_definition)
        try:
            c.execute(table_definition)
            return True
        except Exception as ex:
            print(ex)
            return False

    def add_field(self, table, field_name, field_type):
        try:
            c = self._conn.cursor()
            c.execute(f"ALTER TABLE {table} ADD COLUMN {field_name} {field_type.value}")
            return True
        except(Exception,):
            return False

    def remove_field(self, table, field_name):
        # Crear una nueva tabla con los campos que no se quieren eliminar
        c = self._conn.cursor()
        c.execute(f"PRAGMA table_info({table})")
        columns = c.fetchall()
        columns_to_keep = [col[1] for col in columns if col[1] != field_name]
        new_table_definition = f"CREATE TABLE new_{table} (\n"
        for col in columns_to_keep:
            c.execute(f"PRAGMA table_info({table})")
            col_def = c.fetchone()
            col_type = col_def[2]
            new_table_definition += f"  {col} {col_type},\n"
        new_table_definition = new_table_definition[:-2] + ")"
        c.execute(new_table_definition)

        # Copiar los datos a la nueva tabla
        c.execute(f"INSERT INTO new_{table} SELECT {','.join(columns_to_keep)} FROM {table}")

        # Borrar la tabla original y renombrar la nueva tabla
        c.execute(f"DROP TABLE {table}")
        c.execute(f"ALTER TABLE new_{table} RENAME TO {table}")

    def actualizar_estado(self, file):
        self.insertar("migrations", "file, state", "?,?", (file, "1"))

    def revisar_estado(self, file):
        datsa = self.where("migrations", {
            "file": {
                "value": file
            }
        })
        return len(datsa) > 0
