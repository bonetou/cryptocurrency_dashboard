from read_data_options import read_crypto_options
import streamlit as st
import pandas as pd
import datetime

st.title('Cryptocurrency Dashboard')

#sidebar options
crypto_options = read_crypto_options()
sidebar = st.sidebar.selectbox('Select the cryptocurrency file to read', 
	crypto_options)

#display data table
st.subheader(f'Data for {sidebar}')
data = pd.read_csv(f'data/{sidebar}')
data['Date'] = pd.to_datetime(data['Date'])

st.write('Select data range to analyse')
start_date = st.date_input('Start Date', data['Date'][0])
end_date = st.date_input('End Date', data['Date'][data.shape[0]-1])

#st.dataframe(data)
