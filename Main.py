import streamlit as st
import pandas as pd
# from pykrx import stock
# from pykrx import bond
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import streamlit as st
from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.experimental_connection('gcs', type=FilesConnection)
kospi = conn.read("data1-study1/kospi_index.csv", input_format="csv", ttl=600)
kosdaq= conn.read("data1-study1/kosdaq_index.csv", input_format="csv", ttl=600)



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
st.write('업데이트 중.. :sunglasses:')
st.write('Github : https://github.com/88koala88/streamlit_stock')
st.write('Vlog : https://koala88python.tistory.com')





# 인덱스 차트

df1 = kospi
fig1 = px.line(df1, x="날짜", y="종가", title='코스피 지수')

st.plotly_chart(fig1, use_container_width=True, **kwargs)

df2 = kosdaq
fig2 = px.line(df2, x="날짜", y="종가", title='코스닥 지수')
  
st.plotly_chart(fig2, use_container_width=True, **kwargs)

 
   





