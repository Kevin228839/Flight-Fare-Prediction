# Flight fare prediction
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

# Preprocessing
# import dataset
df_train = pd.read_excel("Data_Train.xlsx")

# drop null value
df_train.dropna(inplace=True)

# drop duplicates
df_train.drop_duplicates(keep='first', inplace=True)

# convert Dep_Time and Arrival_Time into hour and minute
# Dep_Time
df_train["Dep_hour"] = pd.to_datetime(df_train["Dep_Time"]).dt.hour
df_train["Dep_minute"] = pd.to_datetime(df_train["Dep_Time"]).dt.minute
df_train = df_train.drop(columns="Dep_Time")

# Arrival_Time
df_train["Arr_hour"] = pd.to_datetime(df_train["Arrival_Time"]).dt.hour
df_train["Arr_minute"] = pd.to_datetime(df_train["Arrival_Time"]).dt.minute
df_train = df_train.drop(columns="Arrival_Time")

# convert Date_of_Journey into timestamp
df_train["Date_of_Journey_Year"] = pd.to_datetime(
    df_train["Date_of_Journey"], format="%d/%m/%Y").dt.year
# ps. I don't think "year" is mandatory
df_train["Date_of_Journey_Month"] = pd.to_datetime(
    df_train["Date_of_Journey"], format="%d/%m/%Y").dt.month
df_train["Date_of_Journey_Day"] = pd.to_datetime(
    df_train["Date_of_Journey"], format="%d/%m/%Y").dt.day
df_train = df_train.drop(columns="Date_of_Journey")


# convert Duration into minute
df_train['Duration'] = df_train['Duration']\
    .str.replace("h", '*60')\
    .str.replace(' ', '+')\
    .str.replace('m', '*1')\
    .apply(eval)

# Encode categorical attributes

# Select categorical data
df_train_categorical = df_train[['Airline', 'Source', 'Destination']]
df_train.drop(["Airline","Source", "Destination"], axis=1, inplace=True)

# Use OneHotEncoder
df_train_categorical = pd.get_dummies(df_train_categorical, drop_first=True)

# Concat categorical and numerical data
train_preprocessed = pd.concat([df_train, df_train_categorical], axis=1)
train_target = df_train['Price']

# Drop 'Price' because price is the target variable
train_preprocessed.drop(['Price'], axis=1, inplace=True)




# -----Preprocess Test Set------
# Import dataset
df_test = pd.read_excel("Test_set.xlsx")
df_test.dropna(inplace=True)
df_test.drop_duplicates(keep='first', inplace=True)

# Convert time
df_test["Dep_hour"] = pd.to_datetime(df_test["Dep_Time"]).dt.hour
df_test["Dep_minute"] = pd.to_datetime(df_test["Dep_Time"]).dt.minute
df_test = df_test.drop(columns="Dep_Time")

df_test["Arr_hour"] = pd.to_datetime(df_test["Arrival_Time"]).dt.hour
df_test["Arr_minute"] = pd.to_datetime(df_test["Arrival_Time"]).dt.minute
df_test = df_test.drop(columns="Arrival_Time")

df_test["Date_of_Journey_Year"] = pd.to_datetime(
    df_test["Date_of_Journey"], format="%d/%m/%Y").dt.year
df_test["Date_of_Journey_Month"] = pd.to_datetime(
    df_test["Date_of_Journey"], format="%d/%m/%Y").dt.month
df_test["Date_of_Journey_Day"] = pd.to_datetime(
    df_test["Date_of_Journey"], format="%d/%m/%Y").dt.day
df_test = df_test.drop(columns="Date_of_Journey")

df_test['Duration'] = df_test['Duration']\
    .str.replace("h", '*60')\
    .str.replace(' ', '+')\
    .str.replace('m', '*1')\
    .apply(eval)

# Encode categorical attributes
df_test_categorical = df_test[['Airline', 'Source', 'Destination']]
df_test.drop(["Airline","Source", "Destination"], axis=1, inplace=True)
df_test_categorical = pd.get_dummies(df_test_categorical, drop_first=True)
test_preprocessed = pd.concat([df_test, df_test_categorical], axis=1)
