from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, Column, String, Float, DateTime
from datetime import datetime
from main import get_weather_data

app = Flask(__name__)

# Database Configuration
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db" # SQLite database and location

db.init_app(app)

# Class to create a table in db to store search history from users
class Search(Base):
    __tablename__ = 'searches'
    
    id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False)
    temperature = Column(Float, nullable=False)
    searched_at = Column(DateTime, nullable=False)

# Create route to index.html through app.route
@app.route('/')
def index():
    return render_template('index.html', title="Home Page")

# Use GET method shortcut "app.get" to get /weather from index form
@app.get('/weather')
def get_weather():
    city_name = request.args.get('city_name')
    city_weather = get_weather_data(city_name)
    current_time = datetime.now()
    # If to check if city_weather isnt empty or wrong.
    if city_weather is not None:
        search = Search(city=city_name, temperature=city_weather['temperature'], searched_at=current_time)
        db.session.add(search)
        db.session.commit()
    return render_template('index.html', city_name=city_name, city_weather=city_weather)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
