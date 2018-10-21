# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 09:21:06 2018

@author: T58830
"""
import pandas as pd
import numpy as np


def optimizer(name, currency, inp, curr,lower,upper):
  inp = inp.dropna()
  data = pd.DataFrame()
  data['px'] = inp.div(curr)
  data = data.dropna()
  data['px'] = data['px']/data['px'][0]*100    
  mov_avg = []
  days = []
  for i in range(lower,upper +1):
    ret = mov_average_optim(data, i)
    mov_avg.append(ret)
    days.append(i)
  mov_frame = pd.DataFrame()
  mov_frame[name] = mov_avg
  mov_frame.index = days
#  x= mov_frame.idxmax()
#  y= mov_frame.max()
#  fig.annotate(x + ' days',
#             (mov_frame.index[x], mov_frame[name][y]),
#             xytext=(15, 15), 
#             textcoords='offset points',
#             arrowprops=dict(arrowstyle='-|>'))
  mov_frame.to_excel(str(lower) + str(upper) + name + currency + '.xlsx')
  return mov_frame

def mov_average_optim(data, number):
  mov_avg_int = number
 
 
  data['mov_avg'] = data.rolling(window=mov_avg_int).mean() #find moving average
  
  data['diff'] = data['px'] - data['mov_avg']
  data = data.dropna()
  test = np.sign(data['diff'])
  data['signchange'] = ((np.roll(test, 1) - test) != 0).astype(int) #Find all the points where moving average and px cross)    
  data['perf'] = (data['px'] - data['px'].shift(1))/data['px'].shift(1) #Calculate daily perf


  signals = data.copy()
  signals = signals[signals.signchange != 0]
  if signals['diff'][0] < 0:
    signals = signals.drop(signals.index[[0]])

  start_div = signals['px'][0]
  start = start_div
  buy = False         #Initiate this at false
  delay = 2           #Days of delay until trades
  changed = False     #Variable makes sure that first trade is a buy
  counter = 0         #Initiate lots variables
  trade_count = 0     #
  delay_list  = []    #
  trade_list  = []    #
  trade_dates = []    #
  dates       = []       #

  
  
#==============================================================================
#     Next part is a mess, sorry for whoever has to read this    
#==============================================================================
  
  for px, diff, perf, date, sign in zip(data['px'],data['diff'],data['perf'],data.index, data['signchange']):
    
    if sign == 1:
      trade_count += 1
      dates.append(date)
    
 
    if diff > 0 and sign == 1:
      if changed == False:
        changed = True
      if counter+delay < len(data.index):
        delay_list.append(data.index[counter+delay])

          
    if diff < 0 and sign == 1:
      if changed == False:
        pass
      else:
        if counter+delay < len(data.index):
          delay_list.append(data.index[counter+delay])
    
    if len(delay_list) > 0: 
      if delay_list[0] == date:
        buy = not buy
        delay_list.pop(0)     
    
    if buy:
      if date == signals.index[0]:
        data.at[date, 'portfolio_overall'] = start
        data.at[date, 'portfolio'] = start_div
      else:
        start = start * (perf +1)
        start_div = start_div * (perf +1)
        data.at[date, 'portfolio_overall'] = start
        data.at[date, 'portfolio'] = start_div
    else:
      data.at[date, 'portfolio_overall'] = start
      data.at[date, 'portfolio'] = start_div 
      data.at[date, 'perf'] = 0 

    counter =counter + 1

  print(trade_list)


  test = data.copy()
  test = test.drop('diff', axis=1)
  test = test.drop('signchange', axis=1)
  test = test.drop('perf', axis=1)   
#    test.plot(logy = True)
  


  
  
  return (data['portfolio_overall'][-1]-data['px'][-1])/data['px'][0]*100/(((data['px']-data['px'].mean())**2).sum()/len(data['px']))
    


