import pandas as pd
from sqlalchemy import create_engine

def preprocess_data():
    engine = create_engine(
        "mysql+pymysql://penguins_user:penguins_pass@mysql-data:3306/penguins_db"
    )

    df = pd.read_sql("SELECT * FROM penguins_raw", con=engine)

    df = df.drop(columns=["id"], errors="ignore")
    df = df.dropna()

    df.to_sql("penguins_clean", con=engine, if_exists="replace", index=False)

    print(f"Se guardaron {len(df)} filas en penguins_clean")
