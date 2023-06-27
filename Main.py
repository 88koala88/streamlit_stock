import streamlit as st
import pandas as pd
# from pykrx import stock
# from pykrx import bond
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime






# streamlit_app.py

import streamlit as st
from st_files_connection import FilesConnection


# 페이지 구성
st.set_page_config(
    page_title="주가 데이터 대시보드",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


st.title('Main')




###Treemap

import pandas as pd
df = pd.read_csv('snp500_tree_df.csv')
import plotly.express as px
import numpy as np


sector_nm = 'Information Technology'

df = df[df['sector'] == sector_nm]

def treemap(df)

    fig = px.treemap(df, path=[px.Constant(sector_nm), 'industry', 'corp_name'], values='Volume',
                  color='Volume', hover_data=['Volume'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(df['Volume'], weights=df['Volume']))

    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    return(fig)


fig = treemap(df)

st.plotly_chart(fig, use_container_width=True)





