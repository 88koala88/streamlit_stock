#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pykrx import stock
from pykrx import bond
from time import sleep
import FinanceDataReader as fdr

from datetime import datetime
import os
import time

import glob
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud import storage
# 서비스 계정 키 JSON 파일 경로
key_path = glob.glob("*.json")[0]

# Credentials 객체 생성
credentials = service_account.Credentials.from_service_account_file(key_path)

if not os.path.exists(f'data_crawler'):
    os.makedirs(f'data_crawler')
if not os.path.exists(f'log'):
    os.makedirs(f'log')
    
# ### 오늘 날짜 계산

# In[2]:


now = datetime.now()
today_date1 = now.strftime('%Y%m%d')
today_date2 = now.strftime('%Y-%m-%d')
ticker_nm = '005930'


start_date = '20180101'


# # 국내 주식

# ## krx 종목 리스트

# In[22]:

print('종목리스트 수집 시작')
market_list = ['KOSPI', 'KOSDAQ', 'KONEX']

kor_ticker_list_df = pd.DataFrame()
for market_nm in market_list:
    kor_ticker_list = stock.get_market_ticker_list(today_date1, market=market_nm)
    for tickers in kor_ticker_list:
        corp_name = stock.get_market_ticker_name(tickers)
        df = pd.DataFrame({'ticker':tickers,
                           'corp_name':corp_name,
                           'marke': market_nm
                          }, index = [0])
        kor_ticker_list_df = pd.concat([kor_ticker_list_df,df])
kor_ticker_list_df = kor_ticker_list_df.reset_index(drop = True)


kor_ticker_list = kor_ticker_list_df['ticker']

kor_ticker_list_df.to_csv(f'data_crawler/kor_ticker_list.csv', index=False, mode='w')

print('종목리스트 수집 완료')


      

# kor_ticker_list_df = pd.read_csv(f'data_crawler/ticker_list.csv')
# kor_ticker_list = kor_ticker_list_df['ticker']
# In[23]:


# ## 시가총액

# ### 종목별 시가총액 수집용

# In[63]:
def log_df(file_name, status):
    now_time = datetime.now()
    now_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
    log_df = pd.DataFrame({
        'ticker_nm': ticker_nm,
        'file_name': file_name,
        'time': now_time,
        'statue': status
    }, index = [0])    
    
    if not os.path.exists(f'data_crawler/log_df.csv'):
        log_df.to_csv(f'data_crawler/log_df.csv', index = False, mode = 'w')
    else:
        log_df.to_csv(f'data_crawler/log_df.csv', index = False, mode = 'a', header = False)
            

print('S&P 500 symbol list 수집 시작')     
    
    
    
    
# S&P 500 symbol list
sp500 = fdr.StockListing('S&P500')
sp500.columns = ['ticker', 'corp_name', 'sector', 'industry']

sp500.to_csv(f'data_crawler/sp500.csv', index=False, mode='w')
sp500_ticker_list = sp500['ticker']

print('S&P 500 주가정보 수집 시작')   
for ticker_nm in sp500_ticker_list:
    try:
        # Apple(AAPL), 2017-01-01 ~ Now
        snp500_daily = fdr.DataReader(ticker_nm, '2017-01-01',today_date2)
        snp500_daily['ticker'] = ticker_nm
        snp500_daily = snp500_daily.reset_index()
        
        file_name = 'snp500_daily'
        df = snp500_daily
        
        if not os.path.exists(f'data_crawler/{file_name}.csv'):
            df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='w')
        else:
            df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='a', header=False)
        
        log_df(file_name, 'success')    
    except:
        log_df(file_name, 'fail')

    try:
        stock_data = snp500_daily

        # 날짜 데이터 강제 stirng 변환
        stock_data['Date'] = stock_data['Date'].astype(str)
        # 날짜 데이터 datetime64[ns] 형식 변환
        stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        
        stock_data['month'] = stock_data['Date'].dt.month
        stock_data['year'] = stock_data['Date'].dt.year
        snp500_monthly = stock_data[['year','month','ticker', 'Close', 'Volume']].groupby(['year','month','ticker']).mean()
        snp500_monthly = snp500_monthly.reset_index()
        
        snp500_monthly['Date'] = snp500_monthly['year'].astype(str) + "-" + snp500_monthly['month'].astype(str) + '-01'
        snp500_monthly['Date'] = pd.to_datetime(snp500_monthly['Date'])
        
        file_name = 'snp500_monthly'
        df = snp500_monthly
        
        if not os.path.exists(f'data_crawler/{file_name}.csv'):
            df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='w')
        else:
            df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='a', header=False)
        
        log_df(file_name, 'success')    
    except:
        log_df(file_name, 'fail')
        
        
