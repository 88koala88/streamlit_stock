import streamlit as st
# import func_list
# import pandas as pd
# # from pykrx import stock
# # from pykrx import bond
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import datetime
# import numpy as np
# from st_files_connection import FilesConnection



image = Image.open('Data/arc.png')
# if st.button('아키텍쳐(클릭)', use_container_width=True):
st.image(image, caption='대시보드 데이터 아키텍쳐')


st.title('주가 데이터 대시보드 Blog List')

st.write('- Github : https://github.com/88koala88/streamlit_stock')
st.write('- Blog : https://koala88python.tistory.com')
st.write('- [GCP Compute Engine 구축](https://koala88python.tistory.com/99)')
st.write('- [Mac에서 GCP VM 인스턴스 활용하여 접속하기](https://koala88python.tistory.com/100)')
st.write('- [GCP에서 SQL DB 구축하기](https://koala88python.tistory.com/102)')
st.write('- [ubuntu 환경에서 PostgreSQL 설치 및 vscode 연결하기](https://koala88python.tistory.com/103)')
st.write('- [Google Cloud - Big Query&Storage 와 Python 연동하기](https://koala88python.tistory.com/104)')
st.write('- [Google BARD API로 Python과 연동하기](https://koala88python.tistory.com/105)')
st.write('- [Linux에서 Cron 기능 활용하기](https://koala88python.tistory.com/106)')
