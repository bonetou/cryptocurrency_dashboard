from read_data_options import read_crypto_options
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime
import numpy as np

st.title('Cryptocurrency Dashboard')

#sidebar options
crypto_options = read_crypto_options()
sidebar = st.sidebar.selectbox('Select the cryptocurrency file to read', 
	crypto_options)

#select data file and date
data = pd.read_csv(f'data/{sidebar}')
data['Date'] = pd.to_datetime(data['Date'])
data['Date'] = data['Date'].dt.date
data['Year Month'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m')

#config dataframe date
min_date = data['Date'][0]
max_date = data['Date'][data.shape[0]-1]

st.subheader('Select data range to analyse')
start_date = st.date_input('Start Date', value=min_date, min_value=min_date, max_value=max_date)
end_date = st.date_input('End Date', value=max_date, min_value=min_date, max_value=max_date)

#display dashboard components or not 
data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
data['Return'] = (data['Close'] - data['Open'])/data['Open']
n_ups = data[data['Return'] > 0 ].count()['Return']
n_downs = data[data['Return'] < 0 ].count()['Return']

st.write(sidebar.replace('.csv', ''), 'data')
st.dataframe(data)

st.subheader('Charts and Indicators')
#Close price, volume and returns
fig = make_subplots(
	rows=3, cols=1,
	x_title='Date',
	row_heights=[30, 20,15])

fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Close Price'), row=1, col=1)
fig.add_trace(go.Scatter(x=data['Date'], y=data['Return'], name='Return'), row=2, col=1)
fig.add_trace(go.Scatter(x=data['Date'], y=data['Volume'], name='Volume'), row=3, col=1)
fig.update_layout(title='Close Price, Returns and Volume')
st.plotly_chart(fig)

#number of ups and downs
x = ['n_ups', 'n_downs']
y = [n_ups, n_downs]
fig = go.Figure([go.Bar(
		x=x,
		y=y,
		text=y,
		textposition='auto',
		marker_color=['green', 'crimson']
	)
])
fig.update_layout(title='Number of Ups and Downs')
st.plotly_chart(fig)

#return per month
return_per_month=[]
year_months = data['Year Month'].unique()
for year_month in year_months:
	temp_data = data[data['Year Month']==year_month]['Close'].reset_index(drop=True)
	ret = (temp_data[temp_data.shape[0]-1] - temp_data[0])/temp_data[0]
	return_per_month.append(ret)

colors = [('green' if ret > 0 else 'red') for ret in return_per_month]

fig = go.Figure([go.Bar(
	x=year_months,
	y=return_per_month,
	marker={'color': colors}
)])
fig.update_layout(title='Return per Month', yaxis=dict(tickformat='.1%'))
go.Layout(yaxis=dict(tickformat='.2%'))

st.plotly_chart(fig)