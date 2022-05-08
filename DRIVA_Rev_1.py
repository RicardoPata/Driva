import pandas as pd
import numpy as np
import requests
import json
import time
#import smtplib
import ccxt
from datetime import datetime
import time

#teste 

while True:
   
    #dictionary
    dfHL = pd.DataFrame(columns=['time', 'open' , 'high' ,'low', 'close'] )

    # Vars BOOL
    Dif_RGG_OK = False
    Dif_GRR_OK = False

    GRR_Rtrc= False # descida, condicoes para retracement ok to check v
    RGG_Rtrc= False # subida, condicoes para retracement ok to check


    Aposta_RGG_made = False
    Aposta_GRR_made = False
    
    RGG_Rtrc_Atingido = False
    GRR_Rtrc_Atingido = False


    RGG_Rtrc_Estabelecido = False
    GRR_Rtrc_Estabelecido = False
   
    RGG_High_ind_Rtrc_1 = False
    GRR_Low_ind_Rtrc_1 = False
    
    
    RGG_High_ind_Rtrc_2 = False
    GRR_Low_ind_Rtrc_2 = False


    Mail_GRR_Long = False
    Mail_RGG_Short = False
    
    GRR_Wait_TPSL = False
    RGG_Wait_TPSL = False
    
    
    # Vars INT
    Dif_HL_val = 0.9 # este dif e para achar a diferenca entre high e low

    WebFail_Time = 0
    WebFail_BTC_Time = 0
    
    Web_Requests_Candles = 0  
    Web_Requests_Btc = 0 
    
    RGG_NewCandle_index = 0
    GRR_NewCandle_index = 0
    
    Rtrc_RGG_Res_Last = 0
    Rtrc_GRR_Res_Last = 0
    
    Dif_GRR = 0
    Dif_RGG = 0
     
    RGG_HighMax_indice = 0
    GRR_LowMin_indice = 0
    
    RGG_Rtrc_Time_indice_int = 0
    GRR_Rtrc_Time_indice_int = 0
    
    RGG_High_ind_Rtrc_2 = False
    GRR_Low_ind_Rtrc_2 = False
    
    RGG_Time_ind_Rtrc_2 = False
    GRR_Time_ind_Rtrc_2 = False
    
    
    Ciclos =  0
    
    Xminutos = 1 # numero minutos apos internet falhar que programa deve reniciar
    Minutos = Xminutos * 60
    
    while True:
        print("Ciclo Numero: ",Ciclos)
        Ciclos = Ciclos + 1
        # Web_Requests_Candles = Web_Requests_Candles + 1
        # print ("Web_Requests_Candles: ",Web_Requests_Candles)

        try: # Candle Stick data frame
        
            # collect the candlestick data from Binance >
            binance = ccxt.binance()
            #binance = ccxt.binance({ 'options': { 'defaultType': 'future' } })
            trading_pair = 'BTC/USDT'
            candles = binance.fetch_ohlcv(trading_pair, '5m')
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
            dfHL = pd.concat([dfHL,dfHL_A.iloc[0:1]])
            dfHL = dfHL.drop_duplicates(subset="time", keep="last", inplace=False)
            dfHL= dfHL.reset_index(drop=True)
         
            
            print ("\nWeb Requests Velas: ",Web_Requests_Candles,"\n")
            Web_Requests_Candles = Web_Requests_Candles + 1
      
        except:
              
              WebFail_Time = WebFail_Time + 1
              print("Velas Web Requests Failed: ",WebFail_Time,"\n")
              
              if WebFail_Time >= Minutos:
                  print("\nRestart Data Frame \n\n")
                  dfHL = None
                  WebFail_Time = 0
                  break
              time.sleep(1)
              pass
              

        if len(dfHL)<4:
            print("Velas: ",len(dfHL))

        if len(dfHL)>3:
            if len(dfHL)==4:
                print("Velas fechadas : ",len(dfHL) - 1)
            
            #Get bitcoin price
            try:
                r = requests.get('https://fapi.binance.com/fapi/v1/ticker/price?symbol=BTCUSDT')
                BtcPrice =json.loads(r.text)
                BtcPriceNow = BtcPrice['price']
                
                Web_Requests_Btc = Web_Requests_Btc + 1
                print ("Web Requests Bitcoin: ",Web_Requests_Btc,"\n")
                
            
            except:
            
                WebFail_BTC_Time = WebFail_BTC_Time + 1
                print("Web Failed Requests Bitcoin : ",WebFail_BTC_Time,"\n")
              
                if WebFail_BTC_Time >= Minutos:
                    print("Restart Data Frame BTC price")
                    dfHL = None
                    WebFail_BTC_Time = 0
                    break
                
                time.sleep(1)
                pass




            # High da vela mais recente
            New_Candle_High = dfHL['high'].iloc[-1]
            
            RGG_NewCandle_indice_list = dfHL.high[dfHL.high == New_Candle_High].index.tolist() # saca o index da ultima vela com high higher
            RGG_NewCandle_index = int(str(RGG_NewCandle_indice_list)[1:-1][-1]) # transforma de lista para valor inteiro
     
            
            # Low da vela mais recente
            New_Candle_Low = dfHL['low'].iloc[-1]
            
            GRR_NewCandle_indice_list = dfHL.low[dfHL.low == New_Candle_Low].index.tolist() # saca o index da ultima vela com high higher
            GRR_NewCandle_index = int(str(GRR_NewCandle_indice_list)[1:-1][-1]) # transforma de lista para valor inteiro
     
    
    
            #time frame fixo das 3 velas sempre mais recentes        
            #Subida  RGG
            RGG_R1 = dfHL['open'].iloc[-3] > dfHL['close'].iloc[-3] #vela vermelha
            RGG_G1 = dfHL['open'].iloc[-2] < dfHL['close'].iloc[-2] #vela verde
            RGG_G2 = dfHL['open'].iloc[-1] < dfHL['close'].iloc[-1] #vela verde
            RGG = RGG_R1 and RGG_G1 and RGG_G2                      # SEQUENCIA RED GREEN GREEN CONFIRMADO

            #Descida  GRR
            GRR_G1 = dfHL['open'].iloc[-3] < dfHL['close'].iloc[-3] #vela verde
            GRR_R1 = dfHL['open'].iloc[-2] > dfHL['close'].iloc[-2] #vela vermelha
            GRR_R2 = dfHL['open'].iloc[-1] > dfHL['close'].iloc[-1] #vela vermelha
            GRR = GRR_G1 and  GRR_R1 and  GRR_R2                    # SEQUENCIA  GREEN RED RED CONFIRMADO



             ########## STEP 1  ########## STEP 1      ########## STEP 1  ########## STEP 1

            if RGG and not RGG_Rtrc_Atingido and not GRR_Rtrc_Atingido:# SEQUENCIA RED GREEN GREEN CONFIRMADO
                RGG_G2_HighMax = dfHL['high'].iloc[-1]           # vela G2 High
                RGG_R1G1_LowMin =  min(dfHL['low'].iloc[-3:-1])  # low mais baixo das velas R1 e G1 - usar este para calcular retracement / ,
                RGG_R1G1_LowMax =  max(dfHL['low'].iloc[-3:-1])  # low mais alto das velas R1 e G1
                Dif_RGG = abs(((RGG_G2_HighMax - RGG_R1G1_LowMin) / RGG_R1G1_LowMin)*100) # diferenca entre o Maximo e Minimo

                RGG_HighMax_indice_list = dfHL.high[dfHL.high == RGG_G2_HighMax].index.tolist() # saca o index da vela G2 high higher
                RGG_HighMax_indice = int(str(RGG_HighMax_indice_list)[1:-1][-1]) # transforma de lista para valor inteiro
     
                GRR_Rtrc_Estabelecido= False
                Dif_RGG_OK = True
                Dif_GRR_OK = False
                         
                
                
            ########## STEP 2  ########## STEP 2   ########## STEP 2  ########## STEP 2
                
            if Dif_RGG_OK  and not GRR and not RGG_Rtrc_Atingido and not GRR_Rtrc_Atingido: # se tem sequencia certa, diferenca ok, nao ha uma sequencia GRR mais recente nem aposta foi feita
                if New_Candle_High > RGG_G2_HighMax: # se a vela mais recente tem o high maior que a vela G2
                    RGG_G2_HighMax = New_Candle_High
                    Mail_RGG_Short = False
                    RGG_Rtrc_Estabelecido = False

                    RGG_HighMax_indice_list = dfHL.high[dfHL.high == New_Candle_High].index.tolist() # saca o index da ultima vela com high higher
                    RGG_HighMax_indice = int(str(RGG_HighMax_indice_list)[1:-1][-1]) # transforma de lista para valor inteiro
     
        
                Rtrc_RGG = (RGG_G2_HighMax - RGG_R1G1_LowMin) * 0.42     #0.59 se quisermos melhor rácio
                Rtrc_RGG_Res = RGG_G2_HighMax - Rtrc_RGG
               
                if  not RGG_Rtrc_Estabelecido: print("\n\n SEQUENCIA RGG - \nStep1 - Step2 \n",Dif_RGG,"Dif_RGG: \n Min Val: ", RGG_R1G1_LowMax, "Max Val: ",RGG_G2_HighMax)   
             
                RGG_Rtrc_Estabelecido = True
                #Dif_RGG_OK = False
                
                

            ########## STEP 3 ######### STEP 3       ########## STEP 3 ######### STEP 3

            if RGG_Rtrc_Estabelecido and Dif_RGG >= Dif_HL_val and not GRR  and not Mail_RGG_Short and not RGG_Rtrc_Atingido and not GRR_Rtrc_Atingido:
                print("\n\nStep3 - RGG -  RETRACEMENT estabelecido. EMAIL")
               
                #if float(BtcPriceNow) <= float(Rtrc_RGG_Res):                        #mudei aqui o sinal

                Rtrc_RGG_TP = (RGG_G2_HighMax - RGG_R1G1_LowMin) * 1.233        #mudei aqui o sinal? original 0.233
                TP_RGG = RGG_G2_HighMax + Rtrc_RGG_TP                            

                Rtrc_RGG_SL = (RGG_G2_HighMax - RGG_R1G1_LowMin) * 1          #mudei aqui o sinal
                SL_RGG = RGG_G2_HighMax - Rtrc_RGG_SL                           
                
               
                # funçao para enviar email , condiçao para enviar apenas 1
                if Rtrc_RGG_Res != Rtrc_RGG_Res_Last:
                    # content = ('ENTRY LONG p=' +str(Rtrc_RGG_Res)+' a=1 s=btcusdt q=50% sl='+str(SL_RGG)+' tp='+str(TP_RGG)+' tt=futures l=30c tf=900 e=binance')
                    # mail = smtplib.SMTP("smtp.gmail.com",587)
                    # mail.ehlo()
                    # mail.starttls()
                    # mail.login("email","password")
                    # content = 'Subject: {}\n\n{}'.format(content, content)
                    # mail.sendmail("from email", "toemail", content)
                    # mail.sendmail("from email", "toemail", content)
                    # mail.close()
                    
                    print("\nenviou mail ENTRY SHORT" '\RGG','\nDiferenca %: ', Dif_RGG,'\nResultado Retraement: ', Rtrc_RGG_Res,'\nBTC Live Price: ',BtcPriceNow,"\n",datetime.now())
   
                    Rtrc_RGG_Res_Last = Rtrc_RGG_Res
                    Mail_RGG_Short = True



             ########## STEP 4 ######### STEP 4        ########## STEP 4 ######### STEP 4
                  
          
            # if Mail_RGG_Short and (RGG_HighMax_indice + 1) >= NewCandle_index: # mais uma vela depois do higher maximo
            #     RGG_High_ind_Rtrc_1 = True
            #    # RGG_Rtrc_index_1 =  RGG_HighMax_indice + 1
                
            if Mail_RGG_Short and RGG_NewCandle_index >  (RGG_HighMax_indice + 1): # mais duas vela depois do higher maximo
                RGG_High_ind_Rtrc_2 = True
               # RGG_Rtrc_index_2 =  RGG_HighMax_indice + 2
                    
                    #############

                if RGG_High_ind_Rtrc_2  and float(BtcPriceNow) <= float(Rtrc_RGG_Res) or float(New_Candle_Low) <= float(Rtrc_RGG_Res ) and not RGG_Rtrc_Atingido and not GRR_Rtrc_Atingido: # retracement atingido
    
                            Rtrc_RGG_TP = (RGG_G2_HighMax - RGG_R1G1_LowMin) * 1.233    
                            TP_RGG = RGG_G2_HighMax + Rtrc_RGG_TP        
    
                            Rtrc_RGG_SL = (RGG_G2_HighMax - RGG_R1G1_LowMin) * 1     
                            SL_RGG = RGG_G2_HighMax - Rtrc_RGG_SL 
                   
                                        # High da vela mais recente                           
                            RGG_Rtrc_Candle_Time = dfHL['time'].iloc[-1]
                            RGG_Rtrc_Candle_indice_list = dfHL.time[dfHL.time == RGG_Rtrc_Candle_Time].index.tolist() # saca o index da ultima vela com high higher
                            RGG_Rtrc_Time_indice_int = int(str(RGG_Rtrc_Candle_indice_list)[1:-1][-1]) # transforma de lista para valor inteiro
                     
                    
                            if not RGG_Wait_TPSL :
                                print("\n\nStep4 - RGG"'\nAPOSTA SHORT DONE \RGG','\nDiferenca %: ', Dif_RGG,'\nResultado Retraement: ', Rtrc_RGG_Res,'\nBTC Live Price: ',BtcPriceNow,"\n",datetime.now(),"\nWaiting for : \nSL:",SL_RGG,"\nTP: ",TP_RGG)
                                RGG_Wait_TPSL = True
                                
                            RGG_Rtrc_Atingido = True
                            Mail_RGG_Short = False
                            RGG_High_ind_Rtrc_1 = False
                            RGG_High_ind_Rtrc_2 = False
            
            ########## STEP 5 ######### STEP 5
            # if RGG_Rtrc_Atingido and (Rtrc_Time_indice_int + 1) >= NewCandle_index: # mais uma vela depois do higher maximo
            #     RGG_Time_ind_Rtrc_1 = True
            #  #   RGG_Time_index_Rtrc_1 =  RGG_Time_ind_Rtrc_1 + 1
                
            if RGG_Rtrc_Atingido and  RGG_NewCandle_index  > (RGG_Rtrc_Time_indice_int + 1) : # mais uma vela depois do higher maximo
                RGG_Time_ind_Rtrc_2 = True
             #   RGG_Time_index_Rtrc_2 =  RGG_Time_ind_Rtrc_2 + 2
                
            if RGG_Rtrc_Atingido: # Aguarda por SL ou TP
                RGG_Wait_TPSL = False
                
                print("\n\nStep5 - RGG\n Aguarda TP/SL")
              
                
                if  RGG_Time_ind_Rtrc_2 and float(BtcPriceNow) >= TP_RGG or float(BtcPriceNow) <= SL_RGG or float((New_Candle_High) >= TP_RGG  or float(New_Candle_Low)  <= SL_RGG) : # restart cycle after SL or TP subida

                            print("\nApostamos subida: SL ou TP atingido\n\n")

                        
                            RGG_Rtrc_Atingido = False
                            RGG_Time_ind_Rtrc_1 = False
                            RGG_Time_ind_Rtrc_2 = False
                            break


            #############DESCIDA #####################    #############DESCIDA #####################  #############DESCIDA #####################


            ########## STEP 1 ######### STEP 1


            if GRR and not RGG_Rtrc_Atingido and not GRR_Rtrc_Atingido: # SEQUENCIA GREEN RED RED  CONFIRMADO e retracement ainda nao atingido
                 GRR_R2_LowMin = dfHL['low'].iloc[-1]               # vela G2 tem High maximo
                 GRR_G1R1_HighMin =  min(dfHL['high'].iloc[-3:-1])  # low mais baixo das velas R1 e G1 - usar este para calcular retracement / ,
                 GRR_G1R1_HighMax =  max(dfHL['high'].iloc[-3:-1])  # low mais alto das velas R1 e G1
                 Dif_GRR = abs(((GRR_G1R1_HighMax - GRR_R2_LowMin) / GRR_R2_LowMin)*100) # diferenca entre o Maximo e Minimo

                 GRR_LowMin_indice_list = dfHL.low[dfHL.low == GRR_R2_LowMin].index.tolist() # saca o index da vela G2 high higher
                 GRR_LowMin_indice = int(str(GRR_LowMin_indice_list)[1:-1][-1]) # transforma de lista para valor inteiro
     

                 RGG_Rtrc_Estabelecido= False
                 Dif_GRR_OK = True
                 Dif_RGG_OK = False


                 
            ########## STEP 2 ######### STEP 2
                 
            if Dif_GRR_OK  and not RGG and not RGG_Rtrc_Atingido and not GRR_Rtrc_Atingido: # se tem sequencia

                if New_Candle_Low < GRR_R2_LowMin: # se a vela mais recente tem o high maior que a vela G2
                    GRR_R2_LowMin = New_Candle_Low
                    Mail_GRR_Long = False
                    GRR_Rtrc_Estabelecido= False
                    GRR_LowMin_indice_list = dfHL.low[dfHL.low == New_Candle_Low].index.tolist() # saca o index da vela G2 high higher
                    GRR_LowMin_indice = int(str(GRR_LowMin_indice_list)[1:-1][-1]) # transforma de lista para valor inteiro
     

                Rtrc_GRR = (GRR_G1R1_HighMax - GRR_R2_LowMin) * 0.58         # 0.41 se quisermos melhor rácio
                Rtrc_GRR_Res = GRR_G1R1_HighMax - Rtrc_GRR

                if  not GRR_Rtrc_Estabelecido:print("\nSEQUENCIA GRR - Step1 - - Step2 \n""\nDif_GRR:", Dif_GRR," \n Min Val: ", GRR_R2_LowMin, "Max Val: ",GRR_G1R1_HighMax)

                GRR_Rtrc_Estabelecido= True
                #Dif_GRR_OK = False              
            
            
            
            ########## STEP 3 ######### STEP 3

            if GRR_Rtrc_Estabelecido and Dif_GRR >= Dif_HL_val and not RGG  and not Mail_GRR_Long and not RGG_Rtrc_Atingido and not GRR_Rtrc_Atingido: #tem sequencia, diferenca, retracment
                print("Step3 - GRR - RETRACEMENT  estabelecido. email\n")
               
                Rtrc_GRR_TP = (GRR_G1R1_HighMax - GRR_R2_LowMin) * 1.233         
                TP_GRR = GRR_R2_LowMin - Rtrc_GRR_TP

                Rtrc_GRR_SL = (GRR_G1R1_HighMax - GRR_R2_LowMin) * 1          
                SL_GRR = GRR_R2_LowMin + Rtrc_GRR_SL
                
                if Rtrc_GRR_Res != Rtrc_GRR_Res_Last:
                    # content = 'ENTRY SHORT p='+str(Rtrc_GRR_Res)+' a=1 s=btcusdt q=50% sl='+str(SL_GRR)+' tp='+str(TP_GRR)+' tt=futures l=30c tf=900 e=binance'
                    # mail = smtplib.SMTP("smtp.gmail.com",587)
                    # mail.ehlo()
                    # mail.starttls()
                    # mail.login("email","password")
                    # content = 'Subject: {}\n\n{}'.format(content, content)
                    # mail.sendmail("from email", "toemail", content)
                    # mail.sendmail("from email", "toemail", content)
                    # mail.close()
                    # print("enviou mail ENTRY LONG\nDiferenca %: ", Dif_GRR,'\nResultado Retraement: ', Rtrc_GRR_Res,'\nBTC Live Price: ',BtcPriceNow,"\n",datetime.now())
               
                    Rtrc_GRR_Res_Last = Rtrc_GRR_Res

                    Mail_GRR_Long = True



            ########## STEP 4 ######### STEP 4

            if Mail_GRR_Long and GRR_NewCandle_index > (GRR_LowMin_indice + 1): # mais duas vela depois do higher maximo
                GRR_Low_ind_Rtrc_2 = True
               # RGG_Rtrc_index_2 =  RGG_HighMax_indice + 2
                    
                print("Step4 - GRR\n"'\nWaiting for : APOSTA LONG DONE \n')
                if GRR_Low_ind_Rtrc_2  and (float(BtcPriceNow) >= float(Rtrc_GRR_Res) or float(New_Candle_High) >= float(Rtrc_GRR_Res))and not RGG_Rtrc_Atingido and not GRR_Rtrc_Atingido: # Retracement atingido
    
    
                        Rtrc_GRR_TP = (GRR_G1R1_HighMax - GRR_R2_LowMin) * 1.233         
                        TP_GRR = GRR_R2_LowMin - Rtrc_GRR_TP
    
                        Rtrc_GRR_SL = (GRR_G1R1_HighMax - GRR_R2_LowMin) * 1          
                        SL_GRR = GRR_R2_LowMin + Rtrc_GRR_SL
                        
                        
                        GRR_Rtrc_Candle_Time = dfHL['time'].iloc[-1]
                        GRR_Rtrc_Candle_indice_list = dfHL.time[dfHL.time == GRR_Rtrc_Candle_Time].index.tolist() # saca o index da ultima vela com high higher
                        GRR_Rtrc_Time_indice_int = int(str(GRR_Rtrc_Candle_indice_list)[1:-1][-1]) # transforma de lista para valor inteiro
                     
                        
                        
                        if not GRR_Wait_TPSL :
                            print("Step4 - GRR\n"'\nAPOSTA LONG DONE \GRR','\nDiferenca %: ', Dif_GRR,'\nResultado Retraement: ', Rtrc_GRR_Res,'\nBTC Live Price: ',BtcPriceNow,"\n",datetime.now(),"\nWaiting for : \nSL:",SL_GRR,"\nTP: ",TP_GRR)
                            GRR_Wait_TPSL = True
                       
                        GRR_Rtrc_Atingido = True
                        Mail_GRR_Long = False
                    
                       # GRR_Low_ind_Rtrc_1 = False
                        GRR_Low_ind_Rtrc_2 = False
                        
    
                    
            ########## STEP 5 ######### STEP 5       
      
            if GRR_Rtrc_Atingido and  GRR_NewCandle_index  > (GRR_Rtrc_Time_indice_int + 1) : # mais duas vela depois do higher maximo
                GRR_Time_ind_Rtrc_2 = True                        
       
                        
            if  GRR_Rtrc_Atingido: # Aguarda por SL ou TP
                GRR_Wait_TPSL = False
                print("Step5 - GRR\n Aguarda TP/SL\n")
               
                if GRR_Time_ind_Rtrc_2 and float(BtcPriceNow)  >= SL_GRR or float(BtcPriceNow) <= TP_GRR or float((New_Candle_High) >= SL_GRR  or float(New_Candle_Low)  <= TP_GRR):
                            print("Apostamos LONG: SL ou TP atingido")
                            GRR_Rtrc_Atingido = False
                            GRR_Time_ind_Rtrc_2 = False  
                          
                            break

            ####################################################################################
