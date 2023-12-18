from tradeogre import TradeOgre
import json
import os
import time
import requests
from decimal import Decimal, getcontext
import sys
from datetime import datetime
import signal

os.system('cls')

print("Loading...")

sleeptime = 1

public_key = '3c4f364216f9fd099267843cf44577ad'
private_key = '6c7331cd667d63a627fa70e912bca041'
api_url = 'https://tradeogre.com/api/v1'
api_url_sell = '/order/sell'
api_url_buy = '/order/buy'
market_name = 'BTC-USDT'

transaction_type = api_url + "/order/buy"


# first no buy no data you got me ? lulz
quantity = 0
buy_quantity = 0
alpha_price = 0
last_transaction = ""
last_price_value = 0

differentiating_value_USDT_positive=500
differentiating_value_USDT_negative=-500
differentiating_value_percentage_positive=0.51
differentiating_value_percentage_negative=-0.51

# Set up the request headers with basic authentication
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',  # Add this line to explicitly specify JSON response
}
auth = (public_key, private_key)

to = TradeOgre(key=public_key, secret=private_key)
#to = TradeOgre(key="01191d89c2ad11ac5eabca84f6ebe9c3", secret="cf695053bce02950c4ab08124335e593")
#reply = to.balances(key="01191d89c2ad11ac5eabca84f6ebe9c3", secret="cf695053bce02950c4ab08124335e593")

# flag
flag = False

#data
data = {
'market': market_name,
'quantity': 0,
'price': 0
}


#

