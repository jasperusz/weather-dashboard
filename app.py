from flask import Flask, render_template, request

app = Flask(__name__)

# Create route to index.html through app.route
@app.route('/')
def index():
    return render_template('index.html', title="Home Page")

# Use GET method shortcut "app.get" to get /weather from index form
@app.get('/weather')
def get_weather():
    city_name = request.args.get('city_name')
    return f'Weather Conditions from City {city_name}'

if __name__ == '__main__':
    app.run(debug=True)