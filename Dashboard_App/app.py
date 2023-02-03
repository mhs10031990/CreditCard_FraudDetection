import streamlit as st
import streamlit.components.v1 as components
from prediction import binary_model
import pandas as pd
import requests
import json

st.set_page_config(page_title="Refract",layout="wide", page_icon="")
st.header("Credit Card Fraud Detection Application")
st.write("These days every business suffers from the fraud. Not a single business is fully immune to fraud. The business problem is to detect credit card fraud transcation from millions of transaction")
output1 = ""
check_prediction  = 0

with st.sidebar:
    from PIL import Image
    image = Image.open('refract.png')

    st.image(image)
    st.sidebar.header("Adjust your inputs")

    amount = st.slider('Amount in INR', 1, 5000000, 50000)
    location = st.selectbox('Choose your location',('Karnataka','Tamil Nadu','Jharkhand','Gujurat','Maharashtra','Haryana','West Bengal')) 
    age = st.slider('Customer Age', 18, 70, 1)
    hour = st.slider('select hour', 1, 24, 1)
    day = st.slider('Starts sunday as 1', 1, 7, 1)
    month = st.slider('Select month', 1, 12, 1)
    category = st.radio('Transaction type',('grocery','miscellanous','others'))

    if st.button('Predict'):
        check_prediction = 1            
        if category == 'grocery':
            temp_category = 'grocery_pos'
        else:
            temp_category = 'misc_net' 
    
        payload = [amount, 28611, 35.9946, -81.7266, 880000, 36.430124, -81.17948299999998, age, hour, day, month, temp_category]
        
    else :
        st.write('Please submit once you are ready!')

tab1, tab2, tab3 = st.tabs(["Data Profile", "Insights", "Prediction"])
with tab1:
    HtmlFile = open("data_profile.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)

with tab2:
    image1 = Image.open('Target_Without_SMOTE.png')
    image2 = Image.open('Target_With_SMOTE.png')

    col1, col2 = st.columns(2)
    col1.image(image1, caption='Original Target distribution')
    col2.image(image2, caption='SMOTE Target distribution')
    st.write("#")

    image3 = Image.open('randforest_model_no_smote.png')
    image4 = Image.open('randforest_model_with_smote.png')

    col3, col4 = st.columns(2)
    col3.image(image3, caption='Original Model Metrics')
    col4.image(image4, caption='SMOTE Model Metrics')
    st.write("#")

    image5 = Image.open('reandom_forest_no_smote_ROC_AUC.png')
    image6 = Image.open('reandom_forest_with_smote_ROC_AUC.png')

    col5, col6 = st.columns(2)
    col5.image(image5, caption='Original Model ROC/AUC')
    col6.image(image6, caption='SMOTE Model ROC/AUC')
    st.write("#")    


with tab3:
    if check_prediction == 1:
        st.text_input("Raw Input", payload)
        headers={"Content-type":"application/json"}
        url = 'http://svc-090535dc-7b28-45c0-ae26-cf4b6523c34f:5001/creditcardfrauddetectionmodel/8adb1856-5c6a-45bd-93bf-1e0c568e8e59/score'
        score_input = {"payload" : payload}
        st.text_input("Model Payload", score_input)
        response_json = requests.post(url, json=score_input, headers=headers)
        st.text_input("API Response: ",response_json.content)
        response = response_json.json()
        try:
            output1 = response['upload_logging_data']['response_data']
            st.text_input ('Binary Model Output: ',output1)
        except ValueError:
            output1 =  response.status_code 
            st.text_input ('Oops we got an error: ',output1)
        st.write("#")
    else:
        st.write("Submit to check the model prediction")

