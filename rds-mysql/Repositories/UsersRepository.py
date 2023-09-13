import pymysql

class UsersRepository:
    def __init__(self, db_host, db_user, db_password, db_name):
        self.conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            db=db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.ensure_table_exists()

    def ensure_table_exists(self):
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS usuarios (
                cedula VARCHAR(20) PRIMARY KEY,
                nombre_usuario VARCHAR(255) NOT NULL,
                contrasena VARCHAR(255) NOT NULL
            )
            """
            with self.conn.cursor() as cursor:
                cursor.execute(create_table_query)
                self.conn.commit()
        except Exception as e:
            raise e
        
    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()

    def obtener_usuarios(self):
        try:
            select_users_query = "SELECT * FROM usuarios"

            with self.conn.cursor() as cursor:
                cursor.execute(select_users_query)
                users = cursor.fetchall()

            return users
        except Exception as e:
            raise e

    def agregar_usuario(self, cedula, nombre_usuario, contrasena):
        try:
            insert_user_query = "INSERT INTO usuarios (cedula, nombre_usuario, contrasena) VALUES (%s, %s, %s)"

            with self.conn.cursor() as cursor:
                cursor.execute(insert_user_query, (cedula, nombre_usuario, contrasena))
                self.conn.commit()
                self.cerrar_conexion()

            return True
        except Exception as e:
            raise e

    def obtener_usuario_por_id(self, user_id):
        try:
            select_user_query = "SELECT * FROM usuarios WHERE cedula = %s"

            with self.conn.cursor() as cursor:
                cursor.execute(select_user_query, (user_id,))
                user = cursor.fetchone()

            self.cerrar_conexion()

            return user
        except Exception as e:
            raise e

    def editar_usuario_por_id(self, user_id, nombre_usuario, contrasena):
        try:
            update_user_query = "UPDATE usuarios SET nombre_usuario = %s, contrasena = %s WHERE cedula = %s"

            with self.conn.cursor() as cursor:
                cursor.execute(update_user_query, (nombre_usuario, contrasena, user_id))
                self.conn.commit()
                self.cerrar_conexion()

            return True
        except Exception as e:
            raise e

    def eliminar_usuario_por_id(self, user_id):
        try:
            delete_user_query = "DELETE FROM usuarios WHERE cedula = %s"

            with self.conn.cursor() as cursor:
                cursor.execute(delete_user_query, (user_id,))
                self.conn.commit()
                self.cerrar_conexion()

            return True
        except Exception as e:
            raise e