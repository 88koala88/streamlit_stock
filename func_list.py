import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def daily_chart(stock_data, option):
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
    
    return(fig)




def mothly_chart(stock_data, option):
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
    return(fig)