import streamlit as st
import plotly.express as px
import pandas as pd
from pathlib import Path
from database import Database

# Streamlit Config
st.set_page_config(
    page_title="Stout Case Study 2",
    page_icon="💸",
    initial_sidebar_state="expanded",
    # layout="wide"
)

# Constants
STOUT_IMAGE_PATH = 'images/stout_logo.png'
DATA_PATH = 'data/casestudy.csv'

# Path Settings
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

# Load CSS
# with open(css_file) as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session State
# session=

# Sidebar
with st.sidebar:
    pages = st.radio('Navigation', options=['Analysis', 'About'])

# Database
db = Database(DATA_PATH)

st.image(STOUT_IMAGE_PATH)
st.title('Stout Case Study 2')

if pages=='Analysis' :
    # Revenue over the Years
    st.markdown('# Revenue over the Years')
    st.markdown('As we can see from the plot below, 2016 was not a great year, but in 2017 the company performed really well and even recovered the losses of the previous year')
    df_plot = db.query_revenue_over_years(db.df)
    fig = px.line(
        data_frame=df_plot,
        markers=True,
        x='year',
        y='net_revenue',
        template='plotly_dark'
    )
    fig.update_layout(
        title={'text' : 'Revenue over the Years'},
        xaxis_title = 'Year',
        yaxis_title = 'Revenue',
        font=dict(size=15)
    )
    fig.update_xaxes(
        dtick='M1'
    )
    st.plotly_chart(fig)

    # Revenue from new customers vs lost
    st.markdown('# Revenue from New Customers vs Lost from Attrition')
    st.markdown('The graph shows that new customers brought a lot more money to the company than the money that was lost from attrition')
    df_plot = db.query_revenue_lost_vs_gained(db.df)
    fig = px.line(
        data_frame=df_plot,
        markers=True,
        x='Year',
        y=['New Customer Revenue', 'Revenue Lost from Attrition'],
        template='plotly_dark'
    )
    fig.update_layout(
        title={'text' : 'Revenue from New Customers vs Lost from Attrition'},
        xaxis_title = 'Year',
        yaxis_title = 'Revenue',
        font=dict(size=15),
        legend_title_text=''
    )
    fig.update_xaxes(
        dtick='M1'
    )
    st.plotly_chart(fig)

    #New customers vs Lost Customers
    st.markdown('# New Customers vs Lost Customers')
    st.markdown('Despite 2017 being a year with a lot of profit for the company, it lost a lot more customers than it gained. Maybe though they followed a strategy of raising the prices with the cost of losing clients and it worked in the end.')
    df_plot = db.query_new_vs_lost_customers(db.df)
    fig = px.line(
        data_frame=df_plot,
        markers=True,
        x='Year',
        y=['New Customers', 'Lost Customers'],
        template='plotly_dark',
        labels=['New Customers', 'Lost Customers']
    )
    fig.update_layout(
        title={'text' : 'New Customers vs Lost Customers'},
        xaxis_title = 'Year',
        yaxis_title = 'Customers',
        font=dict(size=15),
        legend_title_text=''
    )
    fig.update_xaxes(
        dtick='M1'
    )
    st.plotly_chart(fig)

    #Histogram of Net Revenue
    st.markdown('# Histogram of Net Revenue') 
    st.markdown('As expected, 2017 has clearly higher revenue than the other years. Also data doesn\'t seem to be normally distributed')

    fig = px.histogram(
        data_frame=db.df,
        x='net_revenue',
        nbins=40,
        title='Net Revenue Histogram',
        template='plotly_dark',
        color='year'
    )
    fig.update_layout(
        xaxis_title = '',
        yaxis_title = 'Net Revenue',
        font=dict(size=15),
    )
    st.plotly_chart(fig)
    
elif pages=='About':
    st.markdown("""
                    This project was made by [Christos Aivazidis](https://www.linkedin.com/in/aiva00) as part of the Stout\'s Case Study 2  
                      
                    Use the navigation bar on the left to navigate to the "Analysis" page and explore the interactive plots I created from the data.
                    """)
    
    st.markdown("""
                    In this case study we analyze the customers and revenue of a company over the years and there are 2 important goals:  
                    1. Create appropriate queries to get the correct data
                    2. Generate interesting visualizations and conclusions from them
                    """)
    
    st.info('You can also check the jupyter notebook for all the queries and the code step-by-step')