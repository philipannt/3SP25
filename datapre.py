import pandas as pd
import numpy as np

file_path = "D:/Python/3SP25/CHOTOT_motorcycles.csv"
df = pd.read_csv(file_path)

# df['seller_type'] = df['seller_type'].map({'Individual': 1, 'Dealer': 0})
# df['owner'] = df['owner'].apply(lambda x: 1 if x in ['1st owner'] else 0)
# valid_df = df.dropna(subset=["selling_price", "ex_showroom_price"])
# valid_df["weight"] = valid_df["selling_price"] / valid_df["ex_showroom_price"]
# avg = valid_df["weight"].mean()
# df["ex_showroom_price"] = df["ex_showroom_price"]
# df.loc[df["ex_showroom_price"].isna(), "ex_showroom_price"] = df["selling_price"] / avg
# df["name"], name_labels = pd.factorize(df["name"])

df['name'] = df['Brand'] + ' ' + df['Model']
df = df.drop(['Name', 'Max_Price', 'Brand', 'Model', 'Type', 'Engine Capacity', 'Nationality', 'Địa điểm', 'Thời gian đăng'], axis=1)
df['Price'] = df['Price'].apply(lambda x: int(x.replace('.', '').replace(' đ', '').replace('đ', '').strip()))
df['Showroom_Price'] = pd.to_numeric(df['Min_Price'].str.lower().str.replace('triệu', '').str.strip(), errors='coerce') * 1000000
df["name"], name_labels = pd.factorize(df["name"])
df['Kilometer Driven'] = df['Kilometer Driven'].replace('Không có thông tin', np.nan)
df['Kilometer Driven'] = pd.to_numeric(df['Kilometer Driven'], errors='coerce')
for col in df.select_dtypes(include=[np.number]).columns:
    df[col] = df[col].fillna(df[col].mean())

df['name'] = df['Brand'] + ' ' + df['Model']
df = df.drop(['Name', 'Max_Price', 'Brand', 'Model', 'Địa điểm', 'Thời gian đăng'], axis=1)


print(df.head())

output_path = "BIKE_DETAILS.csv"
df.to_csv(output_path, index=False)
print("Done.")