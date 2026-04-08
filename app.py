from flask import Flask, render_template, request
from main import get_weather_data

app = Flask(__name__)

# Create route to index.html through app.route
@app.route('/')
def index():
    return render_template('index.html', title="Home Page")

# Use GET method shortcut "app.get" to get /weather from index form
@app.get('/weather')
def get_weather():
    city_name = request.args.get('city_name')
    city_weather = get_weather_data(city_name)
    return f'Weather Conditions from City {city_name}: {city_weather}'

if __name__ == '__main__':
    app.run(debug=True)