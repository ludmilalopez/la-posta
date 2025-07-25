#Contiene toda la logica que administra el sistema, proceso logico del sistema, funciones para calculos
#buscar pagina en html o buscar cosas en el model,etc.

'''### info:
     CONTROL 

    Dependencias:
        pip install uuid

    Referencias:
        https://pypi.org/project/uuid/
        https://docs.python.org/3/library/uuid.html
    
'''
from flask import request, session,redirect,render_template
# request: gestiona las solicitudes http recibidas
# session: para el manejo de sesion
# redirect: redirigir a otras rutas 
# render_template: para renderizar las plantillas con jinja y crear paginas dinamicas
from datetime import datetime 
from model import * #importo las funciones de model (tienen las consultas)
from werkzeug.utils import secure_filename #Libreria de ciberseguridad
import os  # Gestiona acceso al sistema operativo local
from uuid import uuid4 #Crea nombres de archivos unicos e irrepetibles
from appConfig import config  # Archivo de configuracion de la aplicación

##########################################################################
# + + I N I C I O + + MANEJO DE  REQUEST + + + + + + + + + + + + + + + + +
##########################################################################
#Toma la informacion del formulario al enviar el submit y te lo convierte a dic

def getRequest(diResult):
    if request.method=='POST':
        for name in request.form.to_dict().keys():
            li=request.form.getlist(name)
            if len(li)>1:
                diResult[name]=request.form.getlist(name)
            elif len(li)==1:
                diResult[name]=li[0]
            else:
                diResult[name]=""
    elif request.method=='GET':  
        for name in request.args.to_dict().keys():
            li=request.args.getlist(name)
            if len(li)>1:
                diResult[name]=request.args.getlist(name)
            elif len(li)==1:
                diResult[name]=li[0]
            else:
                diResult[name]=""    
 
##########################################################################
# - - F I N - - MANEJO DE  REQUEST - - - - - - - - - - - - - - - - - - - -
##########################################################################

##########################################################################
# + + I N I C I O + + MANEJO DE  SUBIDA DE ARCHIVOS  + + + + + + + + + + +
##########################################################################

def upload_file (diResult) :
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif','.jpeg']
    MAX_CONTENT_LENGTH = 1024 * 1024     
    if request.method == 'POST' :         
        for key in request.files.keys():  
            diResult[key]={} 
            diResult[key]['file_error']=False            
            
            f = request.files[key] 
            if f.filename!="":     
                #filename_secure = secure_filename(f.filename)
                file_extension=str(os.path.splitext(f.filename)[1])
                filename_unique = uuid4().__str__() + file_extension
                path_filename=os.path.join( config['upload_folder'] , filename_unique)
                # Validaciones
                if file_extension not in UPLOAD_EXTENSIONS:
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: No se admite subir archivos con extension '+file_extension
                if os.path.exists(path_filename):
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: el archivo ya existe.'
                    diResult[key]['file_name']=f.filename
                try:
                    if not diResult[key]['file_error']:
                        diResult[key]['file_error']=True
                        diResult[key]['file_msg']='Se ha producido un error.'

                        f.save(path_filename)   
                        diResult[key]['file_error']=False
                        diResult[key]['file_name_new']=filename_unique
                        diResult[key]['file_name']=f.filename
                        diResult[key]['file_msg']='OK. Archivo cargado exitosamente'
 
                except:
                        pass
            else:
                diResult[key]={} # viene vacio el input del file upload

    # si existe el archivo devuelve True
    # os.path.exists(os.path.join('G:\\directorio\\....\\uploads',"agua.png"))

    # borrar un archivo
    # os.remove(os.path.join('G:\\directorio\\.....\\uploads',"agua.png"))
            
##########################################################################
# - - F I N - - MANEJO DE  SUBIDA DE ARCHIVOS  - - - - - - - - - - - - - - 
##########################################################################



##########################################################################
# + + I N I C I O + + MANEJO DE  SESSION + + + + + + + + + + + + + + + + +
##########################################################################

def cargarSesion(dicUsuario):
    '''info:
        Realiza la carga de datos del usuario
        en la variable global dict 'session'.
        recibe 'dicUsuario' que es un diccionario con datos
               de un usuario.
        Comentario: Usted puede agregar en 'session' las claves que necesite
    '''

    session['id_usuario'] = dicUsuario['id']
    session['nombre']     = dicUsuario['nombre']
    session['apellido']   = dicUsuario['apellido']
    session['username']   = dicUsuario['usuario'] 
    session['mail']=dicUsuario['mail']  

def crearSesion(request):
    '''info:
        Crea una sesion. Consulta si los datos recibidos son validos.
        Si son validos carga una sesion con los datos del usuario
        recibe 'request' una solicitud htpp con los datos 'email' y 'pass' de 
        un usuario.
        retorna True si se logra un session, False caso contrario
    '''
    sesionValida=False
    mirequest={}
    try: 
        #Carga los datos recibidos del form cliente en el dict 'mirequest'.          
        getRequest(mirequest)
        # CONSULTA A LA BASE DE DATOS. Si usuario es valido => crea session
        dicUsuario={}
        if obtenerUsuarioXEmailPass(dicUsuario,mirequest.get("userid"),mirequest.get("userpassword")):
            # Carga sesion (Usuario validado)
            cargarSesion(dicUsuario)
            sesionValida = True
    except ValueError:                              
        pass
    return sesionValida

