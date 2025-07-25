#Tiene toda la logica para acceder a la base de datos, tiene funciones que adentro tiene armadas las consultas
from __mysql__db import * #importo las funciones que acceden a la base de datos
from flask import request, session, redirect, render_template #importo session para el manejo de sesion


#para obtener los datos del cliente/administrador que inicio sesion
def obtenerUsuarioXEmailPass(result,email,password):
    '''### Información:
       Obtiene todos los campos de la tabla usuario a partir de la clave 'email' y del 'password'.
       Carga la información obtenida de la BD en el dict 'result'
       Recibe 'result' in diccionario donde se almacena la respuesta de la consulta
       Recibe 'email' que es el mail si se utiliza como clave en la búsqueda
       Recibe 'password' que se utiliza en la consulta. (Para validadar al usuario)
       Retorna:
        True cuando se obtiene un registro de u usuario a partir del 'email' y el 'pass.
        False caso contrario.
    '''
    res=False
    sSql="""SELECT id, nombre,apellido,usuario,email,pass
    FROM usuario WHERE email=%s and pass=%s;"""
    val=(email,password)
    fila=selectDB(BASE,sSql,val)
    if fila!=[]:
        res=True
        result['id']=fila[0][0]
        result['nombre']=fila[0][1]
        result['apellido']=fila[0][2]
        result['usuario']=fila[0][3] 
        result['email']=fila[0][4]
        result['pass']=fila[0][5]
    return res


#para mostrar las entradas de algun cliente
def obtenerEntradasClientePorID(param):
    res=False
    sSql="""select reserva.id as id_reserva, evento.nombre as 'Evento',evento.descripcion as 'Descripcion', estado.estado as 'Estado', tipo_entrada.tipo as 'Tipo de entrada',evento.fecha_hora as 'Fecha', tipo_evento.tipo as 'Tipo de evento', reserva.cantidad_entradas as 'Cantidad' from reserva
            inner join evento on evento.id=reserva.id_evento
            inner join cliente on cliente.id=reserva.id_cliente
            inner join estado on estado.id=reserva.id_estado
            inner join tipo_entrada on tipo_entrada.id=reserva.id_tipo_entrada
            inner join tipo_evento on tipo_evento.id=evento.id_tipo_evento
            where id_cliente=%s"""
    val=(session['id_usuario'],)
    datos=[]
    datos=selectDB(BASE,sSql,val,True)
    if(datos!=[]):
        tu_titulos=datos[0]
        li_datos=datos[1:]
        di_datos={}
        for fila in li_datos:
          di_datos["tbl_row_"+str(fila[0])]=fila

          param["page-title"]=""
          param["page-header"]= ""        
          param['table']={
            "title_table":"",
            "description_table":"",

            "colIni":1, # Sirve para mostrar desde col 0 (incluye id), desde 1 no lo incluye al id
                    # siempre color el id en la primer posición (la 0) de la lista
                    # poner a izquierda columnas que no quiere visualizar
                    
            "titles":{"id":"tbl_row_tit","cols":tu_titulos},
            "data":li_datos,   
            }
    else:
        tu_titulos=()
        li_datos=[]
        di_datos={}
        for fila in li_datos:
          di_datos["tbl_row_"+str(fila[0])]=fila

          param["page-title"]=""
          param["page-header"]= ""        
          param['table']={
            "title_table":"",
            "description_table":"",

            "colIni":1, # Sirve para mostrar desde col 0 (incluye id), desde 1 no lo incluye al id
                    # siempre color el id en la primer posición (la 0) de la lista
                    # poner a izquierda columnas que no quiere visualizar
                    
            "titles":{"id":"tbl_row_tit","cols":tu_titulos},
            "data":li_datos,   
          }


#para mostrar los datos de la cuenta que este activa
def obtenerDatosDeLaCuenta(param):
    res=False
    sSql="""select cliente.id as id_cliente, cliente.nombre as 'Nombre', cliente.apellido as 'Apellido', cliente.usuario as 'Usuario', cliente.mail as 'Mail' from cliente
        where id=%s""" 
    val=(session['id_usuario'],)
    datos=[]
    datos=selectDB(BASE,sSql,val,True) #datos va a ser una lista de tuplas
    if(datos!=[]):
        tu_titulos=datos[0] #guardo ej tu_titulos la tupla con los titulos
        li_datos=datos[1:] #guardo en li_datos una lista de tuplas (cada tupla es una fila de la tabla de la bd)
        di_datos={} #inicializo el diccionario vacio
        for fila in li_datos: #para cada fila de datos
          di_datos["tbl_row_"+str(fila[0])]=fila #guardo la fila d datos en el dic q tiene al id de la fila en su clave

          param["page-title"]=""
          param["page-header"]= ""        
          param['table']={
            "title_table":"",
            "description_table":"",

            "colIni":1, # Sirve para mostrar desde col 0 (incluye id), desde 1 no lo incluye al id
                    # siempre color el id en la primer posición (la 0) de la lista
                    # poner a izquierda columnas que no quiere visualizar
                    
            "titles":{"id":"tbl_row_tit","cols":tu_titulos},
            "data":li_datos,   
            }
    else:
        tu_titulos=()
        li_datos=[]
        di_datos={}
        for fila in li_datos:
          di_datos["tbl_row_"+str(fila[0])]=fila

          param["page-title"]=""
          param["page-header"]= ""        
          param['table']={
            "title_table":"",
            "description_table":"",

            "colIni":1, # Sirve para mostrar desde col 0 (incluye id), desde 1 no lo incluye al id
                    # siempre color el id en la primer posición (la 0) de la lista
                    # poner a izquierda columnas que no quiere visualizar
                    
            "titles":{"id":"tbl_row_tit","cols":tu_titulos},
            "data":li_datos,   
          }


