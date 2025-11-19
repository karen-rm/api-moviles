from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

def get_conn():
    # En local puedes usar variables de entorno o URL fija
    # Railway te dará vars de entorno en producción
    DATABASE_URL = os.getenv("DATABASE_URL")  # Railway usa DATABASE_URL
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL, sslmode="require", cursor_factory=RealDictCursor)
    # fallback local 
    return psycopg2.connect(host="localhost", dbname="quizzes", user="postgres", password="13postgre22", cursor_factory=RealDictCursor)

@app.route("/cuestionarios", methods=["GET"])
def get_cuestionarios():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, titulo FROM cuestionario ORDER BY id DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows), 200

@app.route("/cuestionario", methods=["POST"])
def create_cuestionario():
    data = request.get_json()
    titulo = data.get("titulo")
    if not titulo:
        return jsonify({"error":"titulo required"}), 400
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO cuestionario (titulo) VALUES (%s) RETURNING id, titulo;", (titulo,))
    new = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new), 201

@app.route("/pregunta", methods=["POST"])
def create_item():
    data = request.get_json()
    pregunta = data.get("pregunta")
    correcta = data.get("correcta")
    opc1 = data.get("opc1")
    opc2 = data.get("opc2")
    if not pregunta & correcta & opc1 & opc2:
        return jsonify({"error":"4 campos required"}), 400
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO pregunta (preguntas) VALUES (%s) RETURNING id, pregunta;", (pregunta,))
    new = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new), 201

@app.route("/cuestionario/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id=%s;", (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message":"deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
