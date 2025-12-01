import sys
import os

def test_connection():
    conn = None
    used_project_connector = False

    # 1) Intentar usar el conector del proyecto si está disponible
    try:
        from __mysql__db import BASE, conectarBD  # may raise
        try:
            conn = conectarBD(BASE)
            used_project_connector = True
        except Exception as e:
            print("INFO: Conector del proyecto falló, fallback a pymysql:", e)
            conn = None
    except Exception:
        # módulo no disponible, usar fallback
        conn = None

    # 2) Fallback: usar pymysql con configuración XAMPP por defecto
    if conn is None:
        try:
            import pymysql
        except Exception:
            print("ERROR: 'pymysql' no está instalado. Instálalo con:")
            print("   python -m pip install pymysql")
            sys.exit(1)

        cfg = {
            "host": os.environ.get("DB_HOST", "127.0.0.1"),
            "user": os.environ.get("DB_USER", "root"),
            "password": os.environ.get("DB_PASS", ""),
            "db": os.environ.get("DB_NAME", "laposta"),
            "port": int(os.environ.get("DB_PORT", 3306)),
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor,
            "connect_timeout": 5,
        }
        try:
            conn = pymysql.connect(**cfg)
        except Exception as e:
            print("ERROR conectando con pymysql:", e)
            print("Asegúrate de que MySQL (XAMPP) esté arrancado y que las credenciales sean correctas.")
            sys.exit(1)

    # 3) Ejecutar comprobaciones básicas
    try:
        cur = conn.cursor()

        # Verificar existencia de la tabla 'noticias'
        try:
            cur.execute("SHOW TABLES LIKE 'noticias'")
            found = cur.fetchone()
            if not found:
                print("ERROR: No se encontró la tabla 'noticias' en la base de datos. Importa static/laposta.sql o crea la tabla.")
            else:
                # Contar noticias publicadas (id_estado = 1)
                cur.execute("SELECT COUNT(*) AS count_pub FROM noticias WHERE id_estado = 1")
                row = cur.fetchone()
                count_pub = None
                if isinstance(row, dict):
                    count_pub = row.get('count_pub')
                elif isinstance(row, (list, tuple)):
                    count_pub = row[0]
                print(f"OK: Noticias publicadas (id_estado=1): {count_pub}")
        except Exception as e:
            print("ERROR al consultar la tabla 'noticias':", e)

        # Listar categorías (opcional)
        try:
            cur.execute("SELECT id, nombre FROM categoria ORDER BY nombre")
            categorias = cur.fetchall()
            if categorias:
                print(f"Categorias ({len(categorias)}):")
                for r in categorias:
                    if isinstance(r, dict):
                        print(f" - {r.get('id')} {r.get('nombre')}")
                    else:
                        print(f" - {r[0]} {r[1]}")
            else:
                print("No se encontraron categorías en la BD.")
        except Exception:
            pass

    finally:
        try:
            cur.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass

    print("Test finalizado. Usado conector del proyecto:", used_project_connector)


if __name__ == "__main__":
    test_connection()
