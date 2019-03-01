from dotenv import load_dotenv
import json
import os
import requests
import datetime
import csv
import statistics 



def to_usd(my_price):
    return "${0:,.2f}".format(my_price)


load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

# see: https://www.alphavantage.co/support/#api-key
#api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#print("API KEY: " + api_key) # TODO: remove or comment-out this line after you have verified the environment variable is getting read properly

api_key = os.environ.get("MY_API_KEY") #MY_API_KEY


#***************************
#Data validation:

message = "Please enter the stock symbol you'd like to analyze.  "

x = 1
while x == 1:
    sym_input = input(message)
    if sym_input.isalpha() != True:
        print("Please enter a 4 letter stock symbol")
    else:
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={sym_input}&apikey={api_key}"
        response = requests.get(request_url)

        if 'Error' in response.text:
            print ("Invalid input")
        else:
            break



#print(type(response))
#print(response.status_code)
#print(response.text)

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) #sort to ensure that the latest day is first
latest_day = dates[0]
latest_close = tsd[latest_day]["4. close"]


high_price_list = []
low_price_list = []
close_price_list = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_price_list.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_price_list.append(float(low_price))
    close_p = tsd[date]["4. close"]
    close_price_list.append(float(close_p))


#max of all the high prices...
recent_high = max(high_price_list) 

close_av = 120000
#close_av = statistics.mean(close_price_list)

recent_low = min(low_price_list)

# TODO: further parse the JSON response...




# TODO: traverse the nested response data structure to find the latest closing price and other values of interest...


latest_price_usd = "$100,000.00"

#
# INFO OUTPUTS
#

# TODO: write response data to a CSV file

os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv") # a relative filepath

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

#Writing info to file 
with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above

    #LOOP to write each row

    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": to_usd(float(daily_prices["1. open"])), 
            "high": to_usd(float(daily_prices["2. high"])) , 
            "low": to_usd(float(daily_prices["3. low"])), 
            "close": to_usd(float(daily_prices["4. close"])), 
            "volume": daily_prices["5. volume"]
        })

    #writer.writerow({"city": "New York", "name": "Mets"})
    #writer.writerow({"city": "Boston", "name": "Red Sox"})
    #writer.writerow({"city": "New Haven", "name": "Ravens"})




# TODO: further revise the example outputs below to reflect real information


t = datetime.datetime.now()
t.strftime("%Y-%m-%d %I:%M %p")

print("-----------------------------------")
print(f"STOCK SYMBOL: {sym_input}")
print("RUN AT: " + t.strftime("%Y-%m-%d %I:%M %p"))
print("-----------------------------------")
print(f"LATEST DAY OF AVAILABLE DATA: {last_refreshed}" )
print(f"LATEST DAILY CLOSING PRICE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH CLOSING PRICE: {to_usd(float(recent_high))}")
print(f"RECENT LOW CLOSING PRICE:{to_usd(float(recent_low))}")


# GIVE RECOMMENDATION__________________________
print("-----------------------------------")
if (  float(latest_close) > float(close_av)  ):
    print("RECOMMENDATION: Buy!")
    print("REASONING: The latest closing price is higher than the average closing price.")
else:
    print("RECOMMENDATION: DON'T BUY!")
    print("REASON: Because the latest closing price is less than the average closing price,")
    print("         we recommend you do not invest.")
print("-----------------------------------")
print("Writing info to csv" + str(csv_file_path))

