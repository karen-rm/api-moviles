import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()  

print("Conectando a la base de datos...")

conn = psycopg2.connect(
    host= os.getenv("DB_HOST"),
    port= os.getenv("DB_PORT"),
    dbname= os.getenv("DB_NAME"),
    user= os.getenv("DB_USER"),
    password= os.getenv("DB_PASSWORD"),
    sslmode= os.getenv("DB_SSLMODE")
)

cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS cuestionario (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    codigo VARCHAR(8)
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


cur.execute("""
CREATE TABLE IF NOT EXISTS alumno (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    puntaje INT NOT NULL,
    tiempo_inicio TIMESTAMP NOT NULL,
    tiempo_final TIMESTAMP NOT NULL,
    aprobado BOOLEAN NOT NULL,
    cuestionario_id INT NOT NULL,
    FOREIGN KEY (cuestionario_id) REFERENCES cuestionario(id) ON DELETE CASCADE
);
""")

conn.commit()
cur.close()
conn.close()

print("¡BD lista con todas las tablas creadas exitosamente!")