import streamlit as st
import pandas as pd
import requests
import json

# @st.experimental_memo
def binary_model(payload):
    
    headers={"Content-type":"application/json"}
    url = 'http://svc-e5a99d50-7723-47a5-8ac6-bd5c9bae793c:5001/creditcardfrauddetectionmodel/b662fba5-4e6c-4fd9-872b-83fbdff39018/score'
    data={"payload" : payload}
    response_json = requests.post(url, json=data, headers=headers)
    st.text_input("API Response: ",response_json.content)
    response = response_json.json()
    try:
        return response['upload_logging_data']['response_data']
    except ValueError:
        return response.status_code 