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
        return render_template("signup.html")
    

    
    @aplicacion.route("/micuenta")
    def micuenta():
        param={}
        return mi_cuenta(param)
    


    @aplicacion.route("/reservar_entradas",methods=["POST"])
    def reservar_entradas():
        param={}
        return subirReservaAlSistema(param,request)
    

    
    @aplicacion.route("/CargarDatosCliente",methods=["POST"])
    def registrar_cuenta():
        param={}
        return subirRegistroAlSistema(param,request)
    

  
    @aplicacion.route("/evento", methods = ["GET"])
    def evento():
        param = {}
        return obtenerDatosDeLosEventos(request, param)
    
    

    @aplicacion.route("/misentradas")
    def misentradas():
        param={}
        return mis_entradas(param)
    


    @aplicacion.route("/misventas")
    def misventas():
        param={}
        return mis_ventas(param)
    


    @aplicacion.route("/nuevo_evento",methods=["POST"])
    def nuevo_evento():
        param={}
        return subirEventoAlSistema(param,request)
    


    @aplicacion.route("/nuevoevento")
    def nuevoevento():
        return render_template("nuevoevento.html")
    

    
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
    
    
    @aplicacion.route("/noticias")
    def noticia_individual():
        param = {}
        return obtenerNoticiaIndividual(request, param)
    