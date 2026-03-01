

## Arquitectura general

El proyecto está compuesto por los siguientes servicios:

- **PostgreSQL**: almacena los metadatos de Airflow.
- **MySQL**: almacena los datos del pipeline (`penguins_raw` y `penguins_clean`).
- **Airflow Webserver**: interfaz gráfica de Airflow.
- **Airflow Scheduler**: ejecuta y programa las tareas del DAG.
- **FastAPI**: expone endpoints de inferencia para los modelos entrenados.

---

## Flujo del pipeline

El DAG `penguins_pipeline` ejecuta las siguientes tareas en secuencia:

1. **truncate_raw_table**  
   Limpia la tabla `penguins_raw`.

2. **load_raw_penguins**  
   Carga el archivo `penguins.csv` en la tabla `penguins_raw`.

3. **preprocess_penguins**  
   Lee los datos desde `penguins_raw`, realiza el preprocesamiento y guarda el resultado en `penguins_clean`.

4. **train_model** o **train_models**  
   Lee los datos preprocesados, entrena el modelo o los modelos y guarda los artefactos necesarios para inferencia.

---

## Estructura del proyecto

```bash
AIRFLOW/
├── api/
│   └── app.py
├── dags/
│   └── penguins_pipeline.py
├── data/
│   └── penguins.csv
├── logs/
├── models/
│   ├── randomforest_model.pkl
│   ├── svm_model.pkl
│   ├── gradientboosting_model.pkl
│   ├── scaler.pkl
│   ├── penguins_rf.pkl
│   └── penguins_features.pkl
├── plugins/
├── report/
│   └── model_metrics.pkl
├── src/
│   ├── load_raw_penguins.py
│   ├── preprocess_data.py
│   ├── train_model.py
│   └── train_models.py
├── requirements.txt
├── requirements.api.txt
├── README.md
└── docker/
    ├── Dockerfile
    ├── Dockerfile.api
    └── docker-compose.yml

```
---
## Tecnologias utilizadas

- Python 3.11
- Apache Airflow 2.10.5
- FastAPI
- Uvicorn
- MySQL 8
- PostgreSQL 15
- SQLAlchemy
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Docker
- Docker Compose

---

## Bases de datos utilizadas

### 1. Base de datos de metadatos de Airflow
Se utiliza **PostgreSQL** para almacenar:

- DAG runs
- estados de tareas
- usuarios
- conexiones
- configuracion interna de Airflow

### 2. Base de datos de datos del proyecto
Se utiliza **MySQL** para almacenar:

- `penguins_raw`
- `penguins_clean`

De esta forma se cumple el requerimiento de mantener separadas las bases de datos del negocio y los metadatos de Airflow.

---

## Parametros de conexion a bases de datos

### PostgreSQL - Metadatos de Airflow

- **Motor**: PostgreSQL
- **Contenedor**: `airflow-postgres`
- **Puerto host**: `5433`
- **Puerto contenedor**: `5432`
- **Base de datos**: `airflow`
- **Usuario**: `airflow`
- **Contrasena**: `airflow`

Cadena de conexion usada por Airflow:

```text
postgresql+psycopg2://airflow:airflow@postgres/airflow
```

### MySQL - Datos del proyecto

- **Motor**: MySQL 8
- **Contenedor**: `mysql-penguins`
- **Puerto host**: `3307`
- **Puerto contenedor**: `3306`
- **Base de datos**: `penguins_db`
- **Usuario aplicacion**: `penguins_user`
- **Contrasena aplicacion**: `penguins_pass`
- **Usuario root**: `root`
- **Contrasena root**: `root`

Cadena de conexion usada en los scripts Python:

```text
mysql+pymysql://penguins_user:penguins_pass@mysql-data:3306/penguins_db
```

---

## Como levantar el proyecto desde cero

### 1. Ubicarse en la carpeta `docker`

```bash
cd docker
```

### 2. Levantar todos los servicios

```bash
docker compose up --build -d
```

### 3. Verificar contenedores activos

```bash
docker ps
```

Deben verse los siguientes servicios:

- `airflow-postgres`
- `mysql-penguins`
- `airflow-webserver`
- `airflow-scheduler`
- `penguins-api`

> El contenedor `airflow-init` puede ejecutarse una sola vez y luego detenerse, lo cual es normal.

---

## Acceso a servicios

### Airflow

URL:

```text
http://localhost:8080
```

Credenciales:

- **usuario**: `airflow`
- **contrasena**: `airflow`

### API

URL:

```text
http://localhost:8000
```

---

## Creacion manual de tablas en MySQL

Despues de levantar los contenedores, se deben crear las tablas del proyecto en MySQL.

### 1. Entrar al contenedor de MySQL

```bash
docker exec -it mysql-penguins mysql -u root -p
```

Contrasena:

```text
root
```

### 2. Seleccionar la base de datos

```sql
USE penguins_db;
```

### 3. Crear la tabla `penguins_raw`

```sql
CREATE TABLE penguins_raw (
    id INT AUTO_INCREMENT PRIMARY KEY,
    species VARCHAR(50),
    island VARCHAR(50),
    bill_length_mm FLOAT,
    bill_depth_mm FLOAT,
    flipper_length_mm FLOAT,
    body_mass_g FLOAT,
    sex VARCHAR(20)
);
```

### 4. Crear la tabla `penguins_clean`

