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
    page_title="KOSDAQ 데이터",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


st.title('KOSDAQ')







    

    
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