import streamlit as st
import func_list
import pandas as pd
# from pykrx import stock
# from pykrx import bond
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import numpy as np
from st_files_connection import FilesConnection




# 페이지 구성
st.set_page_config(
    page_title="KOSPI 데이터",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.title('KOSPI')




# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.experimental_connection('gcs', type=FilesConnection)
stock = conn.read("data1-study1/kospi_data.csv", input_format="csv", ttl=600)
kospi_month = conn.read("data1-study1/kospi_data_month.csv", input_format="csv", ttl=600)

#############################################
###### 데이터 수집
###############################################
# stock = pd.read_csv('Data/stock_data.csv')

ticker_list = stock['corp_name'].unique()


# ticker set
ticker_nm = '095570'
option = st.selectbox(
    '원하는 종목을 선택하세요',
    ticker_list
)

naver_news = f'[{option}의 네이버 뉴스](https://search.naver.com/search.naver?where=news&sm=tab_jum&query={option})'
daum_news = f'[{option}의 다음 뉴스](https://search.daum.net/search?w=news&nil_search=btn&DA=NTB&enc=utf8&cluster=y&cluster_page=1&q={option})'


# market 표시
market_nm = stock[stock['corp_name'] == option]['marke'].to_list()[0]
market_nm = f':red[{market_nm}]'





## 폰트
st.write('선택 종목:', option)
# st.write('Market:', market_nm)
st.write(naver_news)
st.write(daum_news)


#stock_data set
stock_data = stock[stock['corp_name'] == option]
kospi_month_fig = kospi_month[kospi_month['corp_name'] == option]




# tab


tab1, tab2  = st.tabs(["일", "월"])

with tab1:
    st.header("일별 데이터")
    col1, col2 = st.columns([3, 1])

    
    stock_data2 = stock_data.sort_values(by = ['날짜'] , ascending = False)
    stock_data3 = stock_data2[['날짜','종가']]
    stock_data_des = stock_data3.reset_index(drop = True)
    daily_fig = func_list.daily_chart(stock_data, option)
    
    with col1:
        st.plotly_chart(daily_fig, use_container_width=True)
        
    with col2:
        st.dataframe(stock_data_des)
    

with tab2:
    st.header("월별 데이터")
    monthly_fig = func_list.monthly_chart(kospi_month_fig, option)
    
    aa, bb = st.columns([3,1])
    with aa:
        st.plotly_chart(monthly_fig, use_container_width=True)
        
    with bb:
        st.dataframe(kospi_month_fig)