import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('API_KEY') # Edit your API_KEY variable in .env file

def get_weather_data(city):
    API_URL = (f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}')
    response = requests.get(API_URL)
    print(response)
    if response.status_code == 200:
        dados = response.json()
        temperature = dados['main']['temp']
        min_temp = dados['main']['temp_min']
        max_temp = dados['main']['temp_max']
        humidity = dados['main']['humidity']
        winds = dados['wind']['speed']
        return {
            'temperature': temperature,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'humidity': humidity,
            'winds': winds
        }
    else:
        return None
    