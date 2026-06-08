# API QUIZZ

## Descripción 
Este repositorio se trata de una API REST desarrollada con Flask y desplegada en Railway que centraliza la lógica de negocio y la comunicación entre las aplicaciones compañeras MakeAQuizz y TakeAQuizz.

La API expone endpoints HTTP (GET, POST, PUT y DELETE) para gestionar usuarios, cuestionarios, preguntas y resultados, realizando operaciones CRUD sobre una base de datos 
PostgreSQL alojada en Railway.

- MakeAQuizz: https://github.com/karen-rm/make-a-quizz
<br>

## Endpoints 
#### [POST] CREATE QUIZZ 
<img width="769" height="541" alt="cuestionarios" src="https://github.com/user-attachments/assets/a4394220-5d74-47d2-b8c5-f1089e5bf205" />
<br><hr>

#### [GET] GET QUIZZES 
<img width="762" height="623" alt="cuestionariosGET" src="https://github.com/user-attachments/assets/9701da71-f650-4f47-a778-eda91bb54a26" />
<br><hr>

#### [POST] UPDATE QUIZZ 
<img width="767" height="560" alt="CuestionariosPUT" src="https://github.com/user-attachments/assets/c076bdc0-2594-4de6-b865-8551184e51ae" />
<br><hr>

#### [DELETE] DELETE QUIZZ 
<img width="769" height="502" alt="cuestionariosDELETE" src="https://github.com/user-attachments/assets/7e8e890a-f838-46ee-b8a8-e8ef0a0e10fe" />

#### [GET] GET QUIZZ
<img width="765" height="536" alt="CustionariosIdGET" src="https://github.com/user-attachments/assets/eddcc9fc-e23a-4d28-b88b-add36f04c191" />
<br><hr>

#### [POST] ADD QUESTION 
<img width="765" height="616" alt="CuestionariosIdPreguntasPOST" src="https://github.com/user-attachments/assets/158f3ef2-bc72-4161-9271-826ee002f3a6" />

#### [GET] GET QUESTIONS
<img width="769" height="612" alt="CustionariosIdPreguntasGET" src="https://github.com/user-attachments/assets/4200d97a-6e2b-4680-9d25-aa29879f9651" />
<br><hr>

#### [DELETE] DELETE QUESTIONS
<img width="766" height="521" alt="CustionariosIdPreguntasDELETE" src="https://github.com/user-attachments/assets/7c5b4c11-7cb1-45ad-8798-7ded7cfe8b19" />
<br><hr>

#### [PUT] UPDATE QUESTIONS
<img width="760" height="485" alt="image" src="https://github.com/user-attachments/assets/a88a6d87-98ac-4683-958a-b9f786157298" />
<br><hr>

#### [DELETE] DELETE QUESTIONS 
<img width="763" height="479" alt="image" src="https://github.com/user-attachments/assets/c1ac6108-9d26-4f81-88ef-19e530fe2fc1" />
<br><hr>

#### [GET] GET STATISTICS OF APPROVED STUDENTS 
<img width="769" height="555" alt="image" src="https://github.com/user-attachments/assets/141a302b-2dbf-45c0-858d-2ed7f29fc9b0" />
<br><hr>

## Arquitectura 
API monolítica  está desarrollada con Flask y sigue una arquitectura REST orientada a recursos. 
Los endpoints reciben solicitudes HTTP, procesan la lógica necesaria y ejecutan consultas sobre una base de datos PostgreSQL alojada en Railway.

<b>Recursos principales</b>
- Cuestionarios
- Preguntas
- Alumnos
- Estadísticas
  
### Operaciones soportadas
- GET: Consulta de información.
- POST: Creación de recursos.
- PUT: Actualización de recursos existentes.
- DELETE: Eliminación de recursos.
  
  <br><br>
#### API DESPLEGADA EN RAILWAY 
<img width="817" height="382" alt="image" src="https://github.com/user-attachments/assets/f69e23b9-9301-4123-b16a-d9de94cdf31f" />
<br>

## Tecnologias
- Flask
- Python
- Postman 
- PostgreSQL


## Instalación 

#### Nota de Despliegue: 
Esta API ya no se encuentra disponible públicamente en Railway. Sin embargo, el código es completamente funcional. Puedes clonar este repositorio para probar los endpoints en tu máquina local (localhost) o utilizarlo para desplegar tu propia instancia en el servicio en la nube de tu preferencia.

#### Requisitos Previos
- Python 3.8+ instalado.
- PostgreSQL corriendo localmente (puedes usar Docker o pgAdmin).
- (Recomendado) Postman o Insomnia para probar los endpoints.

#### Pasos para levantar la API localmente
1. Clonar el repositorio
Abre tu terminal y ejecuta:

```bash
git clone https://github.com/karen-rm/api-moviles.git
```
```bash
cd api-moviles
```

2. Crear y activar un entorno virtual (Recomendado)
Para mantener las dependencias aisladas, crea un entorno virtual:

En Windows:
```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```

En Mac/Linux:
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```

3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

4. Configurar las Variables de Entorno 
Crea un archivo llamado .env en la raíz del proyecto y agrega tus credenciales de PostgreSQL. Asegúrate de que los datos coincidan con tu base de datos (Sigue el ejemplo del .envexample):

##### Variables para la API
- PGHOST
- PGPORT
- PGDATABASE
- PGUSER
- PGPASSWORD

#### Variables para la Base de Datos
- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_SSLMODE

5. Inicializar la Base de Datos
Antes de correr la API, debes crear las tablas (cuestionario, pregunta, alumno). Ejecuta el script de inicialización:

```bash
python db/init_db.py
```
(Si todo sale bien, verás el mensaje: "BD lista con todas las tablas creadas exitosamente").

6. Ejecutar el servidor Flask (en caso de hacerlo localmente)
Finalmente, levanta la API:

```bash
python app.py
```
La API estará corriendo y lista para recibir peticiones en: http://127.0.0.1:5000
