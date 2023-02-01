import streamlit as st
import pandas as pd
import requests
import json

# @st.experimental_memo
def binary_model(payload):
    
    headers={"Content-type":"application/json"}
    url = 'http://svc-090535dc-7b28-45c0-ae26-cf4b6523c34f:5001/creditcardfrauddetectionmodel/8adb1856-5c6a-45bd-93bf-1e0c568e8e59/score'
    data={"payload" : str(payload)}
    response_json = requests.post(url, json=data, headers=headers)
    st.text_input("API Response: ",response_json.content)
    response = response_json.json()
    try:
        return response['upload_logging_data']['response_data']
    except ValueError:
        return response.status_code 