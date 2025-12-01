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
from appConfig import config  # Archivo de configuracion de la aplicación
import os
from uuid import uuid4

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
    session['mail']=dicUsuario['email']
    session['id_tipo_usuario']=dicUsuario['id_tipo_usuario']
    session['tipo_usuario']=dicUsuario['tipo_usuario']  

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

def esAdministrador():
    '''info:
        Verifica si el usuario logueado es administrador
        Retorna True si es admin, False caso contrario
    '''
    return session.get("tipo_usuario") == "admin"

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

# Para mostrar la noticia sin tener que hacerle un html particular
def noticia(param):
    # Página de detalle de una noticia individual + comentarios
    mireq = {}
    getRequest(mireq)

    # ID de la noticia
    noticia_id = mireq.get("id")

    # Si viene un POST y hay sesión, procesar nuevo comentario
    if request.method == 'POST' and haySesion() and noticia_id:
        texto = mireq.get("comentario", "").strip()
        if texto != "":
            # limitar a 300 caracteres por seguridad
            texto = texto[:300]
            dic = {
                "id_usuario": session.get("id_usuario"),
                "id_noticia": int(noticia_id),
                "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "contenido": texto,
                "id_estado": 1  # PUBLICADO
            }
            insertarComentario(dic)
        # evitar reenvío de formulario
        return redirect(f"/noticia?id={noticia_id}")

    # Obtener la noticia principal
    param['page-header'] = ""
    obtenerDatosDeLasNoticias(request, param)
    noticia = param.get('noticia')

    # Cargar categorías y flags de usuario para el header
    obtenerCategorias(param)
    categorias = param.get('categorias', [])
    es_admin = esAdministrador()
    usuario_logueado = haySesion()

    # Otras noticias (sidebar): todas las publicadas menos la actual
    otras_noticias = []
    if noticia_id:
        sSql = """
            SELECT n.id, n.titulo
            FROM noticias n
            WHERE n.id_estado = 1 AND n.id <> %s
            ORDER BY n.fecha_hora DESC
        """
        otras_noticias = selectDB(BASE, sSql, (noticia_id,)) or []
    else:
        sSql = """
            SELECT n.id, n.titulo
            FROM noticias n
            WHERE n.id_estado = 1
            ORDER BY n.fecha_hora DESC
        """
        otras_noticias = selectDB(BASE, sSql) or []

    # Comentarios de la noticia
    comentarios_param = {}
    if noticia_id:
        obtenerComentariosPorNoticia(int(noticia_id), comentarios_param)
    comentarios = comentarios_param.get('comentarios', [])

    return render_template(
        'noticia.html',
        noticia=noticia,
        otras_noticias=otras_noticias,
        comentarios=comentarios,
        categoria=categorias,
        es_admin=es_admin,
        usuario_logueado=usuario_logueado
    )


def borrarComentario(request):
    '''Permite al admin borrar un comentario por id.'''
    if not haySesion() or not esAdministrador():
        return redirect('/login')

    mireq = {}
    getRequest(mireq)
    comentario_id = mireq.get("comentario_id")
    noticia_id = mireq.get("noticia_id")

    if comentario_id:
        try:
            borrarComentarioPorId(int(comentario_id))
        except:
            pass

    # Volver a la noticia de origen si tenemos el id
    if noticia_id:
        return redirect(f"/noticia?id={noticia_id}")
    return redirect('/')


"""Noticias creadas por usuarios"""

def mostrarFormularioNuevaNoticia():
    """Muestra el formulario para crear una nueva noticia.

    Solo usuarios logueados pueden acceder. Las categorías se cargan
    dinámicamente para que el usuario elija.
    """
    if not haySesion():
        return redirect('/login')

    param = {}
    obtenerCategorias(param)
    categorias = param.get('categorias', [])
    es_admin = esAdministrador()
    usuario_logueado = haySesion()

    return render_template(
        "nuevanoticia.html",
        categoria=categorias,
        es_admin=es_admin,
        usuario_logueado=usuario_logueado
    )


