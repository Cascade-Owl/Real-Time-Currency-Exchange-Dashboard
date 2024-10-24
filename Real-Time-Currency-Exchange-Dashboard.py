from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import requests
from dotenv import load_dotenv
import os

# Gets API key from the environmental variables
load_dotenv()
api_key = os.getenv('API_KEY')

# Retrieve weather data from API in JSON format
Currency_Exchange_API = f'https://api.twelvedata.com/currency_conversion?symbol=USD/PHP,USD/EUR&amount=1&format=JSON&apikey={api_key}'
response = requests.get(Currency_Exchange_API)
Currency_Exchange_API_JSON = response.json()

# Store values to plot
USD_TO_PHP_Values = []
USD_TO_EURO_Values = []
Timestamp_Values = []

fig, (php, euro) = plt.subplots(2, 1)

# Updates the response by making a new API request
def update_response():
    response = requests.get(Currency_Exchange_API)

    return response.json()

# Create and animate the plot, called at each frame interval
def plot_animation(frame):
    UPDATED_Currency_Exchange_API_JSON = update_response()

    USD_TO_PHP_Rate = UPDATED_Currency_Exchange_API_JSON['USD/PHP']['rate']
    USD_TO_EURO_Rate = UPDATED_Currency_Exchange_API_JSON['USD/EUR']['rate']
    Timestamp = datetime.now().strftime('%H:%M:%S')
    
    USD_TO_PHP_Values.append(USD_TO_PHP_Rate)
    USD_TO_EURO_Values.append(USD_TO_EURO_Rate)
    Timestamp_Values.append(Timestamp)

    php.cla()
    euro.cla()


    # Plot when there are fewer than 2 plot data points
    if len(USD_TO_PHP_Values) < 2 and len(USD_TO_EURO_Values) < 2:

        php.plot(Timestamp_Values, USD_TO_PHP_Values, label='USD-PHP Rate', color = 'blue', marker='o')
        php.set_xlabel('Time')
        php.set_ylabel('1 USD To PHP Rate')
        php.set_ylim(USD_TO_PHP_Rate-0.1, USD_TO_PHP_Rate+0.1)
        php.legend()
        php.grid(True)
        php.text(0.9945, 0.025, f'Current Rate: {USD_TO_PHP_Rate} PHP', verticalalignment='bottom', horizontalalignment='right', 
                 transform=php.transAxes, color='black', fontsize=11,
                 bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.5'))

        euro.plot(Timestamp_Values, USD_TO_EURO_Values, label='USD-EURO Rate', color = 'violet', marker='o')
        euro.set_xlabel('Time')
        euro.set_ylabel('1 USD To EURO Rate')
        euro.set_ylim(USD_TO_EURO_Rate-0.1, USD_TO_EURO_Rate+0.1)
        euro.legend()
        euro.grid(True)
        euro.text(0.9945, 0.025, f'Current Rate: {USD_TO_EURO_Rate} EUR', verticalalignment='bottom', horizontalalignment='right', 
                  transform=euro.transAxes, color='black', fontsize=11,
                  bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.5'))
    
    # Plot when there are between 2 and 9 plot data points
    elif len(USD_TO_PHP_Values) in range(2, 10) and len(USD_TO_EURO_Values) in range(2, 10):
        
        php.plot(Timestamp_Values, USD_TO_PHP_Values, label='USD-PHP Rate', color = 'blue', marker='o')
        php.set_xlabel('Time')
        php.set_ylabel('1 USD To PHP Rate')
        php.set_ylim(min(USD_TO_PHP_Values)-0.01, max(USD_TO_PHP_Values)+0.01)
        php.legend()
        php.grid(True)
        php.text(0.9945, 0.025, f'Current Rate: {USD_TO_PHP_Rate} PHP', verticalalignment='bottom', horizontalalignment='right', 
                 transform=php.transAxes, color='black', fontsize=11,
                 bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.5'))

        euro.plot(Timestamp_Values, USD_TO_EURO_Values, label='USD-EURO Rate', color = 'violet', marker='o')
        euro.set_xlabel('Time')
        euro.set_ylabel('1 USD To EURO Rate')
        euro.set_ylim(min(USD_TO_EURO_Values)-0.01, max(USD_TO_EURO_Values)+0.01)
        euro.legend()
        euro.grid(True)
        euro.text(0.9945, 0.025, f'Current Rate: {USD_TO_EURO_Rate} EUR', verticalalignment='bottom', horizontalalignment='right', 
                  transform=euro.transAxes, color='black', fontsize=11,
                  bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.5'))
        
    # Plot when there are more than 9 plot data points (removes the oldest plot data point)
    elif len(USD_TO_PHP_Values) > 9 and len(USD_TO_EURO_Values) > 9:

        USD_TO_PHP_Values.pop(0)
        USD_TO_EURO_Values.pop(0)
        Timestamp_Values.pop(0)

        php.plot(Timestamp_Values, USD_TO_PHP_Values, label='USD-PHP Rate', color = 'blue', marker='o')
        php.set_xlabel('Time')
        php.set_ylabel('1 USD To PHP Rate')
        php.set_ylim(min(USD_TO_PHP_Values)-0.01, max(USD_TO_PHP_Values)+0.01)
        php.legend()
        php.grid(True)
        php.text(0.9945, 0.025, f'Current Rate: {USD_TO_PHP_Rate} PHP', verticalalignment='bottom', horizontalalignment='right', 
                 transform=php.transAxes, color='black', fontsize=11,
                 bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.5'))
        
        euro.plot(Timestamp_Values, USD_TO_EURO_Values, label='USD-EURO Rate', color = 'violet', marker='o')
        euro.set_xlabel('Time')
        euro.set_ylabel('1 USD To EURO Rate')
        euro.set_ylim(min(USD_TO_EURO_Values)-0.01, max(USD_TO_EURO_Values)+0.01)
        euro.legend()
        euro.grid(True)
        euro.text(0.9945, 0.025, f'Current Rate: {USD_TO_EURO_Rate} EUR', verticalalignment='bottom', horizontalalignment='right', 
                  transform=euro.transAxes, color='black', fontsize=11,
                  bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.5'))
        
# Create an animation that updates the plot every 19 seconds
animation = FuncAnimation(fig, plot_animation, interval=19000)

plt.tight_layout()
plt.show()

