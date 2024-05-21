""" DataBase.py

Este archivo es fundamental para la creación y gestión de la Base de Datos. En este script, se llevan a cabo todas las configuraciones
necesarias y se realizan las comprobaciones pertinentes para asegurar el correcto funcionamiento de la base de datos.

El uso de este código es sencillo y no requiere la instalación de ninguna librería adicional.
Python incluye de forma nativa la librería utilizada en este script: 
* sqlite3 

Este archivo puede ser importado como un módulo, lo que permite acceder y utilizar todas las funciones que contiene, 
facilitando así su integración en otros ficheros.

Bibliografía
------------
    Codingraph (2022). "Crear Base de Datos con Python". Youtube. 
    Enlace: https://youtu.be/iH7d2vHVCUk?si=k0Dhb6LJQwRh7kVc
"""

import sqlite3

class DataBase:
    """
    Clase DataBase que permite la creación y manipulación de una base de datos SQLite.
    """
    def __init__(self, nombre:str):
        """
        Constructor de la clase DataBase. Inicializa la conexión a la base de datos y crea un cursor.

        Parametros
        ---------
        nombre: str
            Representa el nombre de nuestra base de datos
        """
        self.nombre = nombre
        self.conexion = sqlite3.connect('Usuarios')  # nos conectamos a una DB
        self.cursor = self.conexion.cursor()         # creación del self.cursor

    def __str__(self):
        """
        Método especial que devuelve una representación en cadena de la instancia de DataBase.
        """
        return f""" 
Base de Datos: {self.nombre}
Usuario: {self.returnActivo()[0]}
Puntuación T1: {self.returnActivo()[2]}
Puntuación T2: {self.returnActivo()[3]}
Puntuación T3: {self.returnActivo()[4]}
Puntuación M35: {self.returnActivo()[5]}
"""
    
    def crearTabla(self, nombreTabla:str):
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
        self.cursor.execute(f'''SELECT COUNT(name) FROM SQLITE_MASTER WHERE TYPE = 'table' AND name = '{nombreTabla}' ''')

        # La tabla existe
        if self.cursor.fetchone()[0] >= 1:                           # fetchone para devolver una sola fila de la consulta
            print(f'Usando la tabla {nombreTabla} existente')   # si devuelve uno o más resultados, encontró la tabla
            return True

        # La tabla no existe
        else:
            self.cursor.execute(f'''CREATE TABLE {nombreTabla} (
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
    

    def setInactivo(self):
        """ 
        Establece todos los usuarios de la DB como inactivos
        """
        self.cursor.execute(''' UPDATE USUARIOS SET ACTIVO = 0''')
        self.conexion.commit() # lo guardamos permanentemente

    def setActivo(self, nombre:str):
        """ Establece un usuario en concreto al estado Activo

        Parámetros
        ----------
        nombre: str
            Representa la Primary Key del usuario que modificaremos
        """
        self.cursor.execute('''UPDATE USUARIOS SET ACTIVO=1 WHERE NOMBRE = '{}' '''.format(nombre))


    def returnActivo(self):
        """
        Busca el usuario activo en la sesión actual

        Devuelve
        -------
        tuple
            Devuelve la tupla: (nombre, foto, T1, T2, T3, M35)
        """
        self.cursor.execute(''' SELECT NOMBRE, foto, T1, T2, T3, M35 FROM USUARIOS WHERE ACTIVO = 1 ''')
        activo = self.cursor.fetchall()
        return activo[0] 

    def insertarUsuario(self, nombre:str, contraseña:str):
        """
        Inserta un usuario junto con una contraseña en la base de datos
        """
        try:
            self.cursor.execute('''INSERT INTO USUARIOS (NOMBRE, CONTRASEÑA, FOTO) VALUES (?,?,'T1/Imagenes/UI/Menu/foto_default.jpeg') ''', (nombre, contraseña))
            self.conexion.commit() # realizar los cambios
        except sqlite3.IntegrityError:
            print(f'\n\n--- Error en Insertar: PRIMARY KEY DUPLICADA: {nombre} ---')
                
    def buscarUsuario(self, nombre: str, contraseña: str):
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

        self.cursor.execute('''SELECT * FROM USUARIOS WHERE NOMBRE = '{}' '''.format(nombre))
        usuario_encontrado = self.cursor.fetchall() # obtenemos todos los resultados de la query

        # No se encuentra ningún usuario
        if usuario_encontrado == []:
            print(f'El usuario "{nombre}" no está registrado')
            return -1
        
        # Se encuentra un posible usuario
        else:
            self.cursor.execute("SELECT * FROM USUARIOS WHERE NOMBRE = ? AND CONTRASEÑA = ?" , (nombre, contraseña))
            usuario_encontrado = self.cursor.fetchall()
            # La contraseña no es correcta
            if usuario_encontrado == []:
                print('Contraseña incorrecta')
                return 0
            # la contraseña es correcta
            else:
                print('Inicio de sesión exitoso')
                return 1

    def añadirPuntuacion(self, PK:str, juego:str, cantidad:int):
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
        self.cursor.execute(''' UPDATE USUARIOS SET {} = {}+{} WHERE NOMBRE = '{}' '''.format(juego,juego,cantidad,PK))
        self.conexion.commit() # ejecutar los cambios

    def mostrarDatos(self):
        """
        Muestra todos los datos de todos los usuarios en la DB
        """
        self.cursor.execute('''
            SELECT * FROM USUARIOS
            ''')
        lista = []
        for filaEncontrada in self.cursor.fetchall():
            lista.append(filaEncontrada) 
        print(lista)


    # MÉTODOS SIN UTILIZAR
    def modificarAtributo(self, nombre, diccionario: dict):
        """
        Modifica un atributo del usuario indicado
        """
        valoresValidos = ['NOMBRE','CONTRASEÑA', 'FOTO', 'ACTIVO']
        for key in diccionario.keys():
            if key not in valoresValidos:
                print('Esa columna no existe')
            
            else:
                query = '''UPDATE USUARIOS SET {} = '{}' WHERE NOMBRE = '{}' '''.format(key,diccionario[key], nombre)
                try:
                    self.cursor.execute(query)
                    self.conexion.commit()
                except sqlite3.IntegrityError:
                    print('\n\n--- Error_update: PRIMARY KEY DUPLICADA:', diccionario['NOMBRE'], ' ---\n')
                except sqlite3.OperationalError:
                    print(f'\n\n--- Error_update: NO SE ENCONTRÓ LA PRIMARY KEY {nombre} ---\n')

    def eliminarUsuario(self, nombre):
        """
        Elimina el usuario indicado
        """
        try:
            self.cursor.execute('''
            DELETE FROM USUARIOS WHERE NOMBRE = '{}'
            '''.format(nombre))
            self.conexion.commit()

        except sqlite3.OperationalError:
            print(f'\n\n--- Error_delete: NO SE HA ENCONTRADO: {nombre} ---\n')


# Bases de Datos Instanciadas
db_principal = DataBase('Principal')