from dotenv import load_dotenv
import json
import os
import requests

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)


load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

# see: https://www.alphavantage.co/support/#api-key
#api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#print("API KEY: " + api_key) # TODO: remove or comment-out this line after you have verified the environment variable is getting read properly

symbol = "NFLX" # TODO: capture user input, like... input("Please specify a stock symbol: ")

# see: https://www.alphavantage.co/documentation/#daily (or a different endpoint, as desired)
# TODO: assemble the request url to get daily data for the given stock symbol...




# TODO: use the "requests" package to issue a "GET" request to the specified url, and store the JSON response in a variable...

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

response = requests.get(request_url)
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

for date in dates:
    high_price = tsd[date]["2. high"]
    high_price_list.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_price_list.append(float(low_price))


#max of all the high prices...
recent_high = max(high_price_list) 


recent_low = min(low_price_list)

# TODO: further parse the JSON response...




# TODO: traverse the nested response data structure to find the latest closing price and other values of interest...


latest_price_usd = "$100,000.00"

#
# INFO OUTPUTS
#

# TODO: write response data to a CSV file

# TODO: further revise the example outputs below to reflect real information
print("-----------------")
print(f"STOCK SYMBOL: {symbol}")
print("RUN AT: 11:52pm on June 5th, 2018")
print("-----------------")
print(f"LATEST DAY OF AVAILABLE DATA: {last_refreshed}" )
print(f"LATEST DAILY CLOSING PRICE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH CLOSING PRICE: {to_usd(float(recent_high))}")
print(f"RECENT AVERAGE LOW CLOSING PRICE:{to_usd(float(recent_low))}")
print("-----------------")
print("RECOMMENDATION: Buy!")
print("RECOMMENDATION REASON: Because the latest closing price is within threshold XYZ etc., etc. and this fits within your risk tolerance etc., etc.")
print("-----------------")