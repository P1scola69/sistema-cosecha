from django.db import connection

class conexionBD:
    def consulta(self, sql, params=None):
        """Ejecuta un SELECT y devuelve una lista de diccionarios."""
        with connection.cursor() as cursor:
            cursor.execute(sql, params or [])

            columnas = [col[0] for col in cursor.description]
            return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    def ejecutarSQL(self, sql, params=None):
        """Ejecuta INSERT, UPDATE o DELETE."""
        with connection.cursor() as cursor:
            cursor.execute(sql, params or [])
