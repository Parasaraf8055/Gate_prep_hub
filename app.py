from flask import Flask, render_template, request ,url_for,  redirect , session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Parasaraf@8055",       # Put your MySQL password here
    database="gateprep"
)

cursor = db.cursor()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        if user:
            session['user'] = user[1]
            return redirect('/')
        else:
            return render_template("login.html", error="Invalid Credentials")
    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        import random
        tip = random.choice(daily_tips)
        return render_template('dashboard.html', user=session['user'], tip_of_the_day=tip)
    else:
        return redirect(url_for('login'))
    
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Contact form submitted by {name} ({email}): {message}")
        return render_template('contact.html', success=True)
    return render_template('contact.html')    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            db.commit()
            return redirect('/login')
        except:
            return render_template("register.html", error="Email already registered!")
    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/')
def home():
    return render_template('index.html') 



@app.route('/syllabus')
def syllabus():
    return render_template('syllabus.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

import random
from datetime import datetime

# Daily tips for GATE aspirants
daily_tips = [
    "Stay consistent and focus on your weak areas!",
    "Remember to take breaks while studying, it helps you retain more information.",
    "Set a schedule and stick to it. Time management is key for GATE prep.",
    "Don’t just study, practice! Solving previous years' papers is a must.",
    "Take care of your health; a healthy body keeps the mind sharp."
]







if __name__ == '__main__':
    app.run(debug=True)