def subirNoticiaAlSistema(dicDatos, request):
    """Recibe los datos del formulario de nueva noticia y los guarda como PENDIENTE.

    - Requiere usuario logueado.
    - Usa id_estado = 2 (pendiente), para que el admin luego la apruebe
      desde la pantalla de administración de noticias.
    """
    if not haySesion():
        return redirect('/login')

    mirequest = {}
    getRequest(mirequest)

    # Subida de imagen (opcional, pero la plantilla la marca como requerida)
    files_info = {}
    upload_file(files_info)

    # Resolver ruta de imagen si se subió correctamente
    img_path = None
    if "imagen" in files_info and not files_info["imagen"].get("file_error", False):
        img_path = "uploads/" + files_info["imagen"]["file_name_new"]

    # Construir diccionario para insertar en la tabla noticias
    dicDatos = {}
    dicDatos["id_usuario"] = session.get("id_usuario")
    dicDatos["id_categoria"] = int(mirequest.get("id_categoria")) if mirequest.get("id_categoria") else None
    dicDatos["fecha_hora"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dicDatos["titulo"] = mirequest.get("titulo")
    dicDatos["subtitulo"] = mirequest.get("subtitulo")
    dicDatos["cuerpo"] = mirequest.get("cuerpo")
    dicDatos["img"] = img_path
    dicDatos["id_estado"] = 2  # 2 = pendiente de aprobación

    res = insertarNoticias(dicDatos)

    if res:
        mensaje = "Tu noticia fue enviada y quedará pendiente de aprobación por un administrador."
    else:
        mensaje = "Ocurrió un error al enviar tu noticia. Intentalo nuevamente."

    param = {}
    obtenerCategorias(param)
    categorias = param.get('categorias', [])
    es_admin = esAdministrador()
    usuario_logueado = haySesion()

    return render_template(
        "nuevanoticia.html",
        categoria=categorias,
        es_admin=es_admin,
        usuario_logueado=usuario_logueado,
        mensaje=mensaje
    )


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


# Pagina principal
def paginaPrincipal():
    # Param base y datos generales
    param = {}
    obtenerNoticiasPorID(param)   # todas las noticias publicadas
    obtenerCategorias(param)      # todas las categorías
    todas_noticias = param.get('noticias', [])
    categorias = param.get('categorias', [])

    # Construir diccionario: última noticia por categoría (id_categoria)
    ultimas_por_categoria = {}
    for n in todas_noticias:
        # n = SELECT n.*, c.nombre, u.nombre =>
        # índices base de la tabla noticias:
        # 0:id, 1:id_usuario, 2:id_categoria, 3:fecha_hora, 4:titulo,
        # 5:subtitulo, 6:cuerpo, 7:img, 8:id_estado, 9:categoria_nombre, 10:autor_nombre
        cat_id = n[2]
        # Como vienen ordenadas DESC por fecha_hora, la primera que vemos por categoría es la última
        if cat_id not in ultimas_por_categoria:
            ultimas_por_categoria[cat_id] = n

    # Armar lista ordenada por nombre de categoría para el template
    ultimas = []
    for cat in categorias:
        # cat = (id, nombre)
        cid = cat[0]
        if cid in ultimas_por_categoria:
            ultimas.append({
                'categoria': cat,         # tupla (id, nombre)
                'noticia': ultimas_por_categoria[cid]  # fila completa de noticias
            })

    es_admin = esAdministrador()
    usuario_logueado = haySesion()

    return render_template(
        "home.html",
        ultimas=ultimas,              # lista de {'categoria': (id,nombre), 'noticia': fila}
        categoria=categorias,
        es_admin=es_admin,
        usuario_logueado=usuario_logueado
    )

""" Obtener noticias por categoría usando slug y plantilla unica categoria.html """
def obtenerNoticiasPorCategoriaSlug(slug, param):
    # Mapear slug a nombre real de categoría en la BD
    slug_map = {
        "deportes": "Deportes",
        "economia": "Economía",
        "policiales": "Policiales",
        "politica": "Política",
        "sociedad": "Sociedad",
        "tecno": "Tecnología",
    }

    nombre_categoria = slug_map.get(slug)
    if not nombre_categoria:
        return redirect("/")

    # Buscar id de la categoría
    fila = selectDB(BASE, "SELECT id, nombre FROM categoria WHERE nombre = %s", (nombre_categoria,))
    if not fila:
        return redirect("/")

    categoria_id = fila[0][0]

    # Reusar la lógica existente por id
    return obtenerNoticiasPorCategoriaID(categoria_id, param)

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


# Obtener noticias por ID de categoría
def obtenerNoticiasPorCategoriaID(categoria_id, param):
    # Obtener noticias de la categoría específica por ID (todas las publicadas)
    noticias = selectDB(BASE, """
        SELECT n.*, c.nombre as categoria_nombre, u.nombre as autor_nombre 
        FROM noticias n 
        INNER JOIN categoria c ON n.id_categoria = c.id 
        INNER JOIN usuario u ON n.id_usuario = u.id 
        WHERE c.id = %s AND n.id_estado = 1
        ORDER BY n.fecha_hora DESC
    """, (categoria_id,))

    # Obtener también todas las categorías para el header
    obtenerCategorias(param)
    categorias = param.get('categorias', [])

    # Buscar el nombre de la categoría actual para el título
    categoria_actual = None
    for c in categorias:
        if c[0] == int(categoria_id):
            categoria_actual = c
            break

    es_admin = esAdministrador()
    usuario_logueado = haySesion()

    return render_template(
        "categoria.html",
        categoria_actual=categoria_actual,
        noticias=noticias,
        categoria=categorias,
        es_admin=es_admin,
        usuario_logueado=usuario_logueado
    )


def paginaAdminNoticias():
    '''Función para mostrar la página de administración de noticias'''
    if not haySesion() or not esAdministrador():
        return redirect('/login')
    
    param = {}
    obtenerNoticiasPendientes(param)
    noticias_pendientes = param.get('noticias_pendientes', [])
    
    return render_template("noticiasAdm.html", 
                          noticias_pendientes=noticias_pendientes,
                          es_admin=True,
                          usuario_logueado=True)


def procesarCambioEstadoNoticia(request):
    '''Función para procesar el cambio de estado de una noticia'''
    if not haySesion() or not esAdministrador():
        return redirect('/login')
    
    mireq = {}
    getRequest(mireq)
    
    noticia_id = mireq.get("noticia_id")
    nuevo_estado = mireq.get("nuevo_estado")
    
    if noticia_id and nuevo_estado:
        # Convertir estado text a número
        if nuevo_estado == "publicado":
            estado_num = 1
        elif nuevo_estado == "no-publicado":
            estado_num = 2
        else:
            estado_num = 3  # rechazado
            
        if actualizarEstadoNoticia(noticia_id, estado_num):
            return redirect('/noticiasAdm?success=1')
        else:
            return redirect('/noticiasAdm?error=1')
    
    return redirect('/noticiasAdm')