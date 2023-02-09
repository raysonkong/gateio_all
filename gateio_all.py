from requests import Request, Session
import requests
import json
import pprint
import datetime
import time
import os
from config import *

SLEEP_TIME = 0.2

## ==================================##
## setup config.py in the same folder
## ==================================##

EXCHANGES=["GATEIO"]  # only one

WANTED_CURRENCIES = ['USDT', 'BTC'] 


# # Do not alter below easily
GROUP_SIZE = len(EXCHANGES) * 1000

URL='https://data.gateio.co/api2/1/tickers'
## end of Config file


#===== Setup Date and Time #======== 
# Date
generation_date = datetime.datetime.now()
generation_date = generation_date.strftime("%d_%m_%Y")


# Time now
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
#print(current_time)


#generation_time = now.strftime("%H:%M:%S")


# ======================== ### 
## Making the Call
# ======================== ### 


# output: btc_usdt
response = requests.get(URL)
gateioInfo = response.json()

symbols = []  

def getList(dict):
    for key in dict.keys():
        symbols.append(key)

    return list

getList(gateioInfo)


# ======================== ### 
# selected wanted pairs
# ======================== ### 
selectedSymbols = []

for symbol in symbols:
    for currency in WANTED_CURRENCIES:
        currencyLen = len(currency)
        if symbol[-currencyLen:].lower() == currency.lower():
            selectedSymbols.append(symbol.upper())

#print(selectedSymbols)


# ======================== ### 
# Format the selectedSymbols
# ======================== ###

# input: ELF_USDT 
# output: GATEIO:ELFUSDT

## ====Helper: remove '_' ====== #
def removeUnderscore(symbol):
    newsymbol = ''
    for char in symbol:
        if char != '_':
            newsymbol+=char
    return newsymbol

#print(removeUnderscore('BTC_USDT'))

formattedSymbol = []
for symbol in selectedSymbols:
    formattedSymbol.append(EXCHANGES[0] + ":" + removeUnderscore(symbol))

#print(formattedSymbol)





#================================================
# Group output from Last Step
# to a list containing lists of n 
# =============================================== ### 

# Group size, in production n=400
n=GROUP_SIZE

def group_into_n(data_list, n):
    return [data_list[i:i+n] for i in range(0, len(data_list), n)]

#test = [1,2,3,4,5,6,7,8]
#print(group_into_n(test, n))

grouped_pairs = group_into_n(formattedSymbol, n)

#print(grouped_pairs)


#================================================
# Step 5 #

# write a function to output each of the group in step 4 
# to a separate file
# =============================================== ### 


#def output_to_text_file(nested_grouped_pairs):
#    for idx, group in enumerate(nested_grouped_pairs):
#        with open(f'{idx+1}CMC p.{idx+1} {generation_date}.txt ', 'w') as f:
#            for pair in group:
#                f.write("%s,\n" % pair)


# /Users/raysonkong/code/python/webscrapping/scripts_v2/cmc_api_to_tradingview/outputs
def output_to_text_file(nested_grouped_pairs):
    for idx, group in enumerate(nested_grouped_pairs):
            filename=f"{os.getcwd()}/{EXCHANGES[0]}_ALL_{generation_date}total/-1.0 {EXCHANGES[0]}_ALL p.{idx+1} ({generation_date}).txt"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                for pair in group:
                  f.write("%s,\n" % pair)

#output_to_text_file(grouped_pairs)


def run_srapper():
    os.system('clear')
    output_to_text_file(grouped_pairs)


    print("== CMC Scrapping Completed ==")
    print('\n')
    #print("======================================================")
if __name__ =='__main__':
    run_srapper()

