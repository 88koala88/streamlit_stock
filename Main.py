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
import plotly.express as px
import numpy as np

df = pd.read_csv('snp500_tree_df.csv')

sector_nm = 'Information Technology'

df1 = df[df['sector'] == sector_nm]


# fig = px.treemap(df1, path=[px.Constant(sector_nm), 'industry', 'corp_name'], values='Volume',
#                   color='Volume', hover_data=['Volume'],
#                   color_continuous_scale='RdBu',
#                   color_continuous_midpoint=np.average(df['Volume'], weights=df['Volume']))

# fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    

# st.plotly_chart(fig, use_container_width=True)
# st.dataframe(df1)



# df = px.data.gapminder().query("year == 2007")
# fig = px.treemap(df, path=[px.Constant("world"), 'continent', 'country'], values='pop',
#                   color='lifeExp', hover_data=['iso_alpha'],
#                   color_continuous_scale='RdBu',
#                   color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop']))
# fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
# # fig.show()
# st.plotly_chart(fig, use_container_width=True)



@st.cache_data
def get_chart_68636849():
    import plotly.express as px
    import numpy as np
#     df = px.data.gapminder().query("year == 2007")
    fig = px.treemap(df1, path=[px.Constant(sector_nm), 'industry', 'corp_name'], values='Volume',
                      color='Volume', hover_data=['Volume'],
                      color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(df['Volume'], weights=df['Volume']))

#     fig = px.treemap(df1, path=[px.Constant("world"), 'continent', 'country'], values='pop',
#                       color='lifeExp', hover_data=['iso_alpha'],
#                       color_continuous_scale='RdBu',
#                       color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop']))
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    
    st.plotly_chart(fig)

#     tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
#     with tab1:
#         st.plotly_chart(fig, theme="streamlit")
#     with tab2:
#         st.plotly_chart(fig, theme=None)


