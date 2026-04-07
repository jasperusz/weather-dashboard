import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('API_KEY') # Edit your API_KEY variable in .env file
city = input('Which City do you want to know the Weather? ')

if not city: # Condition check if city string is empty
    print('You need to type a City!')
else:
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
        print(f'Temperature: {temperature:.1f}ºC \n Min. Temperature: {min_temp:.1f}ºC \n Max. Temperature: {max_temp:.1f}ºC \n Humidity: {humidity}% \n Winds: {winds} m/s')
    else:
        print(f'Erro: {response.status_code}')
