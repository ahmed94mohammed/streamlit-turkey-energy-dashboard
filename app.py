import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import time
from datetime import datetime

# Load the dataset
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv'
    data = pd.read_csv(url)
    data['year'] = pd.to_datetime(data['year'], format='%Y')
    return data

data = load_data()

# Filter for Turkey
data_turkey = data[data['country'] == 'Turkey']

# Title of the dashboard
st.title('Turkey Energy Data Dashboard')

# Display current time and date
st.subheader(f"Current Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Sidebar for filtering
st.sidebar.header('Filter Options')

# Filter by year range
start_year, end_year = st.sidebar.slider('Select year range', int(data_turkey['year'].dt.year.min()), int(data_turkey['year'].dt.year.max()), (int(data_turkey['year'].dt.year.min()), int(data_turkey['year'].dt.year.max())))

# Apply filters
filtered_data = data_turkey[(data_turkey['year'].dt.year >= start_year) & (data_turkey['year'].dt.year <= end_year)]

# Display filtered data
st.subheader('Filtered Data')
st.write(filtered_data)

# Line plot for primary energy consumption over time
st.subheader('Primary Energy Consumption Over Time')
if not filtered_data.empty:
    fig = px.line(filtered_data, x='year', y='primary_energy_consumption', title='Primary Energy Consumption Over Time')
    st.plotly_chart(fig)
else:
    st.write("No data available for the selected range.")

# Bar chart for average primary energy consumption per year
st.subheader('Average Primary Energy Consumption per Year')
avg_energy = filtered_data.groupby(filtered_data['year'].dt.year)['primary_energy_consumption'].mean().reset_index()
if not avg_energy.empty:
    fig = px.bar(avg_energy, x='year', y='primary_energy_consumption', title='Average Primary Energy Consumption per Year')
    st.plotly_chart(fig)
else:
    st.write("No data available for the selected range.")

# Box plot for primary energy consumption by year
st.subheader('Primary Energy Consumption by Year')
if not filtered_data.empty:
    fig = px.box(filtered_data, x=filtered_data['year'].dt.year, y='primary_energy_consumption', title='Primary Energy Consumption by Year')
    st.plotly_chart(fig)
else:
    st.write("No data available for the selected range.")

# Heatmap for energy consumption correlation
st.subheader('Energy Consumption Correlation')
numeric_columns = filtered_data.select_dtypes(include=['float64', 'int64']).columns
if not numeric_columns.empty:
    corr = filtered_data[numeric_columns].corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", title='Energy Consumption Correlation Heatmap')
    st.plotly_chart(fig)
else:
    st.write("No numeric data available for correlation heatmap.")

# Adding a new type of data visualization: Renewable energy consumption over time
st.subheader('Renewable Energy Consumption Over Time')
if 'renewables_consumption' in filtered_data.columns:
    fig = px.line(filtered_data, x='year', y='renewables_consumption', title='Renewable Energy Consumption Over Time')
    st.plotly_chart(fig)
else:
    st.write("Renewable energy consumption data not available.")
