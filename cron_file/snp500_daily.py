#!/usr/bin/env python
# coding: utf-8


#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from time import sleep
import FinanceDataReader as fdr

import datetime
import os
import time

import glob
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud import storage

# 서비스 계정 키 JSON 파일 경로
key_path = glob.glob("streamlit_stock/*.json")[0]

# Credentials 객체 생성
credentials = service_account.Credentials.from_service_account_file(key_path)

if not os.path.exists(f'data_crawler'):
    os.makedirs(f'data_crawler')
if not os.path.exists(f'log'):
    os.makedirs(f'log')

now = datetime.datetime.now() - datetime.timedelta(days=1)
today_date1 = now.strftime('%Y%m%d')
today_date2 = now.strftime('%Y-%m-%d')

def log_df(file_name, status):
    now_time = datetime.datetime.now()
    now_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
    log_df = pd.DataFrame({
        'ticker_nm': ticker_nm,
        'file_name': file_name,
        'time': now_time,
        'statue': status
    }, index = [0])    
    
    if not os.path.exists(f'streamlit_stock/data_crawler/snp500_log_df.csv'):
        log_df.to_csv(f'streamlit_stock/data_crawler/snp500_log_df.csv', index = False, mode = 'w')
    else:
        log_df.to_csv(f'streamlit_stock/data_crawler/snp500_log_df.csv', index = False, mode = 'a', header = False)
        


# In[ ]:





# In[20]:


sp500 = pd.read_csv('streamlit_stock/data_crawler/sp500.csv')
sp500_ticker_list = sp500['ticker']

print(f'{today_date2} S&P 500 주가정보 수집 시작')   


# In[22]:


for ticker_nm in sp500_ticker_list:
    file_name = 'snp500_daily'
    try:
        # Apple(AAPL), 2017-01-01 ~ Now
        snp500_daily = fdr.DataReader(ticker_nm, today_date2,today_date2)
        snp500_daily['ticker'] = ticker_nm
        snp500_daily = snp500_daily.reset_index()
        
        # file_name = 'snp500_daily'
        df = snp500_daily
        
        if not os.path.exists(f'streamlit_stock/data_crawler/{file_name}.csv'):
            df.to_csv(f'streamlit_stock/data_crawler/{file_name}.csv', index=False, mode='w')
        else:
            df.to_csv(f'streamlit_stock/data_crawler/{file_name}.csv', index=False, mode='a', header=False)
        
        log_df(file_name, 'success')    
    except:
        log_df(file_name, 'fail')


# In[ ]:





# In[ ]:


print('S&P 500 주가정보 수집 완료 ')           
        
        

# GCP 클라이언트 객체 생성
storage_client = storage.Client(credentials = credentials, 
                         project = credentials.project_id)

    
data = 'streamlit_stock/data_crawler/snp500_daily.csv'
bucket_name = 'data1-study1'    # 서비스 계정 생성한 bucket 이름 입력
source_file_name = data   # GCP에 업로드할 파일 절대경로
destination_blob_name = data    # 업로드할 파일을 GCP에 저장할 때의 이름


bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)

blob.upload_from_filename(source_file_name)

print('success')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