#para mostrar las entradas que se vendieron
def obtenerDatosDeLasVentas(param):
    res=False
    sSql="""select reserva.id as id_reserva, evento.nombre as 'Evento', cliente.usuario as 'Cliente (usuario)', estado.estado as 'Estado', tipo_entrada.tipo as 'Tipo de entrada', reserva.cantidad_entradas as 'Cantidad vendida' from reserva
          inner join evento on evento.id=reserva.id_evento
          inner join cliente on cliente.id=reserva.id_cliente
          inner join estado on estado.id=reserva.id_estado
        inner join tipo_entrada on tipo_entrada.id=reserva.id_tipo_entrada;
        """
    val=()
    datos=[]
    datos=selectDB(BASE,sSql,val,True)
    if(datos!=[]):
        tu_titulos=datos[0]
        li_datos=datos[1:]
        di_datos={}
        for fila in li_datos:
          di_datos["tbl_row_"+str(fila[0])]=fila

          param["page-title"]=""
          param["page-header"]= ""        
          param['table']={
            "title_table":"",
            "description_table":"",

            "colIni":1, # Sirve para mostrar desde col 0 (incluye id), desde 1 no lo incluye al id
                    # siempre color el id en la primer posición (la 0) de la lista
                    # poner a izquierda columnas que no quiere visualizar
                    
            "titles":{"id":"tbl_row_tit","cols":tu_titulos},
            "data":li_datos,   
            }
    else:
        tu_titulos=()
        li_datos=[]
        di_datos={}
        for fila in li_datos:
          di_datos["tbl_row_"+str(fila[0])]=fila

          param["page-title"]=""
          param["page-header"]= ""        
          param['table']={
            "title_table":"",
            "description_table":"",

            "colIni":1, # Sirve para mostrar desde col 0 (incluye id), desde 1 no lo incluye al id
                    # siempre color el id en la primer posición (la 0) de la lista
                    # poner a izquierda columnas que no quiere visualizar
                    
            "titles":{"id":"tbl_row_tit","cols":tu_titulos},
            "data":li_datos,   
          }

#para insertar en la tabla 'reserva' una nueva compra
def insertarReserva(dicDatos):
  sQuery=""" 
    INSERT INTO reserva
    (id,id_evento,id_cliente,id_estado,id_tipo_entrada,cantidad_entradas)
    VALUES
    (%s,%s, %s, %s, %s,%s);
  """

  val=(None,dicDatos.get("id_evento"),dicDatos.get("id_cliente"), dicDatos.get("id_estado"), dicDatos.get("id_tipo_entrada"), dicDatos.get("cantidad_entradas"))
  resul_insert=insertDB(BASE,sQuery,val)


#para insertar en la tabla 'cliente' un nuevo registro
def insertarRegistro(dicDatos):
  sQuery=""" 
    INSERT INTO cliente
    (id,nombre,apellido,usuario,mail,contrasenia)
    VALUES
    (%s,%s, %s, %s, %s,%s);
  """
 
  #val=(None,"lisandro","gaetmank","lgaetmank","lgaetmank@gmail.com","Lisandro123*")
  val=(None,dicDatos.get("nombre"),dicDatos.get("apellido"), dicDatos.get("usuario"), dicDatos.get("mail"), dicDatos.get("contrasenia"))
  
  try:
        resul_insert = insertDB(BASE, sQuery, val)
  except:
        resul_insert=0
  return resul_insert


#para insertar en la tabla 'evento' un nuevo evento
def insertarEvento(dicDatos):
   
  sQuery=""" 
    INSERT INTO evento
    (id,nombre,img,fecha_hora,descripcion,precio_campo,precio_vip,precio_platea,cant_entradas,id_tipo_evento,ubicacion)
    VALUES
    (%s,%s, %s, %s, %s,%s,%s,%s,%s,%s,%s);
  """
  val=(None,dicDatos.get("nombre"),dicDatos.get("img"),dicDatos.get("fecha-hora"), dicDatos.get("descripcion"), dicDatos.get("precio_campo"),dicDatos.get("precio_vip"),dicDatos.get("precio_platea"),dicDatos.get("cant_entradas"),dicDatos.get("id_tipo_evento"),dicDatos.get("ubicacion"))
  resul_insert=insertDB(BASE,sQuery,val)
  return resul_insert

