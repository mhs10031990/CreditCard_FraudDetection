import streamlit as st
import streamlit.components.v1 as components
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
    #st.write("Work in Progress")
    HtmlFile = open("data_profile.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)

with tab2:
  
    image2 = Image.open('randforest_model_with_smote.png')
    image3 = Image.open('reandom_forest_with_smote_ROC_AUC.png')
    #image4 = Image.open('randforest_model_with_smote.png')
    #image5 = Image.open('reandom_forest_with_smote_ROC_AUC.png')
    
    st.image(image2)
    st.write("#")
    st.image(image3)
    st.write("#")
    #st.image(image4)
    #st.write("#")
    #st.image(image5)

    #col1, col2 = st.columns(2)
    
    #with col1:
    #    st.header('Model Confusion Metrics')
    #    st.image(image2)

    #with col2:
    #    st.header('Model ROC/AUC')
    #    st.image(image3)

    #col3, col4 = st.columns(2)
    
    #with col3:
    #    st.header('Tuned Model Confusion Metrics')
    #    st.image(image4)

    #with col4:
    #    st.header('Tuned Model ROC/AUC')
    #    st.image(image5)
    
with tab3:
    if check_prediction > 0:
        #st.text_input("Raw Input", payload)
        headers={"Content-type":"application/json"}
        url = 'http://svc-8b6ea9ed-6c00-464a-a1a1-63529b992d58:5001/ccfrauddetectionmodel/6d176a03-54ee-4d02-ae2d-c588311e3967/score'
        score_input = {"payload" : payload}
        st.text_input("Model Payload", score_input)
        response_json = requests.post(url, json=score_input, headers=headers)
        #st.text_input("API Response: ",response_json.content)
        response = response_json.json()
        try:
            output1 = response['data']
            st.text_input ('Binary Model Output: ',output1)
        except ValueError:
            output1 =  response.status_code 
            st.text_input ('Oops we got an error: ',output1)
        st.write("#")
    else:
        st.write("Submit to check the model prediction")