```sql
CREATE TABLE penguins_clean (
    id INT AUTO_INCREMENT PRIMARY KEY,
    species VARCHAR(50),
    island VARCHAR(50),
    bill_length_mm FLOAT,
    bill_depth_mm FLOAT,
    flipper_length_mm FLOAT,
    body_mass_g FLOAT,
    sex VARCHAR(20)
);
```

### 5. Verificar tablas creadas

```sql
SHOW TABLES;
```

Salida esperada:

```text
+-----------------------+
| Tables_in_penguins_db |
+-----------------------+
| penguins_clean        |
| penguins_raw          |
+-----------------------+
```

### 6. Salir de MySQL

```sql
exit;
```

---

## Como crear la conexion en Airflow

Para que Airflow pueda conectarse a MySQL y ejecutar la tarea `truncate_raw_table`, se debe crear una conexion manualmente en la interfaz.

### Ruta en la interfaz

- Entrar a Airflow
- Ir a **Admin**
- Ir a **Connections**
- Clic en **+**

### Parametros de la conexion

- **Conn Id**: `mysql_penguins`
- **Conn Type**: `MySQL`
- **Host**: `mysql-data`
- **Schema**: `penguins_db`
- **Login**: `penguins_user`
- **Password**: `penguins_pass`
- **Port**: `3306`

### Resumen de la conexion

```text
Conn Id: mysql_penguins
Conn Type: MySQL
Host: mysql-data
Schema: penguins_db
Login: penguins_user
Password: penguins_pass
Port: 3306
```

---

## Tablas del proyecto

### `penguins_raw`
Tabla que almacena los datos crudos cargados desde el archivo CSV.

### `penguins_clean`
Tabla que almacena los datos preprocesados que luego son usados para entrenar el modelo.

---

## Modelos entrenados

Dependiendo de la version del proyecto, se pueden usar uno o varios modelos.

### Version multi-modelo

- `randomforest_model.pkl`
- `svm_model.pkl`
- `gradientboosting_model.pkl`
- `scaler.pkl`
- `report/model_metrics.pkl`

---

## API de inferencia

La API fue desarrollada con **FastAPI** y permite realizar predicciones sobre nuevas observaciones.

### URL base

```text
http://localhost:8000
```

### Endpoint raiz

```http
GET /
```

Respuesta esperada:

```json
{
  "message": "Penguin Classifier API funcionando"
}
```

### Endpoint para listar modelos

```http
GET /models
```

Respuesta esperada:

```json
{
  "available_models": [
    {
      "name": "randomforest",
      "model": "Random Forest Classifier",
      "metrics": {
        "train_accuracy": 0.99,
        "test_accuracy": 0.97,
        "test_precision": 0.97,
        "test_recall": 0.97,
        "test_f1": 0.97
      },
      "endpoint": "POST /classify/randomforest"
    }
  ]
}
```

> Los valores exactos de metricas dependen del entrenamiento realizado.

### Endpoint de clasificacion

```http
POST /classify/{model_name}
```

Ejemplos validos de `model_name`:

- `randomforest`
- `svm`
- `gradientboosting`

### Parametros de entrada de la API

La API recibe un JSON con los siguientes campos:

| Parametro | Tipo | Descripcion |
|----------|------|-------------|
| `island` | integer | Codigo numerico de la isla |
| `bill_length_mm` | float | Longitud del pico en milimetros |
| `bill_depth_mm` | float | Profundidad del pico en milimetros |
| `flipper_length_mm` | integer | Longitud de la aleta en milimetros |
| `body_mass_g` | integer | Masa corporal en gramos |
| `sex` | integer | Codigo numerico del sexo |
| `year` | integer | Ano del registro |

### Ejemplo de entrada

```json
{
  "island": 1,
  "bill_length_mm": 50.0,
  "bill_depth_mm": 15.0,
  "flipper_length_mm": 220,
  "body_mass_g": 5000,
  "sex": 1,
  "year": 2007
}
```

### Ejemplo de consulta a la API

#### Random Forest

```bash
curl -X POST "http://localhost:8000/classify/randomforest" \
-H "Content-Type: application/json" \
-d '{
  "island": 1,
  "bill_length_mm": 50.0,
  "bill_depth_mm": 15.0,
  "flipper_length_mm": 220,
  "body_mass_g": 5000,
  "sex": 1,
  "year": 2007
}'
```

#### SVM

```bash
curl -X POST "http://localhost:8000/classify/svm" \
-H "Content-Type: application/json" \
-d '{
  "island": 1,
  "bill_length_mm": 50.0,
  "bill_depth_mm": 15.0,
  "flipper_length_mm": 220,
  "body_mass_g": 5000,
  "sex": 1,
  "year": 2007
}'
```

#### Gradient Boosting

```bash
curl -X POST "http://localhost:8000/classify/gradientboosting" \
-H "Content-Type: application/json" \
-d '{
  "island": 1,
  "bill_length_mm": 50.0,
  "bill_depth_mm": 15.0,
  "flipper_length_mm": 220,
  "body_mass_g": 5000,
  "sex": 1,
  "year": 2007
}'
```

### Ejemplo de salida

```json
{
  "model": "randomforest",
  "species_id": 2,
  "species_name": "Chinstrap"
}
```

> La especie predicha puede cambiar segun los valores enviados y el modelo usado.

---

## Ejecucion del DAG

1. Ingresar a Airflow.
2. Buscar el DAG `penguins_pipeline`.
3. Activarlo.
4. Ejecutarlo manualmente con **Trigger DAG**.

