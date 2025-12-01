#route es el modulo que intercambia la información tomando los request y dando las responses
#tiene internamente las rutas que escribe el cliente en la url del navegador

from __mysql__db import * #importo las funciones que interaccionan con la base de datos
from controller import * #importo las funciones que cree en controller
from flask import render_template # https://flask.palletsprojects.com/en/2.3.x/tutorial/templates/
#para renderizar las plantillas con jinja y crear paginas dinamicas
from flask import Flask,redirect, request, session  
# redirect: redirigir a otras rutas 
# request: gestiona las solicitudes http recibidas 
# session: para el manejo de sesion
from appConfig import config  # Archivo de configuracion de la aplicación
import os  # Gestiona acceso al sistema operativo local

error = ""

def Route(aplicacion=Flask):

    @aplicacion.route("/GuardarDatosPerfil", methods=["POST"])
    def DeterminarValidez():
        ''' Info: 
          Recepciona la solicitud request que es enviada
          desde el formulario de login 
          retorna la pagina home en caso de exito 
          o la pagina login en caso de fracaso
        '''
        param={}
        return ingresoUsuarioValido(param,request)
    


    #para hacer disponible la variable usuario en todas las plantillas de manera automática
    @aplicacion.context_processor
    def inject_user():
        if session.get('username')!=None :
            return dict(usuario=session.get('username'))
        else:
            return dict(usuario="")

        

    @aplicacion.route("/logout")
    def logout():  
        ''' Info: 
          Cierra la sesión.
          retorna la redirección a la pagina home
        ''' 
        cerrarSesion()     
        return redirect('/')
    
    @aplicacion.route("/noticiasAdm")
    def noticias_admin():
        ''' Página de administración de noticias '''
        return paginaAdminNoticias()
    
    @aplicacion.route("/cambiar_estado_noticia", methods=["POST"])
    def cambiar_estado_noticia():
        ''' Procesa el cambio de estado de una noticia '''
        return procesarCambioEstadoNoticia(request)
    
    @aplicacion.route("/comentariosAdm")
    def comentarios_admin():
        ''' Página de administración de comentarios '''
        if not haySesion() or not esAdministrador():
            return redirect('/login')
        # Aquí puedes agregar la lógica para mostrar los comentarios
        return render_template("comentariosAdm.html")
    


    @aplicacion.route("/")    
    @aplicacion.route("/home")
    def indice():
        return paginaPrincipal()


    @aplicacion.route('/login')
    def login():
        # Preparar datos comunes para el header
        param = {}
        obtenerCategorias(param)
        categorias = param.get('categorias', [])
        es_admin = esAdministrador()
        usuario_logueado = haySesion()

        return render_template(
            'login.html',
            categoria=categorias,
            es_admin=es_admin,
            usuario_logueado=usuario_logueado
        )
    


    @aplicacion.route("/signup",methods=["GET"])
    def signup():
        # Preparar datos comunes para el header
        param = {}
        obtenerCategorias(param)
        categorias = param.get('categorias', [])
        es_admin = esAdministrador()
        usuario_logueado = haySesion()

        return render_template(
            'registrarse.html',
            categoria=categorias,
            es_admin=es_admin,
            usuario_logueado=usuario_logueado
        )
    

    
    @aplicacion.route("/CargarDatosUsuario",methods=["POST"])
    def registrar_cuenta():
        param={}
        return subirRegistroAlSistema(param,request)
    

  
    @aplicacion.route("/noticia", methods=["GET","POST"])
    def noticia_route():
        param = {}
        # Usar la función de controller que arma noticia + otras_noticias + header y comentarios
        return noticia(param)



    @aplicacion.route("/nueva_noticia",methods=["POST"])
    def nueva_noticia():
        param={}
        return subirNoticiaAlSistema(param,request)
    


    @aplicacion.route("/nuevonoticia")
    def nuevanoticia():
        return mostrarFormularioNuevaNoticia()
    

    
    @aplicacion.route("/checkout")
    def checkout():
        return render_template("checkout.html")
    
    
    @aplicacion.route("/economia")
    def economia():
        param = {}
        return obtenerNoticiasPorCategoriaSlug("economia", param)
    
    
    @aplicacion.route("/deportes")
    def deportes():
        param = {}
        return obtenerNoticiasPorCategoriaSlug("deportes", param)
    
    
    @aplicacion.route("/policiales")
    def policiales():
        param = {}
        return obtenerNoticiasPorCategoriaSlug("policiales", param)
    
    
    @aplicacion.route("/politica")
    def politica():
        param = {}
        return obtenerNoticiasPorCategoriaSlug("politica", param)
    
    
    @aplicacion.route("/sociedad")
    def sociedad():
        param = {}
        return obtenerNoticiasPorCategoriaSlug("sociedad", param)
    
    
    @aplicacion.route("/tecno")
    def tecno():
        param = {}
        return obtenerNoticiasPorCategoriaSlug("tecno", param)
    
    
    # Ruta antigua /categoria?id=... ya no es necesaria; se usan slugs /deportes, /economia, etc.
    
    
    """
    @aplicacion.route("/noticias")
    def noticia_individual():
        param = {}
        return obtenerNoticiaIndividual(request, param)
    """