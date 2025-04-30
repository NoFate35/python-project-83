import os
from flask import Flask
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

print("тооооокеееееннр", app.config['SECRET_KEY'])


@app.route('/')
def get_index():
    return "Heeeeeellloooo"
    