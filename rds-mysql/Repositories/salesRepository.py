import pymysql

class SalesRepository:
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
            CREATE TABLE IF NOT EXISTS ventas (
                venta_id INT AUTO_INCREMENT PRIMARY KEY,
                cliente_cedula VARCHAR(20),
                total DECIMAL(10, 2),
                FOREIGN KEY (cliente_cedula) REFERENCES usuarios(cedula)
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

    def agregar_venta(self, cliente_cedula, total):
        try:
            insert_sale_query = "INSERT INTO ventas (cliente_cedula, total) VALUES (%s, %s)"

            with self.conn.cursor() as cursor:
                cursor.execute(insert_sale_query, (cliente_cedula, total))
                self.conn.commit()
                
            venta_id = cursor.lastrowid
            
            self.cerrar_conexion()
            return {
                'venta_id': venta_id,
                'cliente_cedula': cliente_cedula,
                'total': total
            }

        except Exception as e:
            raise e

    def obtener_ventas(self):
        try:
            select_sales_query = "SELECT * FROM ventas"

            with self.conn.cursor() as cursor:
                cursor.execute(select_sales_query)
                sales = cursor.fetchall()

            for sale in sales:
                sale['total'] = float(sale['total'])

            return sales
        except Exception as e:
            raise e

    def obtener_venta_por_id(self, venta_id):
        try:
            select_sale_query = "SELECT * FROM ventas WHERE venta_id = %s"

            with self.conn.cursor() as cursor:
                cursor.execute(select_sale_query, (venta_id,))
                sale = cursor.fetchone()

            self.cerrar_conexion()

            if sale:
                sale['total'] = float(sale['total'])
                return sale
            else:
                return None

        except Exception as e:
            raise e

    def editar_venta_por_id(self, venta_id, total):
        try:
            update_sale_query = "UPDATE ventas SET total = %s WHERE venta_id = %s"

            with self.conn.cursor() as cursor:
                cursor.execute(update_sale_query, (total, venta_id))
                self.conn.commit()
                self.cerrar_conexion()

            return True
        except Exception as e:
            raise e

    def eliminar_venta_por_id(self, venta_id):
        try:
            delete_sale_query = "DELETE FROM ventas WHERE venta_id = %s"

            with self.conn.cursor() as cursor:
                cursor.execute(delete_sale_query, (venta_id,))
                self.conn.commit()
                self.cerrar_conexion()

            return True
        except Exception as e:
            raise e