print('S&P 500 주가정보 수집 완료 ')        
            
print('종목별 시가총액 수집 시작')            
ticker_nm = '005930'
for ticker_nm in kor_ticker_list:
    try:
        kor_market_cap = stock.get_market_cap(start_date, today_date1, ticker_nm)
        kor_market_cap = kor_market_cap.reset_index()
        kor_market_cap['ticker'] = ticker_nm
        # kor_market_cap = kor_market_cap.drop(['거래량', '거래대금'], axis = 1)
        
        file_name = 'kor_market_cap'
        df = kor_market_cap
        
        if not os.path.exists(f'data_crawler/{file_name}.csv'):
            df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='w')
        else:
            df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='a', header=False)
        
        log_df(file_name, 'success')    
    except:
        log_df(file_name, 'fail')

print('종목별 시가총액 수집 완료')
# ### 종목별 시가총액 배치용

# In[64]:

# 
# kor_market_cap = stock.get_market_cap(today_date1)
# kor_market_cap = kor_market_cap.reset_index()
# kor_market_cap.rename(columns = {'티커':'ticker'}, inplace =True)
# kor_market_cap['날짜'] = today_date2
# kor_market_cap = kor_market_cap.drop(['종가','거래량', '거래대금'], axis = 1)
# kor_market_cap.head(2)


# ## OHLCV 
# 
# ### 일자별 OHLCV 조회 (수집용)
print('주가정보 수집 시작')
# In[39]:
ticker_nm = '005930'
time.sleep(300)
for ticker_nm in kor_ticker_list:
    try:
        kor_stock_ohlcv = stock.get_market_ohlcv(start_date, today_date1, ticker_nm)
        kor_stock_ohlcv = kor_stock_ohlcv.reset_index()
        kor_stock_ohlcv['ticker'] = ticker_nm
        
        file_name = 'kor_stock_ohlcv'
        df = kor_stock_ohlcv
        
        if not os.path.exists(f'data_crawler/{file_name}.csv'):
            df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='w')
        else:
            df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='a', header=False)
        
        log_df(file_name, 'success')    
    except:
        log_df(file_name, 'fail')

    try:
        stock_data = kor_stock_ohlcv

        # 날짜 데이터 강제 stirng 변환
        stock_data['날짜'] = stock_data['날짜'].astype(str)
        # 날짜 데이터 datetime64[ns] 형식 변환
        stock_data['날짜'] = pd.to_datetime(stock_data['날짜'])
        
        stock_data['월'] = stock_data['날짜'].dt.month
        stock_data['년'] = stock_data['날짜'].dt.year
        kor_stock_ohlcv_month = stock_data[['년','월','ticker', '종가', '거래량']].groupby(['년','월','ticker']).mean()
        kor_stock_ohlcv_month = kor_stock_ohlcv_month.reset_index()
        
        kor_stock_ohlcv_month['날짜'] = kor_stock_ohlcv_month['년'].astype(str) + "-" + kor_stock_ohlcv_month['월'].astype(str) + '-01'
        kor_stock_ohlcv_month['날짜'] = pd.to_datetime(kor_stock_ohlcv_month['날짜'])
        
        file_name = 'kor_stock_ohlcv_month'
        df = kor_stock_ohlcv_month
        
        if not os.path.exists(f'data_crawler/{file_name}.csv'):
            df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='w')
        else:
            df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='a', header=False)
        
        log_df(file_name, 'success')    
    except:
        log_df(file_name, 'fail')

print('주가정보 수집 완료')
# # ###  전종목 OHLCV 조회 (매일 실행 되는 배치용)
# 
# # In[40]:
# 
# 
# kor_stock_ohlcv = stock.get_market_ohlcv(today_date1, market='ALL')
# kor_stock_ohlcv = kor_stock_ohlcv.reset_index()
# kor_stock_ohlcv.rename(columns = {'티커':'ticker'}, inplace = True)
# kor_stock_ohlcv['날짜'] = today_date2
# kor_stock_ohlcv


# ##  DIV/BPS/PER/EPS
# ### 일자별  DIV/BPS/PER/EPS 조회

print('DIV/BPS/PER/EPS 수집 시작')
# In[34]:
ticker_nm = '005930'
time.sleep(300)
for ticker_nm in kor_ticker_list:
    try:
        kor_stock_fundamental = stock.get_market_fundamental(start_date, today_date1, ticker_nm)
        kor_stock_fundamental = kor_stock_fundamental.reset_index()
        kor_stock_fundamental['ticker'] = ticker_nm
              
        
        file_name = 'kor_stock_fundamental'
        df = kor_stock_fundamental
        
        if not os.path.exists(f'data_crawler/{file_name}.csv'):
            df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='w')
        else:
            df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='a', header=False)
        
        log_df(file_name, 'success')    
    except:
        log_df(file_name, 'fail')



