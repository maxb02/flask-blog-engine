from app import app
from flask import render_template

@app.route('/')
def index():
    name = 'Jack'
    return render_template('index.html', n=name)

