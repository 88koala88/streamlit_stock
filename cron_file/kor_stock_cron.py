#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# In[3]:


# 서비스 계정 키 JSON 파일 경로
key_path = glob.glob("streamlit_stock/*.json")[0]

# Credentials 객체 생성
credentials = service_account.Credentials.from_service_account_file(key_path)

if not os.path.exists(f'data_crawler'):
    os.makedirs(f'data_crawler')
if not os.path.exists(f'log'):
    os.makedirs(f'log')


# In[4]:


# ### 오늘 날짜 계산

# In[2]:


now = datetime.now()
today_date1 = now.strftime('%Y%m%d')
today_date2 = now.strftime('%Y-%m-%d')
ticker_nm = '005930'


# In[5]:


kor_ticker_list_df = pd.read_csv(f'streamlit_stock/data_crawler/kor_ticker_list.csv')
kor_ticker_list = kor_ticker_list_df['ticker']
# In[23]:


# In[6]:


# log
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
    
    if not os.path.exists(f'streamlit_stock/data_crawler/kor_log_df.csv'):
        log_df.to_csv(f'streamlit_stock/data_crawler/kor_log_df.csv', index = False, mode = 'w')
    else:
        log_df.to_csv(f'streamlit_stock/data_crawler/kor_log_df.csv', index = False, mode = 'a', header = False)
            


# ### 일자별 OHLCV 조회 (배치용)

# In[13]:


kor_stock_ohlcv = stock.get_market_ohlcv(today_date1,  market="ALL")
kor_stock_ohlcv = kor_stock_ohlcv.reset_index()
kor_stock_ohlcv = kor_stock_ohlcv.rename(columns =  {'티커':'ticker'})

file_name = 'kor_stock_ohlcv'
df = kor_stock_ohlcv

if not os.path.exists(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv'):
    df.to_csv(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv', index=False, mode='w')
else:
    df.to_csv(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv', index=False, mode='a', header=False)


# ### 시가총액 (배치용)

# In[ ]:


kor_market_cap = stock.get_market_cap(today_date1,  market="ALL")
kor_market_cap = kor_market_cap.reset_index()
kor_market_cap = kor_market_cap.rename(columns =  {'티커':'ticker'})
df = kor_market_cap

file_name = 'kor_market_cap'
df = kor_market_cap

if not os.path.exists(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv'):
    df.to_csv(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv', index=False, mode='w')
else:
    df.to_csv(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv', index=False, mode='a', header=False)


# ###   DIV/BPS/PER/EPS 조회 (매일 실행 되는 배치용)

# In[16]:


# ###   DIV/BPS/PER/EPS 조회 (매일 실행 되는 배치용)

# In[42]:

kor_stock_fundamental = stock.get_market_fundamental(today_date1, market='ALL')
kor_stock_fundamental = kor_stock_fundamental.reset_index()
kor_stock_fundamental.rename(columns = {'티커':'ticker'}, inplace = True)
kor_stock_fundamental['날짜'] = today_date2

file_name = 'kor_stock_fundamental'
df = kor_stock_fundamental

if not os.path.exists(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv'):
    df.to_csv(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv', index=False, mode='w')
else:
    df.to_csv(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv', index=False, mode='a', header=False)


# ### 일자별 거래실적 추이 (거래대금) 배치용

# In[ ]:


print('거래실적 (거래대금)수집 시작')
# In[34]:
ticker_nm = '005930'
# time.sleep(300)
buy_sell_type_list = ['순매수', '매수', '매도']
for buy_sell_type in buy_sell_type_list:
    for ticker_nm in kor_ticker_list:
        file_name = 'kor_stock_trading_value_by_investor'
        try:
            kor_stock_trading_value_by_investor = stock.get_market_trading_value_by_date(today_date1, today_date1, 
                                                                             ticker_nm, 
                                                                             detail=True,
                                                                             on = buy_sell_type)
            kor_stock_trading_value_by_investor = kor_stock_trading_value_by_investor.reset_index()
            kor_stock_trading_value_by_investor['ticker'] = ticker_nm
            kor_stock_trading_value_by_investor['type'] = buy_sell_type
            
            df = kor_stock_trading_value_by_investor
            
            if not os.path.exists(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv'):
                df.to_csv(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv', index=False, mode='w')
            else:
                df.to_csv(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv', index=False, mode='a', header=False)
            
            log_df(file_name, f'success_{buy_sell_type}')    
        except:
            log_df(file_name, f'fail_{buy_sell_type}')
    #time.sleep(300)
        
print('거래실적 (거래대금)수집 완료')        


# ### 일자별 거래실적 추이 (거래대금) 배치용

# In[ ]:


print('거래실적 (거래량)수집 시작')     
# In[38]:
for buy_sell_type in buy_sell_type_list:
    for ticker_nm in kor_ticker_list:
        file_name = 'kor_stock_trading_volume_by_date'
        try:
            kor_stock_trading_volume_by_date = stock.get_market_trading_volume_by_date(start_date, today_date1, 
                                                                             ticker_nm, 
                                                                             detail=True,
                                                                             on =buy_sell_type)
            kor_stock_trading_volume_by_date = kor_stock_trading_volume_by_date.reset_index()
            kor_stock_trading_volume_by_date['ticker'] = ticker_nm
            kor_stock_trading_volume_by_date['type'] = buy_sell_type
            
            df = kor_stock_trading_volume_by_date
            
            if not os.path.exists(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv'):
                df.to_csv(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv', index=False, mode='w')
            else:
                df.to_csv(f'streamlit_stock/data_crawler/{file_name}_{today_date1}.csv', index=False, mode='a', header=False)
            
            log_df(file_name, 'success')    
        except:
            log_df(file_name, 'fail')
    #time.sleep(300)
    
print('거래실적 (거래량)수집 완료')         


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# GCP 클라이언트 객체 생성
storage_client = storage.Client(credentials = credentials, 
                         project = credentials.project_id)

for data in glob.glob(f"streamlit_stock/data_crawler/*_{today_date1}.csv"):
    print('start')
    print(data)
    
    bucket_name = 'data1-study1'    # 서비스 계정 생성한 bucket 이름 입력
    source_file_name = data   # GCP에 업로드할 파일 절대경로
    destination_blob_name = data   # 업로드할 파일을 GCP에 저장할 때의 이름

    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    
    print('success')


# In[ ]:





# In[ ]:





# In[ ]:




