from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('nutrition.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, weight INTEGER, age INTEGER)''')
        conn.commit()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    weight = request.form['weight']
    age = request.form['age']
    with sqlite3.connect('nutrition.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (name, weight, age) VALUES (?, ?, ?)", (name, weight, age))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        age = request.form['age']
        with sqlite3.connect('nutrition.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE age=?", (age,))
            results = c.fetchall()
    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
