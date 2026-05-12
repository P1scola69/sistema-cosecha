# En gestion_cosechas/bd.py
import pymysql
from django.conf import settings

class conexionBD:
    def __init__(self):
        # Toma los datos directamente del settings oficial
        db_data = settings.DATABASES['default']
        self.conexion = pymysql.connect(
            host=db_data['HOST'],
            user=db_data['USER'],
            password=db_data['PASSWORD'],
            database=db_data['NAME'],
            port=int(db_data['PORT']),
            cursorclass=pymysql.cursors.DictCursor
        )

    def consulta(self, sql, params=None):
        with self.conexion.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def ejecutarSQL(self, sql, params=None):
        with self.conexion.cursor() as cursor:
            cursor.execute(sql, params)
            self.conexion.commit()