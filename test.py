import psycopg2

print("Intentando conectar con psycopg2...")

try:
    # Pasamos los datos directos en una sola línea para evitar problemas de formato
    conn = psycopg2.connect("host=127.0.0.1 port=5433 dbname=postgres user=postgres password=1234 sslmode=disable")
    print("¡Éxito! psycopg2 logró conectarse.")
    conn.close()
except Exception as e:
    print("El error original que psycopg2 intentaba ocultar es:")
    print(repr(e)) # repr() fuerza a imprimir crudo sin importar los acentos