def haySesion():  
    '''info:
        Determina si hay una sesion activa observando si en el dict
        session se encuentra la clave 'username'
        retorna True si hay sesión y False si no la hay.
    '''
    return session.get("username")!=None

def cerrarSesion():
    '''info:
        Borra el contenido del dict 'session'
    '''
    try:    
        session.clear()
    except:
        pass

##########################################################################
# - - F I N - - MANEJO DE  SESSION - - - - - - - - - - - - - - - - - - - -
##########################################################################



##########################################################################
# + + I N I C I O + + USUARIO: registro, edicion, actualizacion  + + + + + 
##########################################################################

def ingresoUsuarioValido(param,request):
    '''info:
        Valida el usuario y el pass contra la BD.
        recibe 'param' dict de parámetros
        recibe 'request' una solicitud http con los datos usuario y pass
        retorna: 
            Si es valido el usuario y pass => crea una session y retorna 
            la pagina home.
            Si NO es valido el usuario y pass => retorna la pagina login
            y agrega en el diccionario de parámetros una clave con un mensaje 
            de error para ser mostrada en la pagina login.
    '''
    if crearSesion(request):
        '''
        mireq={}
        getRequest(mireq)
        usuario=mireq['userid'] 
        '''
       
        res=paginaPrincipal()
    else:
        
        res= render_template("login.html", errorVar="Usuario o contraseña incorrectos. Por favor, intentelo de nuevo")
    return res

##########################################################################
# - - F I N - - USUARIO: registro, edicion, actualizacion  - - - - - - - -
##########################################################################
 


##########################################################################
#- - - - - - - - - - - - -   OTRAS PAGINAS    - - - - - - - - - - - - - - -
##########################################################################

#para mostrar las entradas de algun cliente
def mis_entradas(param):
    ''' Info:
        Carga la pagina de mis entradas
        Retorna la pagina misentradas, si hay sesion; sino retorna la home.
    '''
    if haySesion():       # hay session?            
        # Confecciona la pagina en cuestion
        param['page-header']=""
        obtenerEntradasClientePorID(param)
        res= render_template('misentradas.html',param=param)
    else:
        res= redirect('/')   # redirigir al home o a la pagina del login
    return res 


#para mostrar los datos de la cuenta que este activa
def mi_cuenta(param):
    ''' Info:
        Carga la pagina de micuenta
        Retorna la pagina micuenta, si hay sesion; sino retorna la home.
    '''
    if haySesion():       # hay session?            
        # Confecciona la pagina en cuestion
        param['page-header']=""
        obtenerDatosDeLaCuenta(param)
        res= render_template('micuenta.html',param=param)
    else:
        res= redirect('/')   # redirigir al home 
    return res


# Para mostrar el evento sin tener que hacerle un html particular
def noticia(param):
    if haySesion(): 
        param['page-header']=""
        obtenerDatosDeLasNoticias(request, param)
        res = render_template('evento.html',param=param)
    else:
        res = redirect('/')


#para insertar en la tabla 'reserva' una nueva compra
def subirReservaAlSistema(dicDatos,request):
    mirequest={}
    dicDatos={}
    getRequest(mirequest)
    reserva_realizada=False
    dicDatos["id_cliente"]=session.get("id_usuario")
    dicDatos["id_evento"]=mirequest["evId"]
    dicDatos["id_estado"]=1 #tomamos como que al hacer la reserva se la entrega automaticamente
    dicDatos["id_tipo_entrada"]=""
    dicDatos["cantidad_entradas"]=""

    if mirequest.get("cantidad_campo")=="1" or mirequest.get("cantidad_campo")=="2":
        if mirequest.get("cantidad_campo")=="1":
            dicDatos["cantidad_entradas"]=1
            dicDatos["id_tipo_entrada"]=1
        else:
            dicDatos["cantidad_entradas"]=2
            dicDatos["id_tipo_entrada"]=1

        insertarReserva(dicDatos)
        reserva_realizada=True

    if mirequest.get("cantidad_vip")=="1" or mirequest.get("cantidad_vip")=="2":
        if mirequest.get("cantidad_vip")=="1":
            dicDatos["cantidad_entradas"]=1
            dicDatos["id_tipo_entrada"]=2
        else:
            dicDatos["cantidad_entradas"]=2
            dicDatos["id_tipo_entrada"]=2
        
        insertarReserva(dicDatos)
        reserva_realizada=True

    if mirequest.get("cantidad_platea")=="1" or mirequest.get("cantidad_platea")=="2":
        if mirequest.get("cantidad_platea")=="1":
            dicDatos["cantidad_entradas"]=1
            dicDatos["id_tipo_entrada"]=3
        else:
            dicDatos["cantidad_entradas"]=2
            dicDatos["id_tipo_entrada"]=3
        
        insertarReserva(dicDatos)
        reserva_realizada=True

    if not reserva_realizada:
        return render_template("checkout.html",mensaje="No has reservado ningun evento", req=mirequest)
    
    return render_template("checkout.html",mensaje="Tu reserva fue exitosa", req=mirequest)


