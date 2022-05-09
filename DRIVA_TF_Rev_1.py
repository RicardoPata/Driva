import pandas as pd
import numpy as np
import requests

import time
import ccxt
from datetime import datetime

#dfHL_2 = pd.DataFrame(columns=['time', 'open' , 'high' ,'low', 'close'] )



Ciclos = 0
Xminutos = 1 # numero minutos apos internet falhar que programa deve reniciar
Minutos = Xminutos * 60
#dictionary
Web_Requests_Candles = 0 
WebFail_Time = 0 


def TF(dfHL_1):
    
    global Ciclos    
          
    print("Ciclo Numero: ",Ciclos)
    Ciclos = Ciclos + 1
    # Web_Requests_Candles = Web_Requests_Candles + 1
    # print ("Web_Requests_Candles: ",Web_Requests_Candles)
    
    try: # Candle Stick data frame
    
        # collect the candlestick data from Binance >
        binance = ccxt.binance()
        #binance = ccxt.binance({ 'options': { 'defaultType': 'future' } })
        trading_pair = 'BTC/USDT'
        candles = binance.fetch_ohlcv(trading_pair, '1m')
        dates = []
        open_data = []
        high_data = []
        low_data = []
        close_data = []
        
        
        # format the data to match the charting library
        for candle in candles:
            dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S'))
            open_data.append(candle[1])
            high_data.append(candle[2])
            low_data.append(candle[3])
            close_data.append(candle[4])
    
       # ohlc_data = [dates,open_data,high_data,low_data,close_data]
        pd.set_option('display.max_rows',500)
        HeadDictHL = {'time': dates, 'open': open_data,  'high': high_data, 'low': low_data, 'close': close_data}
        dfHL_A = pd.DataFrame(HeadDictHL)
        dfHL_A = dfHL_A.iloc[-2:]
        dfHL_A=dfHL_A.reset_index(drop=True)
        dfHL_1 = pd.concat([dfHL_1,dfHL_A.iloc[0:1]])
        dfHL_1 = dfHL_1.drop_duplicates(subset="time", keep="last", inplace=False)
        dfHL_1= dfHL_1.reset_index(drop=True)
        #print(dfHL_1)
        time.sleep(5)
     
     
        
        #print ("\nWeb Requests Velas: ",Web_Requests_Candles,"\n")
        #Web_Requests_Candles = Web_Requests_Candles + 1
        return dfHL_1, Ciclos
        
    except:
          
          #WebFail_Time = WebFail_Time + 1
          #print("Velas Web Requests Failed: ",WebFail_Time,"\n")
          
          #if WebFail_Time >= Minutos:
              print("\nRestart Data Frame \n\n")
              #self.dfHL_1 = None
              WebFail_Time = 0
            
       
          #pass
                  
