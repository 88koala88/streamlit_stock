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
import streamlit as st
from PIL import Image



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



# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.experimental_connection('gcs', type=FilesConnection)
kospi = conn.read("data1-study1/kospi_index.csv", input_format="csv", ttl=600)
kosdaq= conn.read("data1-study1/kosdaq_index.csv", input_format="csv", ttl=600)

price_change = conn.read("data1-study1/price_index.csv", input_format="csv", ttl=600)


# oday_date = price_change['날짜'].unique().to_list()[0]

today_date = price_change['날짜'].astype(str).to_list()[0]

price_change['type'] = price_change['type'].astype(str)

# 등락률
kospi_change_value = price_change[price_change['type'] == '1001']['종가'].to_list()[0]
kosdaq_change_value = price_change[price_change['type'] == '2001']['종가'].to_list()[0]

kospi_change_ratio = price_change[price_change['type'] == '1001']['등락률'].to_list()[0]
kosdaq_change_ratio = price_change[price_change['type'] == '2001']['등락률'].to_list()[0]


def delta_color_func(aa):
    if aa < 0:
        delta_color_value = 'normal'
    else:
        delta_color_value = 'inverse'
    return delta_color_value
    
                            
# Tab / 인덱스 차트
import streamlit as st
st.write(f'{today_date} 기준     (업데이트 중..)')

col11, col12 = st.columns(2)
with col11:
    st.metric(label="KOSPI", 
              value=kospi_change_value,
              delta=kospi_change_ratio, 
              delta_color=delta_color_func(kospi_change_ratio))
with col12:
    st.metric(label="KOSDAQ", 
              value=kosdaq_change_value,
              delta=kosdaq_change_ratio, 
              delta_color=delta_color_func(kosdaq_change_ratio))


# tab1, tab2  = st.tabs(["KOSPI INDEX", "KOSDAQ INDEX"])

col1, col2 = st.columns(2)

with col1:
    df1 = pd.DataFrame(kospi)
    fig1 = px.line(df1, x='날짜', y='종가', title = '코스피 지수')
    st.plotly_chart(fig1, use_container_width=True)
    

with col2:
    df2 = pd.DataFrame(kosdaq)
    fig2 = px.line(df2, x='날짜', y='종가', title = '코스닥 지수')
    st.plotly_chart(fig2, use_container_width=True)








