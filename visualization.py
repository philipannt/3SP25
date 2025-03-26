import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import validation_curve
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from xgboost import XGBRegressor
from scipy.stats import kurtosis, skew

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import keras
import tensorflow as tf
from keras.src.callbacks import EarlyStopping, ReduceLROnPlateau

from time import time

from warnings import simplefilter
simplefilter("ignore")

data = pd.read_json('E:/Python/3SP25/CHOTOT.json')
data.drop_duplicates(inplace=True)