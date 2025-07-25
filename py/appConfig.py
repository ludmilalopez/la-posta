#importa el módulo path del paquete os, que proporciona funciones para trabajar con rutas de archivos y directorios
from os import path 

config={} #Diccionario vacio para almacenar las configuraciones del proyecto

# Directorio del proyecto
config['project_folder'] = path.dirname(path.realpath(__file__))
#__file__: Representa el nombre del archivo Python que se está ejecutando
#path.realpath(__file__): Devuelve la ruta completa (absoluta) del archivo Python actual
#path.dirname(path.realpath(__file__)): Obtiene el directorio que contiene el archivo Python actual
#config['project_folder'] contendrá la ruta del directorio donde se encuentra el archivo Python actual

# directorio para subir archivos (con el path completo)
config['upload_folder']  = path.join( config['project_folder'] ,'py/uploads')
#Combina la ruta del directorio del proyecto con el subdirectorio 'uploads'
#config['upload_folder'] contiene la ruta del subdirectorio uploads dentro del directorio del proyecto.