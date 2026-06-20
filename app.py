import os
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY',
    'ehsconnect-dev'
)

@app.route('/')
def home():
    return 'EHS Connect'

if __name__ == '__main__':
    app.run(debug=True)
