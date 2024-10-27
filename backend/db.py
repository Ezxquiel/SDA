import pymysql

class SimpleDatabase:
    def __init__(self, host, user, password, database):
        """Inicializa con los datos de conexión."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def _connect(self):
        """Crea y retorna la conexión a la base de datos."""
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def send_data(self, query, params=None):
        """Ejecuta consultas que envían datos (INSERT, UPDATE, DELETE)."""
        try:
            connection = self._connect()
            with connection.cursor() as cursor:
                cursor.execute(query, params)
            connection.commit()
            print("Datos enviados con éxito.")
        except pymysql.MySQLError as e:
            print("Error al enviar datos:", e)
        finally:
            connection.close()

    def fetch_data(self, query, params=None):
        """Ejecuta una consulta SELECT y retorna los resultados."""
        try:
            connection = self._connect()
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print("Error al obtener datos:", e)
            return None
        finally:
            connection.close()
