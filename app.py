from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, Column, String, Float, DateTime, create_engine
from datetime import datetime
from main import get_weather_data
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

# Database Configuration
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
USER = os.getenv('USER')
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db.init_app(app)

# OAuth Configuration

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Class to create a table in db to store search history from users
class Search(Base):
    __tablename__ = 'searches'
    
    id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False)
    temperature = Column(Float, nullable=False)
    searched_at = Column(DateTime, nullable=False)
    weather_description = Column(String(100), nullable=False)
    weather_icon = Column(String(10), nullable=False)
    city_country = Column(String(10), nullable=False)
    user_email = Column(String(100), nullable=True)

# Create route to index.html through app.route
@app.route('/')
def index():
    user=session.get('user')
    return render_template('index.html', title="Home Page", user=user)

# Create route to login
@app.route('/login')
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

# Create route to logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Create route to callback after login
@app.route('/auth/callback')
def auth_callback():
    token = google.authorize_access_token()
    user_info = token.get('userinfo') 
    session['user'] = user_info
    session['email'] = user_info['email']
    return redirect(url_for('index'))

# Create route to get weather search history
@app.route('/history')
def history():
    if session.get('user'):
        search_history = db.session.execute(
            db.select(Search).where(
                Search.user_email == session.get('email')).order_by(
                    Search.searched_at.desc())).scalars().all()
        return render_template('history.html', search_history=search_history, user=session.get('user'))
    else:
        return redirect(url_for('index'))

# Use GET method shortcut "app.get" to get /weather from index form
@app.get('/weather')
def get_weather():
    city_name = request.args.get('city_name')
    city_weather = get_weather_data(city_name)
    current_time = datetime.now()
    user_email = session.get('email')
    # If to check if city_weather isnt empty or wrong.
    if city_weather is not None:
        weather_description = city_weather['weather_description']
        weather_icon = city_weather['weather_icon']
        city_country = city_weather['city_country']
        search = Search(
            city=city_name, 
            temperature=city_weather['temperature'], 
            searched_at=current_time, 
            weather_description=weather_description, 
            weather_icon=weather_icon, 
            city_country=city_country, 
            user_email=user_email)
        db.session.add(search)
        db.session.commit()
    return render_template('index.html', city_name=city_name, city_weather=city_weather, user=session.get('user'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
