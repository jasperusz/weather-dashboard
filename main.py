import requests
api_key = 'your_api_key'
city = 'São Paulo'
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
    print(f'Temperature:{temperature} Min Temperature:{min_temp} Max Temp:{max_temp} Humidity:{humidity} Winds:{winds}')
else:
    print(f'Erro: {response.status_code}')


