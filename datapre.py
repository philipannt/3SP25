import pandas as pd

file_path = "D:/Python/3SP25/BIKE DETAILS.csv"
df = pd.read_csv(file_path)

df['seller_type'] = df['seller_type'].map({'Individual': 1, 'Dealer': 0})
df['owner'] = df['owner'].apply(lambda x: 1 if x in ['1st owner'] else 0)

valid_df = df.dropna(subset=["selling_price", "ex_showroom_price"])
valid_df["weight"] = valid_df["selling_price"] / valid_df["ex_showroom_price"]
avg = valid_df["weight"].mean()

df["ex_showroom_price"] = df["ex_showroom_price"]
df.loc[df["ex_showroom_price"].isna(), "ex_showroom_price"] = df["selling_price"] / avg

df["name"], name_labels = pd.factorize(df["name"])

print(df.head())

output_path = "BIKE_DETAILS.csv"
df.to_csv(output_path, index=False)
print("Done.")