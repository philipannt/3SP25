import os
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("Missing database credentials. Please check your .env file.")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

file_path = "honda.csv"
df = pd.read_csv(file_path)

df.dropna(inplace=True)
df["price"] = df["price"].astype(float)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print("Data after preprocessing:")
print(df.head())

table_name = "processed_data"
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"✅ Data successfully committed to Aiven MySQL ({DB_NAME}) in table `{table_name}`!")