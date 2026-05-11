from django.conf import settings
import pymysql

class conexionBD:
    def conectar(self):
        return pymysql.connect(
            host=settings.DB_CONFIG['HOST'],
            user=settings.DB_CONFIG['USER'],
            password=settings.DB_CONFIG['PASSWORD'],
            database=settings.DB_CONFIG['NAME'],
            port=settings.DB_CONFIG['PORT'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )


    def ejecutarSQL(self, sql, params=None):
        conexion = self.conectar()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(sql, params)
                conexion.commit()
        finally:
            conexion.close()


    def consulta(self, sql, params=None):
        conexion = self.conectar()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        finally:
            conexion.close()