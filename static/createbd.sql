-- Crear base de datos y seleccionar
CREATE DATABASE IF NOT EXISTS laposta;
USE laposta;

-- Eliminar tablas si existen (en orden por claves foráneas)
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS comentario;
DROP TABLE IF EXISTS noticias;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS estado;
DROP TABLE IF EXISTS tipo_usuario;
SET FOREIGN_KEY_CHECKS=1;

-- ===========================
-- CREACIÓN DE TABLAS
-- ===========================

CREATE TABLE tipo_usuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tipo VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE estado (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE categoria (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE usuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  usuario VARCHAR(50) NOT NULL,
  email VARCHAR(150) NOT NULL,
  pass VARCHAR(255) NOT NULL,
  id_tipo_usuario INT NOT NULL,
  CONSTRAINT fk_usuario_tipo
    FOREIGN KEY (id_tipo_usuario) REFERENCES tipo_usuario(id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE noticias (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_categoria INT NOT NULL,
  fecha_hora DATETIME NOT NULL,
  titulo VARCHAR(255) NOT NULL,
  subtitulo VARCHAR(255),
  cuerpo TEXT,
  img TEXT,
  id_estado INT NOT NULL,
  CONSTRAINT fk_noticias_usuario
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_noticias_categoria
    FOREIGN KEY (id_categoria) REFERENCES categoria(id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_noticias_estado
    FOREIGN KEY (id_estado) REFERENCES estado(id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE comentario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_noticia INT NOT NULL,
  fecha_hora DATETIME NOT NULL,
  contenido TEXT NOT NULL,
  id_estado INT NOT NULL,
  CONSTRAINT fk_comentario_usuario
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_comentario_noticia
    FOREIGN KEY (id_noticia) REFERENCES noticias(id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_comentario_estado
    FOREIGN KEY (id_estado) REFERENCES estado(id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ===========================
-- DATOS
-- ===========================

-- 1) TIPO_USUARIO
INSERT INTO tipo_usuario (id,tipo) VALUES (NULL,"normal");

UPDATE tipo_usuario 
SET tipo="usuario"
WHERE id=1;

INSERT INTO tipo_usuario (id,tipo) VALUES (NULL,"admin");

-- 2) ESTADO
INSERT INTO estado (id,nombre) VALUES (NULL,"PUBLICADO");
INSERT INTO estado (id,nombre) VALUES (NULL,"NO PUBLICADO");

-- 3) CATEGORIA
INSERT INTO categoria (id,nombre,descripcion)
VALUES
(NULL,"Policiales","Noticias sobre policiales"),
(NULL,"Economía","Noticias sobre economía"),
(NULL,"Sociedad","Noticias sobre sociedad"),
(NULL,"Tecnología","Noticias sobre tecnología"),
(NULL,"Política","Noticias sobre política"),
(NULL,"Deportes","Noticias sobre deportes");

-- 4) USUARIO
INSERT INTO usuario
(id,nombre,apellido,usuario,email,pass,id_tipo_usuario)
VALUES
(NULL,"Nico","Albornoz","nicolas","nicolasalbornoz@uca.edu.ar","1234",2),
(NULL,"Conra","Clementi","conrado","conradoclementi@uca.edu.ar","1234",2),
(NULL,"Bruno","Zarco","bruno","brunozarco@uca.edu.ar","1234",2),
(NULL,"Ivan","Kamermann","ivan","ivankamermann@uca.edu.ar","1234",2);

-- Nota: la carga de noticias y comentarios se realiza desde static/laposta.sql
