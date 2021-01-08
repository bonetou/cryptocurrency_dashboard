from read_data_options import read_crypto_options
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime

st.title('Cryptocurrency Dashboard')

#sidebar options
crypto_options = read_crypto_options()
sidebar = st.sidebar.selectbox('Select the cryptocurrency file to read', 
	crypto_options)

#select data file and date
data = pd.read_csv(f'data/{sidebar}')
data['Date'] = pd.to_datetime(data['Date'])
data['Date'] = data['Date'].dt.date

#config dataframe date
min_date = data['Date'][0]
max_date = data['Date'][data.shape[0]-1]

st.subheader('Select data range to analyse')
start_date = st.date_input('Start Date', min_date)
end_date = st.date_input('End Date', max_date)

#display dashboard components or not 
if start_date < min_date or end_date > max_date:
	st.write(f'There is no data for this data range, \
		try to select data between {min_date} and {max_date}')
else:
	#table
	data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
	st.write(sidebar.replace('.csv', ''), 'data')
	st.dataframe(data)

	#Close price and volume
	fig = make_subplots(
		rows=2, cols=1,
		x_title='Date',
		row_heights=[30, 15])

	st.subheader('Charts and Indicators')
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Close Price'), row=1, col=1)
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Volume'], name='Volume'), row=2, col=1)
	st.plotly_chart(fig)



