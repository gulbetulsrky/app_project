import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import OrdinalEncoder
from PIL import Image

html_temp = """
<div style="background-color:blue;padding:10px">
<h2 style="color:white;text-align:center;">Used Car Price Estimation </h2>
</div>"""
st.markdown(html_temp,unsafe_allow_html=True)
img = Image.open("used-car-maintenance.png")
st.image(img, caption="We calculate the price of your vehicle in the most accurate way. ",width=600)
st.markdown("Enter the features of your car in the sidebar and learn its price!")

st.sidebar.title('Car Price Prediction')



age=st.sidebar.selectbox("What is the age of your car:",(0,1,2,3,4))
hp=st.sidebar.slider("What is the hp of your car?", 60, 200, step=5)
km=st.sidebar.slider("What is the km of your car", 0,200000, step=500)
gearing_type=st.sidebar.radio('Select gear type',('Automatic','Semi-automatic','Manual'))
car_model=st.sidebar.selectbox("Select model of your car", ('Audi A1', 'Audi A3', 'Opel Astra', 'Opel Corsa', 'Opel Insignia',
       'Renault Clio', 'Dacia Duster', 'Renault Espace'))

model=pickle.load(open("xgbmodel_autoscout","rb"))

my_dict = {
    "age": age,
    "hp_kW": hp,
    "make_model": car_model,
    "km": km,
    'gearing_type':gearing_type
}

df = pd.DataFrame.from_dict([my_dict])


st.header("The configuration of your car is below")
st.table(df)

def ordienc(df):
    gear = ['Automatic', 'Semi-automatic', 'Manual']
    mmodel = ['Audi A1', 'Audi A3', 'Opel Astra', 'Opel Corsa', 'Opel Insignia',
       'Renault Clio', 'Dacia Duster', 'Renault Espace']
    enc = OrdinalEncoder(categories=[mmodel, gear])
    df[['make_model', 'gearing_type']] = enc.fit_transform(df[['make_model', 'gearing_type']])

    return df

ordienc(df)


st.subheader("Press predict if configuration is okay")

if st.button("Predict"):
    prediction = model.predict(df)
    st.success("The estimated price of your car is €{}. ".format(int(prediction[0])))

