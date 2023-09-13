import json
from Repositories.UsersRepository import UsersRepository  # Asegúrate de importar la clase correcta
from Models.User import User

# Configura las credenciales de la base de datos
db_host = 'persondb.c6eunjxbobwx.us-east-2.rds.amazonaws.com'
db_user = 'admin'
db_password = '3HrRThtZBKvTbaL6xRkx'
db_name = 'Persondb'

users_repo = UsersRepository(db_host, db_user, db_password, db_name)

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

# Ruta para obtener la lista de usuarios
def obtener_usuarios(event, context):
    try:
        # Verifica la autorización antes de continuar
        if not autorizar(event):
            return {
                'statusCode': 401,
                'body': 'Acceso no autorizado'
            }

        users = users_repo.obtener_usuarios()

        return {
            'statusCode': 200,
            'body': json.dumps(users)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

# Ruta para agregar un nuevo usuario
def agregar_usuario(event, context):
    try:
        # Verifica la autorización antes de continuar
        if not autorizar(event):
            return {
                'statusCode': 401,
                'body': 'Acceso no autorizado'
            }

        if 'body' in event:
            data = json.loads(event['body'])

            if 'cedula' in data and 'nombre_usuario' in data and 'contrasena' in data:
                usuario = User(data['cedula'], data['nombre_usuario'], data['contrasena'])
                usuario = usuario.toDict()

                if users_repo.agregar_usuario(usuario['cedula'], usuario['nombre_usuario'], usuario['contrasena']):
                    usuario['message'] = 'Usuario agregado con éxito'
                    return {
                        'statusCode': 201,
                        'body': json.dumps(usuario)
                    }
                else:
                    usuario['message'] = 'Error al agregar usuario'
                    return {
                        'statusCode': 500,
                        'body': json.dumps(usuario)
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

# Ruta para obtener un usuario por ID
def obtener_usuario_por_id(event, context):
    try:
        # Verifica la autorización antes de continuar
        if not autorizar(event):
            return {
                'statusCode': 401,
                'body': 'Acceso no autorizado'
            }

        if 'pathParameters' in event and 'id' in event['pathParameters']:
            user_id = event['pathParameters']['id']
            user = users_repo.obtener_usuario_por_id(user_id)

            if user:
                return {
                    'statusCode': 200,
                    'body': json.dumps(user)
                }
            else:
                return {
                    'statusCode': 404,
                    'body': 'Usuario no encontrado'
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

# Ruta para editar un usuario por ID
def editar_usuario_por_id(event, context):
    try:
        # Verifica la autorización antes de continuar
        if not autorizar(event):
            return {
                'statusCode': 401,
                'body': 'Acceso no autorizado'
            }

        if 'pathParameters' in event and 'id' in event['pathParameters'] and 'body' in event:
            cedula = event['pathParameters']['id']
            data = json.loads(event['body'])

            if 'nombre_usuario' in data and 'contrasena' in data:
                usuario = User(cedula, data['nombre_usuario'], data['contrasena'])
                usuario = usuario.toDict()

                if users_repo.editar_usuario_por_id(cedula, usuario['nombre_usuario'], usuario['contrasena']):
                    usuario['message'] = 'Usuario actualizado con éxito'
                    return {
                        'statusCode': 200,
                        'body': json.dumps(usuario)
                    }
                else:
                    usuario['message'] = 'Error al actualizar usuario'
                    return {
                        'statusCode': 500,
                        'body': json.dumps(usuario)
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

# Ruta para eliminar un usuario por ID
def eliminar_usuario_por_id(event, context):
    try:
        # Verifica la autorización antes de continuar
        if not autorizar(event):
            return {
                'statusCode': 401,
                'body': 'Acceso no autorizado'
            }

        if 'pathParameters' in event and 'id' in event['pathParameters']:
            user_id = event['pathParameters']['id']

            if users_repo.eliminar_usuario_por_id(user_id):
                return {
                    'statusCode': 200,
                    'body': 'Usuario eliminado con éxito'
                }
            else:
                return {
                    'statusCode': 500,
                    'body': 'Error al eliminar usuario'
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
