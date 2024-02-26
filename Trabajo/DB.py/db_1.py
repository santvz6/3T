import sqlite3

conexion = sqlite3.connect('Usuarios.db') # nos conectamos a una DB
cursor = conexion.cursor() # creación del cursor

def tablaExiste(nombreTabla):
    cursor.execute('''SELECT COUNT(name) FROM SQLITE_MASTER WHERE TYPE = 'table' AND name = '{}' '''.format(nombreTabla))
    if cursor.fetchone()[0] >= 1: # fetchone para devolver una sola fila de la consulta
        return True

    # Si no exite la tabla, la creamos
    else:
        cursor.execute('''CREATE TABLE USUARIOS (NOMBRE TEXT PRIMARY KEY, CONTRASEÑA INTEGER)''')
        return False


def insertarUsuario(nombre, contraseña):
    try:
        cursor.execute(''' INSERT INTO USUARIOS (NOMBRE, CONTRASEÑA) VALUES (?,?) ''', (nombre, contraseña))
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
    valoresValidos = ['NOMBRE','CONTRASEÑA']
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
        DELETE FROM USUARIOS WHERE NOMBRE = {}
        '''.format(nombre))
        conexion.commit()

    except sqlite3.OperationalError:
        print(f'\n\n--- Error_delete: NO SE HA ENCONTRADO: {nombre} ---\n')






# Sintaxis de las funciones:
tablaExiste('USUARIOS')
insertarUsuario('Luis',123)
insertarUsuario('Pepe', 1234)
insertarUsuario('Pepeluis', 1234)

eliminarUsuario('Juan')

update_db('Miguel',{'NOMBRE':'Jose'})
mostrarDatos()


#   update_db(1,{'NOMBRE': 'Pau'})
#   update_db(2,{'NOMBRE': 'David', 'CONTRASEÑA': 12345})
