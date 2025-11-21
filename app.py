from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2
import secrets
import string
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

import os

print("DATABASE_URL =", os.getenv("DATABASE_URL"))
print("PGHOST =", os.getenv("PGHOST"))
print("PGUSER =", os.getenv("PGUSER"))
print("PGDATABASE =", os.getenv("PGDATABASE"))
print("PGPORT =", os.getenv("PGPORT"))
print("TEST_VAR =", os.getenv("TEST_VAR"))



def get_conn():
    # 1) Intenta usar la url completa de railway
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return psycopg2.connect(db_url, sslmode="require", cursor_factory=RealDictCursor)

    # 2) Si falla, usa las variables de PGHOST / PGUSER
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        port=os.getenv("PGPORT"),
        cursor_factory=RealDictCursor
    )

def generar_codigo():
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(8))


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
        return jsonify({"error": "titulo required"}), 400
    
    codigo = generar_codigo()

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cuestionario (codigo, titulo) VALUES (%s, %s) RETURNING id, codigo, titulo;",
        (codigo, titulo)
    )
    new = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(new), 201


@app.route("/pregunta", methods=["POST"])
def create_pregunta():
    data = request.get_json()

    pregunta = data.get("pregunta")
    correcta = data.get("correcta")
    opc1 = data.get("opc1")
    opc2 = data.get("opc2")
    cuestionario_id = data.get("cuestionario_id")

    if not (pregunta and correcta and opc1 and opc2 and cuestionario_id):
        return jsonify({"error": "Todos los campos son requeridos"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO pregunta (pregunta, respuesta_correcta, opcion1, opcion2, cuestionario_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, pregunta;
    """, (pregunta, correcta, opc1, opc2, cuestionario_id))

    new = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(new), 201


@app.route("/cuestionario/<int:item_id>", methods=["DELETE"])
def delete_cuestionario(item_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM cuestionario WHERE id=%s;", (item_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
