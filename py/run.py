#run se va a encargar de poner a funcionar todo mi sistema

from flask import Flask,session
#importo de la librería flask, el módulo Flask para poder instanciar un servidor http. 
from route import Route
#de route, importo la funcion Route 
import os
#importo os que Gestiona acceso al sistema operativo local

def main():
    flask = Flask(__name__,template_folder="templates",static_folder="static") #se activa la aplicacion

    flask.secret_key="1234567890" #se determina una clave secreta

    Route(flask) #invoco a la funcion Route pasando por parametro flask

    flask.run("0.0.0.0",5000,debug = True) # #Método que inicia la app con la dirección, puertos y modo de argumentos.
    #"0.0.0.0" es la dirección en la que va a estar corriendo, en este caso los 0 dicen que administre con localhost
    #5000: es el puerto (el puerto por default es 80)
    #debug: hace que se esté monitoreando todo el tiempo la aplicación ante cualquier modificación de este archivo u otro del proyecto

main()