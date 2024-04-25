import sqlite3

# Bibilografía: 
# Youtube. 
# Codingraph (2022): https://youtu.be/iH7d2vHVCUk?si=k0Dhb6LJQwRh7kVc

conexion = sqlite3.connect('Usuarios')  # nos conectamos a una DB
cursor = conexion.cursor()  # creación del cursor


############# CRECIÓN TABLA USUARIOS #############
def tablaExiste(nombreTabla):

    # Para ejecutar una query:
    cursor.execute('''SELECT COUNT(name) FROM SQLITE_MASTER WHERE TYPE = 'table' AND name = '{}' '''.format(nombreTabla))

    if cursor.fetchone()[0] >= 1:           # fetchone para devolver una sola fila de la consulta
        print('La tabla USUARIOS existe')   # si devuelve una o más resultados, encontró la tabla
        return True

    # Si no exite la tabla, la creamos
    else:
        cursor.execute('''CREATE TABLE USUARIOS (
                       NOMBRE TEXT PRIMARY KEY, 
                       CONTRASEÑA TEXT, 
                       FOTO TEXT, 
                       ACTIVO BOOLEAN DEFAULT 0, 
                       T1 INT DEFAULT 0,
                       T2 INT DEFAULT 0,
                       T3 INT DEFAULT 0)''')
        
        print('TABLA CREADA')
        return False
    
############# ACTIVO / INACTIVO  #############
def set_inactivo():
    cursor.execute(''' UPDATE USUARIOS SET ACTIVO = 0''')
    conexion.commit() # lo guardamos permanentemente

def set_activo(nombre):
    cursor.execute('''UPDATE USUARIOS SET ACTIVO=1 WHERE NOMBRE = '{}' '''.format(nombre))


############# CREAR USUARIO #############
def insertarUsuario(nombre, contraseña):
    try:
        cursor.execute('''INSERT INTO USUARIOS (NOMBRE, CONTRASEÑA, FOTO) VALUES (?,?,'T1/Imagenes/UI/Menu/foto_default.jpeg') ''', (nombre, contraseña))
        conexion.commit() # ejecutar los cambios
    except sqlite3.IntegrityError:
        print(f'\n\n--- Error_insert: PRIMARY KEY DUPLICADA: {nombre} ---') # raise Exception, detiene el código

############# INICIAR SESIÓN #############                
def buscar_usuario(nombre: str, contraseña: str):
    cursor.execute('''SELECT * FROM USUARIOS WHERE NOMBRE = '{}' '''.format(nombre))
    usuario_encontrado = cursor.fetchall() # obtenemos todos los resultados de la query

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
        # Todos los datos son correctos
        else:
            print('Inicio de sesión realizado')
            return 1
        
############# OPCIONES DE MODIFICACIÓN DEL USUARIO #############  
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


def eliminarUsuario(nombre):
    try:
        cursor.execute('''
        DELETE FROM USUARIOS WHERE NOMBRE = '{}'
        '''.format(nombre))
        conexion.commit()

    except sqlite3.OperationalError:
        print(f'\n\n--- Error_delete: NO SE HA ENCONTRADO: {nombre} ---\n')
        

############# Datos del Usuario Activo #############  
def return_activo():
    cursor.execute(''' SELECT NOMBRE, FOTO, T1, T2, T3 FROM USUARIOS WHERE ACTIVO = 1 ''')
    activo = cursor.fetchall()
    print('USUARIO ACTIVO: ', activo)
    return activo[0] # devuelve una tupla (nombre, foto, T1, T2, T3)

def puntuar_db(PK:str, juego:str, cantidad:int):
    cursor.execute(''' UPDATE USUARIOS SET {} = {}+{} WHERE NOMBRE = '{}' '''.format(juego,juego,cantidad,PK))
    conexion.commit() # ejecutar los cambios


############# INFORMACIÓN PARA EL DESARROLLADOR #############
def mostrarDatos():
    cursor.execute('''
        SELECT * FROM USUARIOS
        ''')
    lista = []
    for filaEncontrada in cursor.fetchall():
        lista.append(filaEncontrada)
    
    print(lista)