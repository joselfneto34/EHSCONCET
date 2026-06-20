import os
from flask import Flask, render_template

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY',
    'ehsconnect-dev'
)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
