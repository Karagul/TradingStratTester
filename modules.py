# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 11:20:41 2018

@author: T58830
"""

import pandas as pd 
import numpy as np


def mean_reversal(inp, number, curr, nr_stdev):
  mov_avg_int = number
  
  inp = inp.dropna()
  data = pd.DataFrame()
  data['px'] = inp.div(curr)
  data = data.dropna()
    
  cop = data.copy()
  data['mov_avg'] = cop.rolling(window=mov_avg_int).mean() #find moving average
  data.dropna()  
  
  data['per'] = (data['px'] - data['mov_avg'])/data['mov_avg']*100
  
  differs = data['per']
  
  stdev = np.std(differs)
  
  signs = []
  diffs = []
  buy = False
  
  
  for diff in differs:
    if diff > nr_stdev*stdev and buy == True:
      signs.append(1)
      diffs.append(1)
      buy = False
    elif diff < -nr_stdev*stdev and buy == False:
      signs.append(1)
      diffs.append(-1)
      buy = True
    else:
      signs.append(0)
      diffs.append(0)
  
  data['diff'] = diffs
  data['signs'] = signs
  
  return data['signs'], data['diff']


def derivative_strat(inp, number,curr):
  mov_avg_int = number
  inp = inp.dropna()
  data = pd.DataFrame()
  data['px'] = inp.div(curr)
  data = data.dropna()
  
  cop = data.copy()
  data['mov_avg'] = cop.rolling(window=mov_avg_int).mean() #find moving average
  data['mov_avg_short'] = cop.rolling(window=200).mean() #find moving average
  
  data['diff'] = data['px'] - data['mov_avg']
  test = np.sign(data['diff'])
  data['signchange_200'] = ((np.roll(test, 1) - test) != 0).astype(int) #Find all the points where moving average and px cross)    
  data['perf'] = (data['px'] - data['px'].shift(1))/data['px'].shift(1) #Calculate daily perf

  data['mov_avg_diff'] = data['mov_avg']-data['mov_avg'].shift(1)
  data = data.dropna()
  
  data['deriv_sign'] = np.where(data['mov_avg_diff'] > 0, 1, 0)



  
  test = data['signchange_200'].copy()
  first_buy = ''
  counter = 0
  while first_buy == '':
    if test[counter] == 1 and data['diff'][counter] > 0:
      first_buy = counter 
    counter += 1
  
  
  buy = False
  counter = 0
  sign_change_deriv = []
  for sign, deriv,diff,shoravg,px,longavg in zip(data['signchange_200'],data['deriv_sign'],data['diff'],data['mov_avg_short'],data['px'],data['mov_avg']):
      if buy == False and deriv == 1 and px >shoravg:
        sign_change_deriv.append(1)
        buy = True       
      elif buy == False and sign == 1 and deriv == 1 and diff > 0:
        sign_change_deriv.append(1)
        buy = True
      elif buy == True and sign == 1 and diff < 0:
        sign_change_deriv.append(1)
        buy = False
      else:
        sign_change_deriv.append(0)
      counter += 1
  
  data['signchange_deriv'] = sign_change_deriv    
  data = data.dropna()    
  
  return data['signchange_deriv'], data['diff']
  
def mov_avg(inp, number,curr):   
  mov_avg_int = number
  inp = inp.dropna()
  data = pd.DataFrame()
  
  data['px'] = inp.div(curr)
  data = data.dropna()
  
  data['mov_avg'] = data.rolling(window=mov_avg_int).mean() #find moving average
  data['diff'] = data['px'] - data['mov_avg']
  test = np.sign(data['diff'])
  data['signchange'] = ((np.roll(test, 1) - test) != 0).astype(int) #Find all the points where moving average and px cross)  
  data = data.dropna()
#  data = data.dropna()
  return data['signchange'], data['diff']
   
def golden_cross(inp, number,curr):   
  mov_avg_int = number
  inp = inp.dropna()
  data = pd.DataFrame()
  data['px'] = inp.div(curr)
  data = data.dropna()
  
  mov_avg_int1 = mov_avg_int
  mov_avg_int2 = 50    

  px = pd.Series()
  px = data['px']
  data['mov_avg_200'] =     px.rolling(window=mov_avg_int1).mean() #find moving average
  data['mov_avg_50']  =     px.rolling(window=mov_avg_int2).mean()
 
  data['diff_50_200'] = data['mov_avg_50'] - data['mov_avg_200']
  
  data = data.dropna()
  series1 = np.sign(data['diff_50_200'])
  data['signchange_50_200'] = ((np.roll(series1, 1) - series1) != 0).astype(int) 
  signals = data.copy()
  signals = signals[signals['signchange_50_200'] != 0]
  if signals['diff_50_200'][0] < 0:
    signals = signals.drop(signals.index[[0]])
  return data['signchange_50_200'], data['diff_50_200']

def simulator(px, signs, diff, curr):   
  data = pd.DataFrame()
  data['signchange'] = signs

  data['px_usd'] = px 
  data['px_curr'] = px.div(curr)
  data = data.dropna()
  data['diff'] = diff
  data['perf'] = (data['px_curr'] - data['px_curr'].shift(1))/data['px_curr'].shift(1) #Calculate daily perf
  
  perf = pd.DataFrame()
  perf['perf'] = data['perf']
  perf['curr'] = curr  
  perf['currperf'] = (perf['curr'] - perf['curr'].shift(1))/perf['curr'].shift(1)   
  
  data['curr_adj_perf'] = (perf['perf'] +1)/(perf['currperf']+1)-1
  
  data = data.dropna()
  signals = data.copy()
  signals = signals[signals.signchange != 0]
  
  if signals['diff'][0] < 0:
    signals = signals.drop(signals.index[[0]])

  start = signals['px_curr'][0]
  buy = False         #Initiate this at false
  delay = 2           #Days of delay until trades
  changed = False     #Variable makes sure that first trade is a buy
  counter = 0         #Initiate lots variables
  delay_list  = []    #
  dates = []
  
  print(data)
  for px, diff, perf, date, sign in zip(data['px_curr'],data['diff'],data['curr_adj_perf'],data.index, data['signchange']):
   
    if sign == 1:
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
      else:
        start = start * (perf +1)
        data.at[date, 'portfolio_overall'] = start
    else:
      if changed:
        data.at[date, 'portfolio_overall'] = start
      else:
        data.at[date, 'portfolio_overall'] = None
        
    counter =counter + 1
  
  time = pd.DataFrame()
  time['date'] = dates
  time['previous_date'] = time['date'].shift(1)
  time = time.drop(time.index[[0]])
  time['difference'] = (time['date']-time['previous_date']).dt.days
  meanval = time['difference'].mean()
  maxval = max(time['difference'])
  minval = min(time['difference'])
  med = np.median(time['difference'])
  
  ml = [len(dates),meanval,maxval,minval,med]
  copy = data['portfolio_overall'] 
  copy = copy.dropna()

  return copy, ml
  
def simulator_error_check(px, signs, diff, curr, err_days):   
  data = pd.DataFrame()
  data['signchange'] = signs

  data['px_usd']  = px 
  data['px_curr'] = px.div(curr)
  data = data.dropna()
  data['diff'] = diff
  data['perf'] = (data['px_curr'] - data['px_curr'].shift(1))/data['px_curr'].shift(1) #Calculate daily perf
  
  perf = pd.DataFrame()
  perf['perf'] = data['perf']
  perf['curr'] = curr  
  perf['currperf'] = (perf['curr'] - perf['curr'].shift(1))/perf['curr'].shift(1)   
  
  data['curr_adj_perf'] = (perf['perf'] +1)/(perf['currperf']+1)-1
  
  data = data.dropna()
  signals = data.copy()
  signals = signals[signals.signchange != 0]
  
  if signals['diff'][0] < 0:
    signals = signals.drop(signals.index[[0]])

  start       = signals['px_curr'][0]
  buy         = False         #Initiate this at false
  delay       = 2           #Days of delay until trades
  changed     = False     #Variable makes sure that first trade is a buy
  counter     = 0         #Initiate lots variables
  delay_list  = []    
  dates       = []
  error_list  = []
  error_count = 0
  
  print(data)
  for px, diff, perf, date, sign in zip(data['px_curr'],data['diff'],data['curr_adj_perf'],data.index, data['signchange']):
   
    if sign == 1:
      dates.append(date)
    if diff > 0 and sign == 1:
      if changed == False:
        changed = True
      if counter+delay < len(data.index):
        delay_list.append(data.index[counter+delay])
      if counter+delay+err_days < len(data.index):
        error_list.append((data.index[counter+delay],px))

          
    if diff < 0 and sign == 1:
      if changed == False:
        pass
      else:
        if counter+delay < len(data.index):
          delay_list.append(data.index[counter+delay])
          
    
    if len(error_list) > 0:       
      if error_list[0][0] == date:
        if error_list[0][1] > px:
          error_count += 1
          error_list.pop(0)
        else:
          error_list.pop(0)

    if len(delay_list) > 0:       
      if delay_list[0] == date:
        buy = not buy
        if buy == False:
          if len(error_list) > 0:       
            if error_list[0][1] > px:
              error_count += 1
              error_list.pop(0)
            else:
              error_list.pop(0)
        delay_list.pop(0)    
    
    
    if buy:
      if date == signals.index[0]:
        data.at[date, 'portfolio_overall'] = start
      else:
        start = start * (perf +1)
        data.at[date, 'portfolio_overall'] = start
    else:
      if changed:
        data.at[date, 'portfolio_overall'] = start
      else:
        data.at[date, 'portfolio_overall'] = None
    

    counter =counter + 1
  
  time = pd.DataFrame()
  time['date'] = dates
  time['previous_date'] = time['date'].shift(1)
  time = time.drop(time.index[[0]])
  time['difference'] = (time['date']-time['previous_date']).dt.days


  
  meanval = time['difference'].mean()
  maxval = max(time['difference'])
  minval = min(time['difference'])
  med = np.median(time['difference'])
  
  ml = [len(dates),meanval,maxval,minval,med,error_count]
  copy = data['portfolio_overall'] 
  copy = copy.dropna()
  print(ml)
  return copy, ml, time['difference']