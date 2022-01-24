import os
import wget 
import pandas as pd
import numpy as np
import pandas_gbq
from google.cloud import storage

url = os.environ['URL']
bucket_name = os.environ['BUCKET']
file_name = os.environ['FILE_NAME']
volatility_tbl = os.environ['VOLATILITY_TBL']
projectId = os.environ['PROJECT']

cf_path= '/tmp/{}'.format(file_name)

def import_file(event, context):

  #Download File
  client = storage.Client()
  bucket = client.get_bucket(bucket_name)
  wget.download(url, cf_path)
  blob = storage.Blob(file_name, bucket)
  blob.upload_from_filename(cf_path)



  #Insert the data downloaded from the URL into its BQ table
  df = pd.read_json(url)
  pandas_gbq.to_gbq(df, 'dataset.table', project_id=projectId, if_exists='replace')

  
  #Get Volatility and Sharpe Ratio and insert it into a BQ table
  TRADING_DAYS = 252
  df['returns'] = np.log(df['price_close']/df['price_close'].shift(1))
  df['returns'].fillna(0, inplace=True)
  df['volatility'] = df['returns'].rolling(window=TRADING_DAYS).std()*np.sqrt(TRADING_DAYS)
  df['sharpe_ratio'] = df['returns'].mean()/df['volatility']  
  df = df[['time_period_start', 'time_period_end', 'volatility', 'sharpe_ratio']]
  
  pandas_gbq.to_gbq(df, volatility_tbl, project_id=projectId, if_exists='replace')
