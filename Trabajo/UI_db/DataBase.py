import sqlite3

# Bibilografía: 
# Youtube. 
# Codingraph (2022): https://youtu.be/iH7d2vHVCUk?si=k0Dhb6LJQwRh7kVc

conexion = sqlite3.connect('Usuarios') # nos conectamos a una DB
cursor = conexion.cursor() # creación del cursor

def tablaExiste(nombreTabla):
    cursor.execute('''SELECT COUNT(name) FROM SQLITE_MASTER WHERE TYPE = 'table' AND name = '{}' '''.format(nombreTabla))
    if cursor.fetchone()[0] >= 1: # fetchone para devolver una sola fila de la consulta
        print('TABLA EXISTE')
        return True

    # Si no exite la tabla, la creamos
    else:
        cursor.execute('''CREATE TABLE USUARIOS (NOMBRE TEXT PRIMARY KEY, CONTRASEÑA TEXT, FOTO TEXT, ACTIVO BOOLEAN DEFAULT 0)''')
        print('TABLA CREADA')
        return False

def set_inactivo():
    cursor.execute(''' UPDATE USUARIOS SET ACTIVO = 0''')
    conexion.commit()

def set_activo(nombre):
    cursor.execute('''UPDATE USUARIOS SET ACTIVO=1 WHERE NOMBRE = '{}' '''.format(nombre))

def insertarUsuario(nombre, contraseña):
    try:
        cursor.execute(''' INSERT INTO USUARIOS (NOMBRE, CONTRASEÑA, FOTO) VALUES (?,?,'T1/Imagenes/Menu/foto_default.jpeg') ''', (nombre, contraseña))
        conexion.commit() # ejecutar los cambios
    except sqlite3.IntegrityError:
        print(f'\n\n--- Error_insert: PRIMARY KEY DUPLICADA: {nombre} ---') # raise Exception, detiene el código
                


def mostrarDatos():
    cursor.execute('''
        SELECT * FROM USUARIOS
        ''')
    lista = []
    for filaEncontrada in cursor.fetchall():
        lista.append(filaEncontrada)
    
    print(lista)


def update_db(nombre, diccionario: dict):
    valoresValidos = ['NOMBRE','CONTRASEÑA', 'FOTO', 'ACTIVO']
    for key in diccionario.keys():
        if key not in valoresValidos:
            print('Esa columna no existe')
        
        else:
            query = '''UPDATE USUARIOS SET {} = '{}' WHERE NOMBRE = '{}' '''.format(key,diccionario[key], nombre)
            try:
                cursor.execute(query)
                conexion.commit()
            except sqlite3.IntegrityError:
                print('\n\n--- Error_update: PRIMARY KEY DUPLICADA:', diccionario['NOMBRE'], ' ---\n')
            except sqlite3.OperationalError:
                print(f'\n\n--- Error_update: NO SE ENCONTRÓ LA PRIMARY KEY {nombre} ---\n')
            
def buscar_usuario(nombre: str, contraseña: str):
    cursor.execute('''SELECT * FROM USUARIOS WHERE NOMBRE = '{}' '''.format(nombre))
    usuario_encontrado = cursor.fetchall()

    # Devolveremos 3 tipos de resultados [-1,0,1], 
    # dependiendo de la búsqueda realizada

    # No se encontró ningún usuario
    if usuario_encontrado == []:
        print(f'Usuario inexistente.')
        return -1
    
    # Sí se encontró un posible usuario
    else:
        cursor.execute("SELECT * FROM USUARIOS WHERE NOMBRE = ? AND CONTRASEÑA = ?" , (nombre, contraseña))
        usuario_encontrado = cursor.fetchall()
        # El usuario encontrado no coincide con la contraseña
        if usuario_encontrado == []:
            print(f'Contraseña errónea.')
            return 0
        else:
            print('Inicio de sesión realizado')
            return 1

def eliminarUsuario(nombre):
    try:
        cursor.execute('''
        DELETE FROM USUARIOS WHERE NOMBRE = '{}'
        '''.format(nombre))
        conexion.commit()

    except sqlite3.OperationalError:
        print(f'\n\n--- Error_delete: NO SE HA ENCONTRADO: {nombre} ---\n')

#   update_db(1,{'NOMBRE': 'Pau'})
#   update_db(2,{'NOMBRE': 'David', 'CONTRASEÑA': 12345})
        
def return_activo():
    cursor.execute(''' SELECT NOMBRE, FOTO FROM USUARIOS WHERE ACTIVO = 1 ''')
    activo = cursor.fetchall()
    print('USUARIO ACTIVO: ', activo)
    return activo[0]