#para insertar en la tabla 'cliente' un nuevo registro
def subirRegistroAlSistema(dicDatos,request):
    mirequest={}
    dicDatos={}
    getRequest(mirequest)
    dicDatos["nombre"]=mirequest.get("name")
    dicDatos["apellido"]=mirequest.get("surname")
    dicDatos["usuario"]=mirequest.get("userid")
    dicDatos["mail"]=mirequest.get("usermail")
    dicDatos["contrasenia"]=mirequest.get("userpassword")
    res = insertarRegistro(dicDatos)
    if res:
        return render_template("login.html")
    
    return render_template("signup.html",error="El mail o usuario ya existen")


#para insertar en la tabla 'evento' un nuevo evento
def subirEventoAlSistema(dicDatos,request):
    mirequest={}
    dicDatos={}
    getRequest(mirequest)
    upload_file(mirequest)
    dicDatos["nombre"]=mirequest.get("nombre")
    dicDatos["img"]="static/uploads/"+mirequest.get("flyer")["file_name_new"]
    dicDatos["fecha"]=mirequest.get("fechaEvento")
    dicDatos["hora"]=mirequest.get("horario")
    dicDatos["fecha-hora"]=dicDatos["fecha"]+" "+dicDatos["hora"]
    dicDatos["descripcion"]=mirequest.get("descripcion")
    dicDatos["precio_campo"]=mirequest.get("precioCampo")
    dicDatos["precio_vip"]=mirequest.get("precioVip")
    dicDatos["precio_platea"]=mirequest.get("precioPlatea")
    dicDatos["cant_entradas"]=mirequest.get("entradas")
    dicDatos["id_tipo_evento"]=mirequest.get("tipoEvento")
    dicDatos["ubicacion"]=mirequest.get("ubiEvento")

    
    res=insertarEvento(dicDatos)

    if res:
        return render_template("checkoutEvento.html",mensaje="El evento se subio exitosamente")
    else:
        return render_template("checkoutEvento.html",mensaje="No se pudo subir el evento correctamente")


# Para mostrar los eventos
def obtenerDatosDeLosEventos(req, param):
    mireq={}
    getRequest(mireq)
    evento = selectDB(BASE,"SELECT * FROM evento WHERE id = %s", (mireq["id"],))
    if(evento!=[]):
        evento = evento=evento[0]
    return render_template("evento.html", param=param, evento=evento)


# Pagina principal
def paginaPrincipal():
    noticias = selectDB(BASE,"SELECT * FROM noticias")
    return render_template("main.html", noticias=noticias)

# Obtener noticias por categoría
def obtenerNoticiasPorCategoria(categoria_nombre, param):
    # Mapeo de categorías a nombres de archivos de plantilla
    categoria_template_map = {
        "economia": "categorias/economia.html",
        "deportes": "categorias/deportes.html", 
        "policial": "categorias/policiales.html",
        "politica": "categorias/politica.html",
        "sociedad": "categorias/sociedad.html",
        "tecnologia": "categorias/tecno.html"
    }
    
    # Obtener noticias de la categoría específica
    noticias = selectDB(BASE, """
        SELECT n.*, c.nombre as categoria_nombre, u.nombre as autor_nombre 
        FROM noticias n 
        INNER JOIN categoria c ON n.id_categoria = c.id 
        INNER JOIN usuario u ON n.id_usuario = u.id 
        WHERE c.nombre = %s AND n.id_estado = 1
        ORDER BY n.fecha_hora DESC
    """, (categoria_nombre,))
    
    # Obtener el template correcto
    template_name = categoria_template_map.get(categoria_nombre)
    
    # Si no encuentra la categoría en el mapeo, intentar construir el nombre dinámicamente
    if not template_name:
        # Intentar construir el nombre del template basado en la categoría
        if categoria_nombre == "policial":
            template_name = "categorias/policiales.html"
        elif categoria_nombre == "tecnologia":
            template_name = "categorias/tecno.html"
        else:
            # Para otras categorías, usar el nombre directamente
            template_name = f"categorias/{categoria_nombre}.html"
    
    return render_template(template_name, param=param, noticias=noticias)

# Obtener una noticia individual por ID
def obtenerNoticiaIndividual(req, param):
    mireq={}
    getRequest(mireq)
    noticia = selectDB(BASE, """
        SELECT n.*, c.nombre as categoria_nombre, u.nombre as autor_nombre 
        FROM noticias n 
        INNER JOIN categoria c ON n.id_categoria = c.id 
        INNER JOIN usuario u ON n.id_usuario = u.id 
        WHERE n.id = %s AND n.id_estado = 1
    """, (mireq.get("id"),))
    
    if noticia:
        noticia = noticia[0]
    
    return render_template("noticiatemp.html", param=param, noticia=noticia)