""" DataBase.py

Este fichero contiene la creación de la Base de Datos. Además, en este script
se desarrollan todos los ajustes y las comprobaciones necesarias.

Para utilizar el código, no es necesario instalar nada ya que Python incluye la librería sqlite3.

El fichero puede ser importado como módulo para utilizar todas las funciones.

Bibliografía
------------
    Codingraph (2022). Crear Base de Datos con Python.
    Youtube. https://youtu.be/iH7d2vHVCUk?si=k0Dhb6LJQwRh7kVc

"""
import sqlite3

conexion = sqlite3.connect('Usuarios')  # nos conectamos a una DB
cursor = conexion.cursor()              # creación del cursor


def crearTabla(nombreTabla:str):
    """ Comprueba si la tabla USUARIOS existe, si no existe crea la Tabla con todos sus atributos.

    Parámetros
    ----------
    nombreTabla: str
        Representa el nombre de la tabla que queremos comprobar

    Devuelve
    --------
    bool
        Un valor booleano que indica si la Tabla existe o no
    """
    
    # Query
    cursor.execute(f'''SELECT COUNT(name) FROM SQLITE_MASTER WHERE TYPE = 'table' AND name = '{nombreTabla}' ''')

    # La tabla existe
    if cursor.fetchone()[0] >= 1:                           # fetchone para devolver una sola fila de la consulta
        print(f'Usando la tabla {nombreTabla} existente')   # si devuelve uno o más resultados, encontró la tabla
        return True

    # La tabla no existe
    else:
        cursor.execute(f'''CREATE TABLE {nombreTabla} (
                       NOMBRE TEXT PRIMARY KEY, 
                       CONTRASEÑA TEXT, 
                       FOTO TEXT, 
                       ACTIVO BOOLEAN DEFAULT 0, 
                       T1 INT DEFAULT 0,
                       T2 INT DEFAULT 0,
                       T3 INT DEFAULT 0,
                       M35 INT DEFAULT 0)''')
        
        print(f'Tabla {nombreTabla} creada con éxito')
        return False
    
def setInactivo():
    """ 
    Establece todos los usuarios de la DB como inactivos
    """
    cursor.execute(''' UPDATE USUARIOS SET ACTIVO = 0''')
    conexion.commit() # lo guardamos permanentemente

def setActivo(nombre:str):
    """ Establece un usuario en concreto al estado Activo

    Parámetros
    ----------
    nombre: str
        Representa la Primary Key del usuario que modificaremos
    """
    cursor.execute(f'''UPDATE USUARIOS SET ACTIVO=1 WHERE NOMBRE = '{nombre}' ''')

def returnActivo():
    """
    Busca el usuario activo en la sesión actual

    Devuelve
    -------
    tuple
        Devuelve la tupla: (nombre, foto, T1, T2, T3)
    """
    cursor.execute(''' SELECT NOMBRE FROM USUARIOS WHERE ACTIVO = 1 ''')
    activo = cursor.fetchall()
    return activo[0] 

def insertarUsuario(nombre:str, contraseña:str):
    """
    Inserta un usuario junto con una contraseña en la base de datos
    """
    try:
        cursor.execute('''INSERT INTO USUARIOS (NOMBRE, CONTRASEÑA, FOTO) VALUES (?,?,'T1/Imagenes/UI/Menu/foto_default.jpeg') ''', (nombre, contraseña))
        conexion.commit() # realizar los cambios
    except sqlite3.IntegrityError:
        print(f'\n\n--- Error en Insertar: PRIMARY KEY DUPLICADA: {nombre} ---')
               
def buscarUsuario(nombre: str, contraseña: str):
    """
    Busca un usuario específico en base a un usuario y contraseña

    Parámetros
    ----------
    nombre: str
        Representa la PK del usuario
    contraseña: str
        Representa un atributo del usuario

    Devuelve: int
        Devuelve 3 tipos de resultados [-1,0,1], dependiendo de la búsqueda realizada
    """

    cursor.execute('''SELECT * FROM USUARIOS WHERE NOMBRE = '{}' '''.format(nombre))
    usuario_encontrado = cursor.fetchall() # obtenemos todos los resultados de la query

    # No se encuentra ningún usuario
    if usuario_encontrado == []:
        print(f'El usuario {nombre} no está registrado')
        return -1
    
    # Se encuentra un posible usuario
    else:
        cursor.execute("SELECT * FROM USUARIOS WHERE NOMBRE = ? AND CONTRASEÑA = ?" , (nombre, contraseña))
        usuario_encontrado = cursor.fetchall()
        # La contraseña no es correcta
        if usuario_encontrado == []:
            print('Contraseña incorrecta')
            return 0
        # la contraseña es correcta
        else:
            print('Inicio de sesión exitoso')
            return 1

def añadirPuntuacion(PK:str, juego:str, cantidad:int):
    """
    Aumenta la puntuación de un usuario

    Parámetros
    ----------
    PK: str
        Representa la Primary Key del usuario que queremos modificar
    juego: str
        Representa el juego donde se produce el cambio de puntuación
    cantidad: int
        Representa la cantidad de puntuación que añadiremos
    """
    cursor.execute(''' UPDATE USUARIOS SET {} = {}+{} WHERE NOMBRE = '{}' '''.format(juego,juego,cantidad,PK))
    conexion.commit() # ejecutar los cambios

def mostrarDatos():
    """
    Muestra todos los datos de todos los usuarios en la DB
    """
    cursor.execute('''
        SELECT * FROM USUARIOS
        ''')
    lista = []
    for filaEncontrada in cursor.fetchall():
        lista.append(filaEncontrada) 
    print(lista)


# MÉTODOS SIN UTILIZAR
def modificarAtributo(nombre, diccionario: dict):
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
