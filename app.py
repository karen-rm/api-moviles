from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2
import secrets
import string
from psycopg2.extras import RealDictCursor
import psycopg2.extras

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

    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return psycopg2.connect(db_url, sslmode="require", cursor_factory=RealDictCursor)

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
    cur.execute("SELECT id, titulo, codigo FROM cuestionario ORDER BY id DESC;")
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


@app.route("/preguntas/<int:cuestionario_id>", methods=["GET"])
def obtener_preguntas(cuestionario_id):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT
            id,
            pregunta,
            respuesta_correcta,
            opcion1,
            opcion2,
            cuestionario_id
        FROM pregunta
        WHERE cuestionario_id = %s
        ORDER BY id ASC;
    """, (cuestionario_id,))

    preguntas = cur.fetchall()
    conn.close()

    return jsonify(preguntas), 200


@app.route("/cuestionario_completo/<int:cuestionario_id>", methods=["DELETE"])
def eliminar_cuestionario_completo(cuestionario_id):
    conn = get_conn()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM pregunta WHERE cuestionario_id=%s;", (cuestionario_id,))
    cur.execute("DELETE FROM cuestionario WHERE id=%s;", (cuestionario_id,))

    conn.commit()
    count = cur.rowcount
    cur.close()
    conn.close()

    return jsonify({"message": "cuestionario y preguntas eliminadas", "count": count}), 200


@app.route("/preguntas/cuestionario/<int:cuestionario_id>", methods=["DELETE"])
def eliminar_preguntas(cuestionario_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM pregunta WHERE cuestionario_id=%s;", (cuestionario_id,))
    conn.commit()
    cur.close()
    conn.close()

    deleted = cur.rowcount
    return jsonify({"message": "deleted", "count": deleted}), 200


@app.route("/alumno", methods=["POST"])
def guardar_alumno():
    data = request.get_json()

    nombre = data.get("nombre")
    puntaje = data.get("puntaje")
    tiempo_inicio = data.get("tiempo_inicio")
    tiempo_final = data.get("tiempo_final")
    aprobado = data.get("aprobado")
    cuestionario_id = data.get("cuestionario_id")

    if not (nombre and puntaje is not None and tiempo_inicio and tiempo_final and aprobado is not None and cuestionario_id):
        return jsonify({"error": "Todos los campos son requeridos"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO alumno (nombre, puntaje, tiempo_inicio, tiempo_final, aprobado, cuestionario_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, nombre, puntaje, tiempo_inicio, tiempo_final, aprobado, cuestionario_id;
    """, (nombre, puntaje, tiempo_inicio, tiempo_final, aprobado, cuestionario_id))

    new = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(new), 201


@app.route("/estadisticas/aprobados", methods=["GET"])
def estadisticas_aprobados():
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Cuestionario con MÁS aprobados
        cur.execute("""
            SELECT
                c.id AS cuestionario_id,
                c.titulo AS nombre,
                COALESCE(SUM(CASE WHEN a.aprobado THEN 1 ELSE 0 END), 0) AS total_aprobados,
                COALESCE(COUNT(a.id), 0) AS total_respuestas
            FROM cuestionario c
            LEFT JOIN alumno a ON a.cuestionario_id = c.id
            GROUP BY c.id, c.titulo
            ORDER BY total_aprobados DESC, total_respuestas DESC
            LIMIT 1;
        """)
        mas_aprob = cur.fetchone() or {
            "cuestionario_id": None,
            "nombre": None,
            "total_aprobados": 0,
            "total_respuestas": 0
        }

        # Cuestionario con MENOS aprobados
        cur.execute("""
            SELECT
                c.id AS cuestionario_id,
                c.titulo AS nombre,
                COALESCE(SUM(CASE WHEN a.aprobado THEN 1 ELSE 0 END), 0) AS total_aprobados,
                COALESCE(COUNT(a.id), 0) AS total_respuestas
            FROM cuestionario c
            LEFT JOIN alumno a ON a.cuestionario_id = c.id
            GROUP BY c.id, c.titulo
            ORDER BY total_aprobados ASC, total_respuestas ASC
            LIMIT 1;
        """)
        menos_aprob = cur.fetchone() or {
            "cuestionario_id": None,
            "nombre": None,
            "total_aprobados": 0,
            "total_respuestas": 0
        }

        cur.close()
        conn.close()

        return jsonify({
            "cuestionario_mas_aprobados": mas_aprob,
            "cuestionario_menos_aprobados": menos_aprob
        })

    except Exception as e:
        print("ERROR /estadisticas/aprobados:", e)
        return jsonify({"error": str(e)}), 500
    

@app.route("/estadisticas/alumno/<string:nombre_cuestionario>", methods=["GET"])
def estadisticas_por_nombre(nombre_cuestionario):
    try: 
        conn = get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Buscar el ID del cuestionario por el nombre
        cur.execute("""
            SELECT id 
            FROM cuestionario 
            WHERE titulo = %s
            LIMIT 1;
        """, (nombre_cuestionario,))
        row = cur.fetchone()

        if not row:
            cur.close()
            conn.close()
            return jsonify({"error": "Cuestionario no encontrado"}), 404

        cuestionario_id = row["id"]

        # Alumno con mayor puntaje
        cur.execute("""
            SELECT id, nombre, puntaje, tiempo_inicio, tiempo_final
            FROM alumno
            WHERE cuestionario_id = %s
            ORDER BY puntaje DESC
            LIMIT 1;
        """, (cuestionario_id,))
        mayor_puntaje = cur.fetchone()

        # Alumno con menor puntaje
        cur.execute("""
            SELECT id, nombre, puntaje, tiempo_inicio, tiempo_final
            FROM alumno
            WHERE cuestionario_id = %s
            ORDER BY puntaje ASC
            LIMIT 1;
        """, (cuestionario_id,))
        menor_puntaje = cur.fetchone()

        # Alumno con mayor tiempo
        cur.execute("""
            SELECT id, nombre, puntaje, tiempo_inicio, tiempo_final,
                   EXTRACT(EPOCH FROM (tiempo_final - tiempo_inicio)) AS duracion
            FROM alumno
            WHERE cuestionario_id = %s
            ORDER BY duracion DESC
            LIMIT 1;
        """, (cuestionario_id,))
        mayor_tiempo = cur.fetchone()

        # Alumno con menor tiempo
        cur.execute("""
            SELECT id, nombre, puntaje, tiempo_inicio, tiempo_final,
                   EXTRACT(EPOCH FROM (tiempo_final - tiempo_inicio)) AS duracion
            FROM alumno
            WHERE cuestionario_id = %s
            ORDER BY duracion ASC
            LIMIT 1;
        """, (cuestionario_id,))
        menor_tiempo = cur.fetchone()

        cur.close()
        conn.close()

        return jsonify({
            "cuestionario": {
                "id": cuestionario_id,
                "nombre": nombre_cuestionario
            },
            "alumno_mayor_puntaje": mayor_puntaje,
            "alumno_menor_puntaje": menor_puntaje,
            "alumno_mayor_tiempo": mayor_tiempo,
            "alumno_menor_tiempo": menor_tiempo
        })
    
    except Exception as e:
        print("ERROR /estadisticas/alumno/<string:nombre_cuestionario>:", e)
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True, port=5000)
