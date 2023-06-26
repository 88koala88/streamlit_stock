import streamlit as st
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
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


st.title('KOSPI')




# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.experimental_connection('gcs', type=FilesConnection)
stock = conn.read("data1-study1/kospi_data.csv", input_format="csv", ttl=600)



# # 데이터 수집
# stock = pd.read_csv('Data/stock_data.csv')

ticker_list = stock['corp_name'].unique()

# ticker set
ticker_nm = '095570'
option = st.selectbox(
    '원하는 종목을 선택하세요',
    ticker_list
#     ('Email', 'Home phone', 'Mobile phone')
)

naver_news = f'[{option}의 네이버 뉴스](https://search.naver.com/search.naver?where=news&sm=tab_jum&query={option})'

daum_news = f'[{option}의 다음 뉴스](https://search.daum.net/search?w=news&nil_search=btn&DA=NTB&enc=utf8&cluster=y&cluster_page=1&q={option})'


# market 표시
market_nm = stock[stock['corp_name'] == option]['market'].to_list()[0]
market_nm = f':red[{market_nm}]'





## 폰트
st.write('선택 종목:', option)
st.write('Market:', market_nm)
st.write(naver_news)
st.write(daum_news)


#stock_data set
#stock_data = stock[stock['ticker'] == option]
stock_data = stock[stock['corp_name'] == option]





# tab

kospi_month = conn.read("data1-study1/kospi_data_month.csv", input_format="csv", ttl=600)


tab1, tab2 = st.tabs(["일", "월"])


tab1.subheader("일별 데이터")
#tab1.line_chart(data)

tab2.subheader("월별 데이터")
line_chart(kospi_month)
tab2.write(kospi_month)




# plotly 시각화
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Bar(
        name = '거래량',
        x = stock_data['날짜'],
        y = stock_data['거래량'],
        #marker = {'color':'black'}
    )
)

fig.add_trace(
    go.Scatter(
        name = '종가',
        x = stock_data['날짜'],
        y = stock_data['종가'],
        #marker = {'color': 'black'},
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
    #title= '나이스평가정보 거래량 및 거래금액 <br><sup>단위(만원)</sup>',
    title= f'{option} 거래량 및 종가',
    
    #title_font_family="맑은고딕",
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
# data = np.random.randn(10, 1)

stock_data2 = stock_data.sort_values(by = ['날짜'] , ascending = False)
stock_data3 = stock_data2[['날짜','종가']]
stock_data_des =stock_data3.reset_index(drop = True)



with col1:
    st.plotly_chart(fig, use_container_width=True)
    
with col2:
    st.dataframe(stock_data_des)


    

    
# col1.subheader("A wide column with a chart")
# col1.plotly_chart(fig, use_container_width=True)

# col2.subheader("A narrow column with the data")
# col2.dataframe(stock_data)

# st.dataframe(stock_data)
# st.plotly_chart(fig, use_container_width=True)



# streamlit.errors.StreamlitAPIException: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
# Traceback:
# File "/home/appuser/venv/lib/python3.9/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 552, in _run_script
#     exec(code, module.__dict__)
# File "/app/streamlit_study/pages/snp500.py", line 13, in <module>
#     page_icon="🧊",
# File "/home/appuser/venv/lib/python3.9/site-packages/streamlit/runtime/metrics_util.py", line 356, in wrapped_func
#     result = non_optional_func(*args, **kwargs)
# File "/home/appuser/venv/lib/python3.9/site-packages/streamlit/commands/page_config.py", line 225, in set_page_config
#     ctx.enqueue(msg)
# File "/home/appuser/venv/lib/python3.9/site-packages/streamlit/runtime/scriptrunner/script_run_context.py", line 90, in enqueue
#     raise StreamlitAPIException(