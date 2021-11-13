""""
@author: Danish Anwer
Reference: https://github.com/heliphix/btc_data/blob/main/datacollector.py
"""

from bs4 import BeautifulSoup 
import requests 
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re 
import pandas as pd  
from tqdm import tqdm
import argparse
parser=argparse.ArgumentParser()

parser.add_argument('-s','--start_date', default='2018/10/25', help="defines the start date like YYYY/MM/DD")
parser.add_argument('-e', '--end_date', default='2021/10/25', help="defines the end date like YYYY/MM/DD")
args = parser.parse_args()
start_date=args.start_date
end_date=args.end_date
features=['transactions','size','sentbyaddress','difficulty','hashrate','mining_profitability','sentinusd','transactionfees','median_transaction_fee','confirmationtime','transactionvalue','mediantransactionvalue','activeaddresses','top100cap','fee_to_reward','price','tweets']
indicators=['sma','ema','wma','trx','mom','std','var','rsi','roc']
periods=['3','7','14','30','90']
crypto=['btc']
url_list=['https://bitinfocharts.com/comparison/'+i+'-'+'btc'+'.html' for i in features]


url_list.extend(['https://bitinfocharts.com/comparison/'+i+'-'+'btc'+'-'+j+k+'.html' for i in features for j in indicators for k in periods])

feature_list=[i.split('/')[-1].split('.')[0]+'USD' if 'fee' in i or 'value' in i or 'price' in i or 'usd' in i else i.split('/')[-1].split('.')[0] for i in url_list]
feature_list=[i[0:-3] if 'fee_to_reward' in i else i for i in feature_list]

dict_data=dict()
for i in tqdm(range(len(feature_list))):
    url=url_list[i]
    session=requests.Session()
    retry = Retry(connect=10, backoff_factor=3)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    page=session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    values=soup.find_all('script')[4].get_text()
    newval=values.replace('[new Date("','').replace('"),',";").replace('],',',').replace('],',']]').replace('null','0')
    x = re.findall('\\[(.+?)\\]\\]', newval)
    l=x[0].split(',')
    m,date=[],[]
    for j in l:
        if str(j.split(";")[0])>=start_date and str(j.split(";")[0])<=end_date:
            m.append(float(j.split(";")[1]))
            date.append(j.split(";")[0])
    
    dict_data['Date']=date
    dict_data[feature_list[i]]=m
    
    
data=pd.DataFrame.from_dict(dict_data)
data.to_csv('bit_coin.csv',index=False)
print(data.head(10))
    
    
    
    
