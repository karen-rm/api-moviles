from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

def get_conn():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        port=os.getenv("PGPORT"),
        cursor_factory=RealDictCursor
    )

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

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cuestionario (titulo) VALUES (%s) RETURNING id, titulo;",
        (titulo,)
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
