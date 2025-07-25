show databases;

use laposta;

show tables;

-- Ver o leer una tabla

SELECT * FROM usuario;

SELECT * FROM categoria;

SELECT * FROM noticias;

SELECT * FROM comentario;

SELECT * FROM estado;

SELECT * FROM tipo_usuario;

-- ver estrucura paaa

describe usuario;

describe tipo_usuario;

describe noticias;

describe estado;

describe comentario;

describe categoria;

--Para agregar o insertar una estructura dentro de la tabla

INSERT INTO tipo_usuario
(id,tipo) 
VALUES 
(NULL,"normal")

UPDATE tipo_usuario SET tipo="usuario"
WHERE id=1;

INSERT INTO tipo_usuario
(id,tipo) 
VALUES 
(NULL,"admin")

SELECT * FROM tipo_usuario;

INSERT INTO estado
(id,nombre)
VALUES
(NULL,"PUBLICADO");

INSERT INTO estado
(id,nombre)
VALUES
(NULL,"NO PUBLICADO");

SELECT * FROM estado;

INSERT INTO categoria
(id,nombre,descripcion)
VALUES
(NULL,"policial","un policia mato un chorro mientras hacia truquitos corte kick buttowski, re loquito jaja");

UPDATE categoria SET descripcion="Noticias sobre policiales"
WHERE id=1;

INSERT INTO categoria
(id,nombre,descripcion)
VALUES
(NULL,"economia","el mercado se regula solo");

UPDATE categoria SET descripcion="Noticias sobre economía"
WHERE id=2;

INSERT INTO categoria
(id,nombre,descripcion)
VALUES
(NULL,"sociedad","Noticias sobre sociedad"),
(NULL,"tecnologia","Noticias sobre tecnología"),
(NULL,"politica","Noticias sobre politica"),
(NULL,"deportes","Noticias sobre deportes");

SELECT * FROM categoria;

INSERT INTO noticias
(id,id_usuario,id_categoria,fecha_hora,titulo,subtitulo,cuerpo,img,id_estado)
VALUES
(NULL,2,2,"2024-01-02 20:40:50","Policia mato un ladron","Hernesto segundo decidio matarlo con alto fierro","aaa","https://www.google.com/url?sa=i&url=https%3A%2F%2Fes.wikipedia.org%2Fwiki%2FPolic%25C3%25ADa&psig=AOvVaw2TpoXmLWA2pz0tSPE06EYB&ust=1717823023972000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCLjPxsvbyIYDFQAAAAAdAAAAABAE",1);

SELECT * FROM noticias;

INSERT INTO comentario
(id,id_usuario,id_noticia,fecha_hora,contenido,id_estado)
VALUES
(NULL,4,2,"2024-01-02 20:42:50","aguante el poli paa",2);

SELECT * FROM comentario;

INSERT INTO usuario
(id,nombre,apellido,usuario,email,pass,id_tipo_usuario)
VALUES
(NULL,"Nico","Albornoz","nicolas","nicolasalbornoz@uca.edu.ar",1234,2),
(NULL,"Conra","Clementi","conrado","conradoclementi@uca.edu.ar",1234,2),
(NULL,"Bruno","Zarco","bruno","brunozarco@uca.edu.ar",1234,2),
(NULL,"Ivan","Kamermann","ivan","ivankamermann@uca.edu.ar",1234,2);

SELECT * FROM usuario;

-- Actualizacion de algun dato

UPDATE usuario SET apellido="Batman"
WHERE id=3;

SELECT * FROM usuario;

-- borrar datos 

DELETE FROM tipo_usuario WHERE id=5;

SELECT * FROM usuario WHERE id=3;


SELECT * FROM noticias;

SELECT * FROM usuario;
SELECT * FROM usuario
    INNER JOIN noticias on usuario.id=noticias.id_usuario;