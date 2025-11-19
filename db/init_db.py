import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="quizzes",
    user="postgres",
    password="13postgre22"
)

cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS cuestionario (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS pregunta (
    id SERIAL PRIMARY KEY,
    pregunta TEXT NOT NULL,
    respuesta_correcta TEXT NOT NULL,
    opcion1 TEXT NOT NULL,
    opcion2 TEXT NOT NULL,
    cuestionario_id INT NOT NULL,
    FOREIGN KEY (cuestionario_id) REFERENCES cuestionario(id) ON DELETE CASCADE
);
""")

conn.commit()
cur.close()
conn.close()

print("BD lista con ambas tablas.")
