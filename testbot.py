# Import Modules
import os
import sys
import time
import json
import signal
import requests
from datetime import datetime
from tradeogre import TradeOgre
# Set User Data
public_key = '3c4f364216f9fd099267843cf44577ad'
private_key = '6c7331cd667d63a627fa70e912bca041'
market_name = 'BTC-USDT'
ask_diff = 0.33333333
diff_value_percentage_pos = 0.50
diff_value_percentage_neg = diff_value_percentage_pos * -1
auth = (public_key, private_key)
trading_live = True
# Set Api Data
to = TradeOgre(key=public_key, secret=private_key)
api_url = 'https://tradeogre.com/api/v1'
api_url_sell = '/order/sell'
api_url_buy = '/order/buy'
transaction_type = api_url + api_url_buy
# Set Init Data
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',  # Add this line to explicitly specify JSON response
}
default_data = {
'market': market_name,
'quantity': "0",
'price': "0"
}  
json_response = "No Transaction"   
# Set Colors
gry_color = "\033[90m"
red_color = "\033[91m"
gre_color = "\033[92m"
blu_color = "\033[94m"
wht_color = "\033[97m"
if market_name == 'BTC-USDT':
    currency0_color = "\033[93m"
    currency1_color = "\033[92m"
os.system('cls')
print("Loading...")  
def remove_duplicates():
    file_path = 'price.log'
    unique_lines = set()
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        for line in lines:
            # Extract content before the comma
            key = line.split(',')[0]         
            # Check if content before comma is unique
            if key not in unique_lines:
                file.write(line)
                unique_lines.add(key)       
def process_and_display(json_response):
    data = {
    'market': market_name,
    'quantity': "0",
    'price': "0"
    }  
    flag = False
    result_ticker = to.ticker(market_name)
    current_datetime = str(datetime.now())
    price = result_ticker['price']
    while True:
        remove_duplicates()
        with open('price.log', 'a') as file:
                file.write(f"{price}, {current_datetime}\n")            
        with open('price.log', 'r') as file:
            for line in file:                        
                log_check = line                   
                #Get Data
                current_datetime = str(datetime.now())
                result_ticker = to.ticker(market_name)
                initialprice = result_ticker['initialprice']
                price = result_ticker['price']
                high = result_ticker['high']
                low = result_ticker['low']
                volume = result_ticker['volume']
                bid = result_ticker['bid']
                ask = result_ticker['ask']  
                parts = market_name.split('-')
                currency0 = parts[0].strip()
                currency0_balance = to.balance(currency0)['balance']  
                parts = market_name.split('-')
                currency1 = parts[1].strip()
                currency1_balance = to.balance(currency1)['balance']                                  
                # Count Amount Of Line In Price Log           
                parts = log_check.split(',')
                compare_price = parts[0].strip()                                                         
                difference_price_neg = float(price) - float(compare_price)
                difference_price_pos = float(price) + float(compare_price)
                difference_price = round(difference_price_neg, 2)                    
                difference_price_div_a = difference_price_pos / 2
                difference_price_div_b = difference_price_neg / difference_price_div_a                    
                difference_price_percentage = difference_price_div_b * 100
                difference_price_percentage_rounded = round(difference_price_percentage, 2)             
                diff = float(price) - float(ask)
                price_diff_neg = diff*ask_diff+diff
                price_diff_pos = diff*ask_diff+diff
                # Process Complete, Reset Display
                print(wht_color)
                os.system('cls')
                print(wht_color + "Date Time    : " + current_datetime)
                print(wht_color + "Market       : " + currency0_color + currency0 + wht_color + "-" + currency1_color + currency1)
                print(gry_color + "initialprice : $" + initialprice)
                print(wht_color + "price        : $" + price)
                print(gry_color + "high         : $" + high)
                print(wht_color + "low          : $" + low)
                print(gry_color + "volume       : $" + volume)
                print(wht_color + "bid          : $" + bid)
                print(gry_color + "ask          : $" + ask)
                print("")
                print(wht_color + "User         : " + public_key)    
                print(currency0 + " Bal      : ₿" + currency0_color + currency0_balance + wht_color)
                print(currency1 + " Bal     : $" + currency1_color + currency1_balance)
                print("")
                print(wht_color + "Trading Live : " + str(trading_live))
                print("")
                print(wht_color + "Checking log : $" + red_color + log_check)
                print(wht_color + "Live Price   : $" + gre_color + price)
                print(wht_color + "Difference   : $" + str(difference_price) + " %" + str(difference_price_percentage_rounded))
                print(wht_color + "Price vs Ask : $" + str(diff))
                print(wht_color + "Diff*Ask+Diff: $" + str(price_diff_neg))
                print("")
                print("previous server response...")
                print("@ market: " + data['market'] + " quantity: " + data['quantity'] + " price: " + data['price'])
                print("previous transaction response: " + str(json_response))
                # Display Complete, Continue Live Process
                if difference_price_percentage > diff_value_percentage_pos:
                    print("")
                    print(red_color + "Sell Condition Met!" + wht_color)
                    quantity = currency0_balance
                    transaction_type = api_url + api_url_sell       
                    data = {
                    'market': market_name,
                    'quantity': quantity,
                    'price': bid
                    }
                    response = requests.post(transaction_type, headers=headers, auth=auth, data=data)
                    print("@ market: " + data['market'] + " quantity: " + data['quantity'] + " price: " + data['price'])
                    print("server response...")
                    flag = False
                    if response.ok:
                        json_response = response.json()
                        print(json_response)
                        with open('log.log', 'a') as file:
                            file.write(f"{json_response}\n")
                    else:
                    # Print the error status code and reason
                        print(response.text)
                        print(f"Error: {response.status_code} - {response.reason}")                        
                    time.sleep(1)
                    with open('price.log', 'w') as file:
                        file.write(f"{price}, {current_datetime}\n")
                    init_process(json_response)
                if difference_price_percentage < diff_value_percentage_neg:
                    print("")
                    print(gre_color + "Buy Condition Met!" + wht_color)
                    quantity = currency1_balance
                    transaction_type = api_url + api_url_buy
                    data = {
                    'market': market_name,
                    'quantity': quantity,
                    'price': ask
                    }   
                    response = requests.post(transaction_type, headers=headers, auth=auth, data=data)
                    print("@ market: " + data['market'] + " quantity: " + data['quantity'] + " price: " + data['price'])
                    print("server response...")
                    flag = False
                    if response.ok:
                        json_response = response.json()
                        print(json_response)
                        with open('log.log', 'a') as file:
                            file.write(f"{json_response}\n")
                    else:
                    # Print the error status code and reason
                        print(response.text)
                        print(f"Error: {response.status_code} - {response.reason}")                        
                    time.sleep(1)
                    with open('price.log', 'w') as file:
                        file.write(f"{price}, {current_datetime}\n")
                    init_process(json_response)
def init_process(json_response):
    #Get Data
    current_datetime = str(datetime.now())
    result_ticker = to.ticker(market_name)
    initialprice = result_ticker['initialprice']
    price = result_ticker['price']
    high = result_ticker['high']
    low = result_ticker['low']
    volume = result_ticker['volume']
    bid = result_ticker['bid']
    ask = result_ticker['ask']  
    parts = market_name.split('-')
    currency0 = parts[0].strip()
    currency0_balance = to.balance(currency0)['balance']  
    parts = market_name.split('-')
    currency1 = parts[1].strip()
    currency1_balance = to.balance(currency1)['balance']
    process_and_display(json_response)
#process_and_display()
init_process(json_response)