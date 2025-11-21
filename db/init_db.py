import psycopg2

conn = psycopg2.connect(
    host="ballast.proxy.rlwy.net",
    port=30634,
    dbname="railway",
    user="postgres",
    password="fmLDYpkxrKDAHWOLTiAyWzDQQLuPxxsl",
    sslmode="require"
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