#with open('price.log', 'w'):
#    pass
#
while True:
    with open('price.log', 'r') as file:
        for line in file:
            content = line.strip()
            if content == "":
                content = ("0,0")
    # Your main code goes here

    # For demonstration purposes, let's have a loop that runs until Ctrl+C is pressed
  

        
    result_balance = to.balance('BTC')
    json_data = json.dumps(result_balance)
    btc_balance = json.loads(json_data)
   
    result_balance = to.balance('USDT')
    json_data = json.dumps(result_balance)
    usdt_balance = json.loads(json_data)
    
    
    result_ticker = to.ticker(market_name)
    json_data = json.dumps(result_ticker)
    btcusdt_price = json.loads(json_data)
    
    price_value = float(btcusdt_price['price'])
    btcusd_price_value = float(btcusdt_price['price'])
    # print(price_value)
        # Set up the request data
        
    buy_q = float(usdt_balance['balance']) / float(btcusdt_price['price'])
    buy_q = format(buy_q, '.8f')

    if last_price_value == price_value:
        pass  # You might want to add some code here if needed
    else:
        current_datetime = datetime.now()
        with open('price.log', 'a') as file:
            # Redirect standard output to the file      
            sys.stdout = file
            file.write(f"{price_value}, {current_datetime}\n")
            sys.stdout = sys.__stdout__
         
    last_price_value = price_value
        
    
    
    def remove_duplicates(file_path):
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

    #Example usage
    file_path = 'price.log'
    remove_duplicates(file_path)

        
    line_number_to_read = 0 # Initialize with the desired line number
    with open('price.log', 'r') as file:
        for line in file:
            
            if flag == False:
              
            #    print(line, end='\r')
            #    time.sleep(1)  # Just for demonstration, you can remove this in your actual implementation

                content = line.strip()
            #    print("Line Content:", content)
                print(content)
                # Split the line at the comma   
                parts = content.split(',')
                # Take the first part (everything before the comma)
                line_parts = parts[0].strip()
                line_parts2 = parts[1].strip()
                line_parts3 = line_parts2[:-7]
                
                
                
                
                
                checking_price_value = float(line_parts)    
                formatted_checking_price_value = "{:.8f}".format(checking_price_value)
                price_compare = price_value - checking_price_value     
                    
                
                sys.stdout = sys.__stdout__  
                if not line:
                    break                                                                                  
                
                # Example usage
                lines_to_print = ["Line 1", "Line 2", "Line 3"]

                # Initial print
            #    overwrite_last_line(lines_to_print[-1])

                # Overwrite with a new line
                new_line = "This is the new line"
            #    overwrite_last_line(new_line)

                alpha_price = btcusdt_price['price']
                
                beta_price = int(float(formatted_checking_price_value))
                
                perc_diff_alpha = float(alpha_price) + float(beta_price)            
                perc_diff_beta = float(alpha_price) - float(beta_price)
        
                perc_diff_gamma = perc_diff_alpha / 2
                
                perc_diff_delta =  perc_diff_beta / perc_diff_gamma
                
                perc_diff_sigma = perc_diff_delta * 100

                #print(result_ticker)
                print("\033[97m:")
                os.system('cls')
                current_datetime = datetime.now()
                print("Current Time   :", current_datetime)  
                print("\033[93mBTC  Balance   :", btc_balance['balance'])  
                print("\033[92mUSDT Balance   :", usdt_balance['balance'])  
                print("\033[94mBTC-USDT Price :", btcusdt_price['price'])
                print("\033[91mUSDT-BTC Power :", buy_q)
                print("\033[94m")
                if price_compare == 0:
                    perc_diff_sigma = 0
                print(formatted_checking_price_value,"\033[97m:", line_parts3, ": diff", price_compare, "or", perc_diff_sigma, "%" )
                with open('log.log', 'r') as file:
                    for line in file:
                        logz = line.strip()
                        # print(logz)
                
                
                #    print("Checking Price Value:", checking_price_value)
                #    print("Price Compare:", price_compare)
                
                # Add your condition here if needed
               
                
                    if perc_diff_sigma >= differentiating_value_percentage_positive:
                        print("Sell Condition Met!" )

                        
                        quantity = usdt_balance['balance']
                        transaction_type = api_url + api_url_sell
                        data = {
                        'market': market_name,
                        'quantity': quantity,
                        'price': btcusd_price_value
                        }   
                        
                        print("\033[91m",quantity)
                        with open('price.log', 'w') as file:                   
                            pass
                        flag = True
                        break
                        
                    if perc_diff_sigma <= differentiating_value_percentage_negative:
                        print("Buy Condition Met!" )
                        
                        alpha = float(btc_balance['balance'])
                        beta = float(btcusdt_price['price'])
                        quantity = alpha * beta
                        
                        transaction_type = api_url + api_url_buy
                        data = {
                        'market': market_name,
                        'quantity': quantity,
                        'price': btcusd_price_value
                        }   
                        
                        print("\033[92m",quantity)
                        with open('price.log', 'w') as file:
                            pass
                        flag = True
                        break
                        
                if flag == True:
                    break
                    
            # break  # Exit the loop since the desired line has been read    
    # selling is converting USDT to BTC
    # buying is converting BTC to USDT
    if flag == True:
        response = requests.post(transaction_type, headers=headers, auth=auth, data=data)
        flag = False
        if response.ok:
            json_response = response.json()
            try:
                # Try to parse the response as JSON
                with open('log.log', 'a') as file:
                # Redirect standard output to the file
                    file.write(f"{transaction_type} quantity: {quantity} price: {btcusdt_price}\n")
                    last_transaction = transaction_type, "quantity :", quantity, "price :", btcusdt_price
                    sys.stdout = file
                    sys.stdout = sys.__stdout__
                    print("No Last Transaction")
                    print(json_response)
                    
            except requests.exceptions.JSONDecodeError:
                # If parsing as JSON fails, print the raw response text
                with open('log.log', 'a') as file:
                    
                    print("No Last Transaction")
                    print(response.text)
        else:
        # Print the error status code and reason
            print(f"Error: {response.status_code} - {response.reason}")   
        #to.sell(market, balance, price)  # market, quantity, price
        #orders_result = to.orders(market)
        #print(orders_result)
        #result_orders = to.orders(market="BTC-LOKI")
        #print(result_orders)
        #result_order = to.order(uuid="1702a7bc-6a18-92c0-c1fe-aaf581d2352d")
        #print(result_order)