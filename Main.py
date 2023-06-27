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



