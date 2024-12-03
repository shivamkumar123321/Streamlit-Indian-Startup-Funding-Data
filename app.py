import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='StartUp Analysis',page_icon="❤️",initial_sidebar_state="expanded")

def load_overall_analysis():
    st.write('Johny Johny Yes Papa')

def load_investor_analysis():
    st.subheader('Startup analysis')

def load_startup_analysis():
    st.header('Startup analysis')


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select one',['Overall Analysis','Investor','StartUp'])

if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'Investor':
    st.selectbox()
else:
    load_startup_analysis()






















































































































































