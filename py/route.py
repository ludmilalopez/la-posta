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
    


    @aplicacion.route("/")    
    @aplicacion.route("/home")
    def indice():
        return paginaPrincipal()
    


    @aplicacion.route('/login')
    def login():
        return render_template('login.html')
    


    @aplicacion.route("/signup",methods=["GET"])
    def signup():
        return render_template("registrarse.html")
    

    
    @aplicacion.route("/CargarDatosUsuario",methods=["POST"])
    def registrar_cuenta():
        param={}
        return subirRegistroAlSistema(param,request)
    

  
    @aplicacion.route("/noticia", methods = ["GET"])
    def noticia():
        param = {}
        return obtenerDatosDeLasNoticias(request, param)



    #mis noticias admin
    @aplicacion.route("/misentradas")
    def misentradas():
        param={}
        return mis_entradas(param)
    
    

    @aplicacion.route("/nueva_noticia",methods=["POST"])
    def nueva_noticia():
        param={}
        return subirNoticiaAlSistema(param,request)
    


    @aplicacion.route("/nuevonoticia")
    def nuevonoticia():
        return render_template("noticia.html")
    

    
    @aplicacion.route("/checkout")
    def checkout():
        return render_template("checkout.html")
    
    
    @aplicacion.route("/economia")
    def economia():
        param = {}
        return obtenerNoticiasPorCategoria("economia", param)
    
    
    @aplicacion.route("/deportes")
    def deportes():
        param = {}
        return obtenerNoticiasPorCategoria("deportes", param)
    
    
    @aplicacion.route("/policiales")
    def policiales():
        param = {}
        return obtenerNoticiasPorCategoria("policial", param)
    
    
    @aplicacion.route("/politica")
    def politica():
        param = {}
        return obtenerNoticiasPorCategoria("politica", param)
    
    
    @aplicacion.route("/sociedad")
    def sociedad():
        param = {}
        return obtenerNoticiasPorCategoria("sociedad", param)
    
    
    @aplicacion.route("/tecno")
    def tecno():
        param = {}
        return obtenerNoticiasPorCategoria("tecnologia", param)
    
    
    """
    @aplicacion.route("/noticias")
    def noticia_individual():
        param = {}
        return obtenerNoticiaIndividual(request, param)
    """