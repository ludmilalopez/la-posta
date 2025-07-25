#este archivo es el que se 'comunica' con la base de datos

import mysql.connector #importo la  librería de Python utilizada para interactuar con bases de datos MySQL

def conectarBD(configDB=None):
    ''' # Establecer una conexión con el servidor MySQL
        # retorna la conexión
    '''
    mydb=None
    if configDB!=None:
        try:        
            mydb = mysql.connector.connect(
                    host=configDB.get("host"),
                    user=configDB.get("user"),
                    password=configDB.get("pass"),
                    database=configDB.get("dbname")
                   )
        except mysql.connector.Error as e:
            print("ERROR ->",e)        
    return mydb

def cerrarBD(mydb):
    ''' # Realiza el cierra un conexión a una base de datos.
        # recibe 'mydb' una conexion a una base de datos
    '''
    if mydb!=None:
        mydb.close()

def consultarDB(mydb,sQuery="",val=None,title=False):
    ''' # Realiza la consulta 'SELECT'
        # recibe 'mydb' una conexion a una base de datos
        # recibe 'sQuery' la cadena con la consulta sql.
        # recibe 'val' valores separados anti sql injection
        # recibe 'title' booleana
        # retorna una 'list' con el resultado de la consulta
        #     cada fila de la 'list' es una tupla
        #     Si 'title' es True, entonces agrega a la lista
        #     los títulos de las columnas.
    '''
    myresult=None
    try:
        if mydb!=None:
            mycursor = mydb.cursor() #genero un cursor.

            if val==None:
                mycursor.execute(sQuery) #si no le paso val, se ejecuta esta linea
            else:
                mycursor.execute(sQuery,val) #si le paso val, se ejecuta esta linea
            #con execute ejecuto la consulta, pasando el texto. eso hace que el select viaje hasta la base de datos, realice la consulta, y me la retorne en la variable que es mi cursor

            myresult = mycursor.fetchall() #extraigo la información en el formato que tiene internamente en el cursor y me lo transforma en una lista de tuplas

            # Para obtener los nombres de las columnas
            if title:
                myresult.insert(0,mycursor.column_names)

    except mysql.connector.Error as e:
        print("ERROR ->",e) #se imprime el error

    return myresult #me devuelve una lista de tuplas, en donde cada tupla es una fila de la tabla

def ejecutarDB(mydb,sQuery="",val=None):
    ''' # Realiza las consultas 'INSERT' 'UPDATE' 'DELETE'
        # recibe 'mydb' una conexion a una base de datos
        # recibe 'sQuery' la cadena con la consulta (query) sql.
        # recibe 'val' valores separados anti sql injection
        # retorna la cantidad de filas afectadas con la query.
    '''
    res=None

    try: #lo hago porque puedo tener mal armado el string de consulta, la base de datos no disponible, u otros errores.

        mycursor = mydb.cursor() #genero un cursor.

        if val==None:
            mycursor.execute(sQuery) #si no le paso val, se ejecuta esta linea
        else:
            mycursor.execute(sQuery,val) #si le paso val, se ejecuta esta linea
        #ejecuto la consulta que le paso. si lo hizo correctamente, pasa a la siguiente instrucción

        mydb.commit() # commit() Hace efectiva la operación que realice en la base de datos.

        res=mycursor.rowcount        # filas afectadas

    except mysql.connector.Error as e:
        mydb.rollback() # rollback() Vuelve hacia atrás las operaciones que se realizaron. 
        #se vuelve al estado original, al que estaba antes de mandar el insert, update o delete.

        print("ERROR ->",e) #se imprime el error

    return res # Devuelve un número entero, que es la cantidad de filas afectadas por la consulta
    
############################################################################

############################################################################
## - - - FUNCIONES SECUNDARIAS - - - - - - - - - - - - - - - - - - - - - -
## UTILIZA LAS FUNCIONES PRINCIPALES PARA ACCEDER A LA BASE DE DATOS
##  
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def selectDB(configDB=None,sql="",val=None,title=False):
    ''' ########## SELECT
        # recibe 'configDB' un 'dict' con los parámetros de conexion
        # recibe 'sql' una cadena con la consulta sql
        # recibe 'val' valores separados anti sql injection
        # recibe 'title' booleana
        # retorna una 'list' con el resultado de la consulta
        #     cada fila de la 'list' es una 'tuple'
        #     Si 'title' es True, entonces agrega a la lista
        #     los títulos de las columnas.
    '''
    resQuery=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        resQuery=consultarDB(mydb,sQuery=sql,val=val,title=title)
        cerrarBD(mydb)
    return resQuery

def insertDB(configDB=None,sql="",val=None):
    ''' ########## INSERT
        # recibe 'configDB' un 'dict' con los parámetros de conexion
        # recibe 'sql' una cadena con la consulta sql
        # recibe 'val' valores separados anti sql injection
    '''
    res=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        res=ejecutarDB(mydb,sQuery=sql,val=val)
        cerrarBD(mydb)
    return res

def updateDB(configDB=None,sql="",val=None):
    ''' ########## UPDATE
        # recibe 'configDB' un 'dict' con los parámetros de conexion
        # recibe 'sql' una cadena con la consulta sql
        # recibe 'val' valores separados anti sql injection
    '''
    res=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        res=ejecutarDB(mydb,sQuery=sql,val=val)
        cerrarBD(mydb)
    return res

def deleteDB(configDB=None,sql="",val=None):
    ''' ########## DELETE
        # recibe 'configDB' un 'dict' con los parámetros de conexion
        # recibe 'sql' una cadena con la consulta sql
        # recibe 'val' valores separados anti sql injection
    '''
    res=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        res=ejecutarDB(mydb,sQuery=sql,val=val)
        cerrarBD(mydb)
    return res

############################################################################ 


########################################################################## 
## CONFIGURACION DE LA CONEXION A LA BASE DE DATOS
## DICCIONARIO con los datos de la conexión
## Nota: Sería una buena práctica colocar este diccionario con los datos 
##       de la conexion en el archivo de configuración de la app
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

BASE={ "host":"localhost",
        "user":"root",
        "pass":"",
        "dbname":"laposta"}

############################################################################

#establece la conexión con la base de datos
def IniciarConexion():
    return mysql.connector.connect(host = "localhost",user="root",password="",database="laposta")


