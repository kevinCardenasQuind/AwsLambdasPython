import json
from Repositories.salesRepository import SalesRepository  # Asegúrate de importar la clase correcta

# Configura las credenciales de la base de datos
db_host = 'persondb.c6eunjxbobwx.us-east-2.rds.amazonaws.com'
db_user = 'admin'
db_password = '3HrRThtZBKvTbaL6xRkx'
db_name = 'Persondb'

sales_repo = SalesRepository(db_host, db_user, db_password, db_name)

# Función para verificar y validar el token bearer
def verificar_token_bearer(authorization_header):
    if authorization_header.startswith('Bearer '):
        token = authorization_header.split(' ')[1]

        if token == '0c6823a7b08a47f1daa8e3c1744a95a359b5df404db9de00f0245bb720da1620':
            return True
        else:
            return False
    else:
        return False

# Función de autorización para todas las rutas
def autorizar(event):
    if 'headers' in event and 'Authorization' in event['headers']:
        authorization_header = event['headers']['Authorization']

        # Verifica el token bearer utilizando la función de verificación
        return verificar_token_bearer(authorization_header)
    else:
        return False

# Ruta para obtener la lista de ventas
def obtener_ventas(event, context):
    try:
        # Verifica la autorización antes de continuar
        if not autorizar(event):
            return {
                'statusCode': 401,
                'body': 'Acceso no autorizado'
            }

        ventas = sales_repo.obtener_ventas()

        return {
            'statusCode': 200,
            'body': json.dumps(ventas)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

# Ruta para agregar una nueva venta
def agregar_venta(event, context):
    try:
        # Verifica la autorización antes de continuar
        if not autorizar(event):
            return {
                'statusCode': 401,
                'body': 'Acceso no autorizado'
            }

        if 'body' in event:
            data = json.loads(event['body'])

            if 'cliente_cedula' in data and 'total' in data:
                cliente_cedula = data['cliente_cedula']
                total = data['total']

                venta = sales_repo.agregar_venta(cliente_cedula, total)

                if venta:
                    return {
                        'statusCode': 201,
                        'body': json.dumps(venta)
                    }
                else:
                    return {
                        'statusCode': 500,
                        'body': 'Error al agregar la venta'
                    }
            else:
                return {
                    'statusCode': 400,
                    'body': 'Falta información en la solicitud'
                }
        else:
            return {
                'statusCode': 400,
                'body': 'Solicitud no válida'
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

# Ruta para obtener una venta por ID
def obtener_venta_por_id(event, context):
    try:
        # Verifica la autorización antes de continuar
        if not autorizar(event):
            return {
                'statusCode': 401,
                'body': 'Acceso no autorizado'
            }

        if 'pathParameters' in event and 'venta_id' in event['pathParameters']:
            venta_id = event['pathParameters']['venta_id']
            venta = sales_repo.obtener_venta_por_id(venta_id)

            if venta:
                return {
                    'statusCode': 200,
                    'body': json.dumps(venta)
                }
            else:
                return {
                    'statusCode': 404,
                    'body': 'Venta no encontrada'
                }
        else:
            return {
                'statusCode': 400,
                'body': 'Solicitud no válida'
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

# Ruta para editar una venta por ID
def editar_venta_por_id(event, context):
    try:
        # Verifica la autorización antes de continuar
        if not autorizar(event):
            return {
                'statusCode': 401,
                'body': 'Acceso no autorizado'
            }

        if 'pathParameters' in event and 'venta_id' in event['pathParameters'] and 'body' in event:
            venta_id = event['pathParameters']['venta_id']
            data = json.loads(event['body'])

            if 'total' in data:
                total = data['total']

                if sales_repo.editar_venta_por_id(venta_id, total):
                    return {
                        'statusCode': 200,
                        'body': 'Venta actualizada con éxito'
                    }
                else:
                    return {
                        'statusCode': 500,
                        'body': 'Error al actualizar la venta'
                    }
            else:
                return {
                    'statusCode': 400,
                    'body': 'Falta información en la solicitud'
                }
        else:
            return {
                'statusCode': 400,
                'body': 'Solicitud no válida'
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

# Ruta para eliminar una venta por ID
def eliminar_venta_por_id(event, context):
    try:
        # Verifica la autorización antes de continuar
        if not autorizar(event):
            return {
                'statusCode': 401,
                'body': 'Acceso no autorizado'
            }

        if 'pathParameters' in event and 'venta_id' in event['pathParameters']:
            venta_id = event['pathParameters']['venta_id']

            if sales_repo.eliminar_venta_por_id(venta_id):
                return {
                    'statusCode': 200,
                    'body': 'Venta eliminada con éxito'
                }
            else:
                return {
                    'statusCode': 500,
                    'body': 'Error al eliminar la venta'
                }
        else:
            return {
                'statusCode': 400,
                'body': 'Solicitud no válida'
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
