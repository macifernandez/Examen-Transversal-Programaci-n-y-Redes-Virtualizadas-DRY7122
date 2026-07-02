from flask import Flask
import sqlite3
import hashlib

sample = Flask(__name__)

def crear_hash(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

def crear_base_datos():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        contrasena_hash TEXT NOT NULL
    )
    """)

    usuarios = [
        ("Maciel Fernandez", crear_hash("maciel123")),
        ("Danitza Flores", crear_hash("danitza123"))
    ]

    cursor.execute("DELETE FROM usuarios")

    cursor.executemany(
        "INSERT INTO usuarios (nombre, contrasena_hash) VALUES (?, ?)",
        usuarios
    )

    conexion.commit()
    conexion.close()

def validar_usuarios():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT nombre, contrasena_hash FROM usuarios")
    usuarios = cursor.fetchall()

    print("Usuarios registrados:")
    for usuario in usuarios:
        print(usuario)

    conexion.close()

@sample.route("/")
def main():
    crear_base_datos()
    validar_usuarios()
    return "Base de datos creada con usuarios y contraseñas en hash\n"

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=7500)
