

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


