import pandas as pd
from sqlalchemy import create_engine

def load_raw_penguins():
    df = pd.read_csv("/opt/airflow/data/penguins.csv")

    engine = create_engine(
        "mysql+pymysql://penguins_user:penguins_pass@mysql-data:3306/penguins_db"
    )

    df = df[[
        "species",
        "island",
        "bill_length_mm",
        "bill_depth_mm",
        "flipper_length_mm",
        "body_mass_g",
        "sex"
    ]]

    df.to_sql("penguins_raw", con=engine, if_exists="append", index=False)

    print(f"Se cargaron {len(df)} filas en penguins_raw")

