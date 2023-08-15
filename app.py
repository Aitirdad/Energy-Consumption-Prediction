import pandas as pd
import numpy as np
import streamlit as st
import joblib
columns = ['PJME_MW', 'hour', 'dayofweek', 'quarter', 'month', 'year', 'dayofyear', 'dayofmonth', 'weekofyear', 'lag1', 'lag2', 'lag3']
model = joblib.load('my_model.joblib')
st.title('Give me some time to tell you how much energy you use⚡')
start = st.text_input("Start Date⌚", "2002-12-31 01:00:00")
end = st.text_input("End Date⌚", "2002-12-31 01:00:00")
df = pd.DataFrame(columns=columns)
def create_features(df):
    df = df.copy()
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day
    df['weekofyear'] = df.index.isocalendar().week
    return df
def add_lags(df):
    df['lag1'] = (df.index - pd.Timedelta('364 days'))
    df['lag2'] = (df.index - pd.Timedelta('728 days'))
    df['lag3'] = (df.index - pd.Timedelta('1092 days'))
    return df
future = pd.date_range(start=start, end=end, freq='1h')
future_df = pd.DataFrame(index=future)
df_and_future = create_features(future_df)
df_and_future = add_lags(df_and_future)
def predict():
    global leaf_index
    if leaf_index < len(model.get_dump()):
        leaf_output = model.get_dump()[leaf_index][127:137]
        st.write("Prediction from leaf", leaf_index, ":", leaf_output, "MegaWatts⚡")
        leaf_index += 1
    else:
        st.write("No more leaves to display.")

leaf_index = 0
trigger = st.button('Predict', on_click=predict)