print('DIV/BPS/PER/EPS 수집 완료')

# # ###   DIV/BPS/PER/EPS 조회 (매일 실행 되는 배치용)
# 
# # In[42]:
# 
# 
# kor_stock_fundamental = stock.get_market_fundamental(today_date1, market='ALL')
# kor_stock_fundamental = kor_stock_fundamental.reset_index()
# kor_stock_fundamental.rename(columns = {'티커':'ticker'}, inplace = True)
# kor_stock_fundamental['날짜'] = today_date2
# kor_stock_fundamental


# In[36]:


# ## 거래실적 (거래대금)
# 
# ### 일자별 거래실적 추이 (거래대금) 순매수

print('거래실적 (거래대금)수집 시작')
# In[34]:
ticker_nm = '005930'
time.sleep(300)
buy_sell_type_list = ['순매수', '매수', '매도']
for buy_sell_type in buy_sell_type_list:
    for ticker_nm in kor_ticker_list:
        try:
            kor_stock_trading_value_by_investor = stock.get_market_trading_value_by_date(start_date, today_date1, 
                                                                             ticker_nm, 
                                                                             detail=True,
                                                                             on = buy_sell_type)
            kor_stock_trading_value_by_investor = kor_stock_trading_value_by_investor.reset_index()
            kor_stock_trading_value_by_investor['ticker'] = ticker_nm
            kor_stock_trading_value_by_investor['type'] = buy_sell_type
            
            file_name = 'kor_stock_trading_value_by_investor'
            df = kor_stock_trading_value_by_investor
            
            if not os.path.exists(f'data_crawler/{file_name}.csv'):
                df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='w')
            else:
                df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='a', header=False)
            
            log_df(file_name, f'success_{buy_sell_type}')    
        except:
            log_df(file_name, f'fail_{buy_sell_type}')
    time.sleep(300)
        
print('거래실적 (거래대금)수집 완료')        
# buy_sell_type = ['순매수', '매수', '매도']
# 
# kor_stock_trading_value_by_investor = stock.get_market_trading_value_by_date(start_date, today_date1, 
#                                                                              ticker_nm, 
#                                                                              detail=True,
#                                                                              on ='순매수')
# kor_stock_trading_value_by_investor = kor_stock_trading_value_by_investor.reset_index()
# kor_stock_trading_value_by_investor['ticker'] = ticker_nm
# kor_stock_trading_value_by_investor



# ## 일자별 거래실적 추이(거래량)
# ### 거래실적(거래량)

print('거래실적 (거래량)수집 시작')     
# In[38]:
for buy_sell_type in buy_sell_type_list:
    for ticker_nm in kor_ticker_list:
        try:
            kor_stock_trading_volume_by_date = stock.get_market_trading_volume_by_date(start_date, today_date1, 
                                                                             ticker_nm, 
                                                                             detail=True,
                                                                             on =buy_sell_type)
            kor_stock_trading_volume_by_date = kor_stock_trading_volume_by_date.reset_index()
            kor_stock_trading_volume_by_date['ticker'] = ticker_nm
            kor_stock_trading_volume_by_date['type'] = buy_sell_type
            
            file_name = 'kor_stock_trading_volume_by_date'
            df = kor_stock_trading_volume_by_date
            
            if not os.path.exists(f'data_crawler/{file_name}.csv'):
                df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='w')
            else:
                df.to_csv(f'data_crawler/{file_name}.csv', index=False, mode='a', header=False)
            
            log_df(file_name, 'success')    
        except:
            log_df(file_name, 'fail')
    time.sleep(300)
    
print('거래실적 (거래량)수집 완료')         
# kor_stock_trading_volume_by_date = stock.get_market_trading_volume_by_date(start_date, today_date1, 
#                                                                              ticker_nm, 
#                                                                              detail=True,
#                                                                              on ='순매수')
# kor_stock_trading_volume_by_date = kor_stock_trading_volume_by_date.reset_index()
# kor_stock_trading_volume_by_date['ticker'] = ticker_nm
# kor_stock_trading_volume_by_date
  
        
        

# GCP 클라이언트 객체 생성
storage_client = storage.Client(credentials = credentials, 
                         project = credentials.project_id)

for data in glob.glob("data_crawler/*.csv"):
    print('start')
    print(data)
    
    bucket_name = 'data1-study1'    # 서비스 계정 생성한 bucket 이름 입력
    source_file_name = data   # GCP에 업로드할 파일 절대경로
    destination_blob_name = data    # 업로드할 파일을 GCP에 저장할 때의 이름

    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    
    print('success')
