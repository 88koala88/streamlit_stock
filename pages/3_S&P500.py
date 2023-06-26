import streamlit as st
import pandas as pd
# from pykrx import stock
# from pykrx import bond

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime


st.set_page_config(
    page_title="S&P 500",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title('S&P 500')

# 데이터 수집
stock = pd.read_csv('pages/snp_data.csv')

ticker_list = stock['Name'].unique()


# ticker set
ticker_nm = 'MMM'
option = st.selectbox(
    '원하는 종목을 선택하세요',
    ticker_list
)

st.write('선택 종목:', option)



# stock_data set
stock_data = stock[stock['Name'] == option]



# plotly 시각화
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Bar(
        name = '거래량',
        x = stock_data['Date'],
        y = stock_data['Volume'],
      
    )
)

fig.add_trace(
    go.Scatter(
        name = '시가',
        x = stock_data['Date'],
        y = stock_data['Open'],
       
        yaxis="y2"
    )
)

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)


fig.update_layout(
  
    title= f'{option} 거래량 및 시가',
    
   
    title_font_size = 18,
    hoverlabel=dict(
        bgcolor='white',
        font_size=15,
    ),
    hovermode="x unified",
    template='plotly_white',
    xaxis_tickangle=90,
    yaxis_tickformat = ',',
    legend = dict(orientation = 'h', xanchor = "center", x = 0.85, y=1.1), #Adjust legend position
    barmode='group'
)


################################################################
col1, col2 = st.columns([3, 1])


with col1:
    st.plotly_chart(fig, use_container_width=True)
    
with col2:
    st.dataframe(stock_data[['Date','Close','Symbol']])
    

 