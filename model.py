import joblib

import pandas as pd
import numpy as np

from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

def read_data():
    file_path = "E:/Python/3SP25/BIKE DETAILS.csv"
    df = pd.read_csv(file_path)
    return df

def encode_data():
    df = read_data()
    
    df['seller_type'] = df['seller_type'].map({'Individual': 1, 'Dealer': 0})
    df['owner'] = df['owner'].apply(lambda x: 1 if x == '1st owner' else 0)

    valid = df.dropna(subset=["selling_price", "ex_showroom_price"]).copy()
    valid["weight"] = valid["selling_price"] / valid["ex_showroom_price"]
    avg_weight = valid["weight"].mean()

    mask = df["ex_showroom_price"].isna() & df["selling_price"].notna()
    df.loc[mask, "ex_showroom_price"] = df.loc[mask, "selling_price"] / avg_weight

    df["name"], name_labels = pd.factorize(df["name"])
    joblib.dump(name_labels, 'name_labels.pkl')

    # print(df.head())

    return df

def training_model():
    df = encode_data()
    
    X = df.drop(columns=['selling_price'])
    y = df['selling_price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f'MSE: {mse}')
    print(f'R2 Score: {r2}')

    joblib.dump(model, 'bike_price_model.pkl')

def preprocess_input(user_input):
    name_labels = joblib.load('name_labels.pkl')
    
    input_df = pd.DataFrame([user_input])
    input_df['name'] = name_labels.get_indexer([input_df['name'][0]])

    input_df['seller_type'] = 1 if user_input['seller_type'] == 'Individual' else 0
    input_df['owner'] = 1 if user_input['owner'] == '1st owner' else 0

    numeric_cols = ['year', 'km_driven', 'ex_showroom_price']
    for col in numeric_cols:
        input_df[col] = pd.to_numeric(input_df[col], errors='coerce').fillna(0)

    return input_df[['name', 'year', 'seller_type', 'owner', 'km_driven', 'ex_showroom_price']]

def predict_price(data_input):
    model = joblib.load('bike_price_model.pkl')
    input_df = preprocess_input(data_input)
    return model.predict(input_df)[0]

def main():
    training_model()

    data_input = {
        'year': '2016',
        'km_driven': '21100',
        'name': 'Honda Future',
        'ex_showroom_price': '50000000',
        'seller_type': 'Individual',
        'owner': '1st owner',
    }

    price = predict_price(data_input)
    print(f"Giá xe dự đoán: {price:,.0f} VNĐ")

if __name__ == '__main__':
    main()