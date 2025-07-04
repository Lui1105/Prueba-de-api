import os
import psycopg2;
from flask import Flask, request, jsonify, g
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:LUIS_PRUEBA1105@db.ncoyompjudfzqrwwpjsf.supabase.co:5432/postgres?sslmode=require')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        try:
            db = g._database = psycopg2.connect(DATABASE_URL);
        except psycopg2.Error as e:
            print(f"Error al conectar a la base de datos: {e}");
            raise

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_user(username):
    conect = None;
    try:
        #Obteniendo la base de datos
        conect = get_db();
        #Obteniendo el cursor de la base de datos
        cursor = conect.cursor();
        #Obteniendo la contraseña de la fila que coincida con el nombre de usuario
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        return row[0] if row else None
    except psycopg2.Error as e:
        print(f"Error al consultar usuario en la base de datos: {e}");
        return None;
    finally:
        pass;

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400
    db_password = query_user(username)
    if db_password == password:
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

if __name__ == '__main__':
    app.run(debug=True)

