import pandas as pd
import joblib
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def train_model():
    engine = create_engine(
        "mysql+pymysql://penguins_user:penguins_pass@mysql-data:3306/penguins_db"
    )

    df = pd.read_sql("SELECT * FROM penguins_clean", con=engine)

    if "id" in df.columns:
        df = df.drop(columns=["id"])

    X = df.drop(columns=["species"])
    y = df["species"]

    X = pd.get_dummies(X, drop_first=True)

    feature_columns = X.columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, "/opt/airflow/models/penguins_rf.pkl")
    joblib.dump(feature_columns, "/opt/airflow/models/penguins_features.pkl")

    print("Modelo entrenado y guardado")
    print("Columnas guardadas en /opt/airflow/models/penguins_features.pkl")
