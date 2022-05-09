# -*- coding: utf-8 -*-
"""
Created on Mon May  9 06:26:50 2022

@author: Asus
"""
import requests
import json
import time

Web_Requests_Btc = 0
Minutos = 0

global BtcPriceNow

def BTC_Price(BtcPriceNow):
    #Get bitcoin price        
    try:
        r = requests.get('https://fapi.binance.com/fapi/v1/ticker/price?symbol=BTCUSDT')
        BtcPrice =json.loads(r.text)
        BtcPriceNow = BtcPrice['price']
        print("BTC price: ",BtcPriceNow)
        return BtcPriceNow
    except:
        pass