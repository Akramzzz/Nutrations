from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('nutrition.db') as conn:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            weight INTEGER, 
            age INTEGER, 
            phone TEXT, 
            diet TEXT
        )
        ''')
        conn.commit()

# Ensure the DB is initialized correctly
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    weight = request.form['weight']
    age = request.form['age']
    phone = request.form['phone']
    diet = request.form['diet']
    
    with sqlite3.connect('nutrition.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (name, weight, age, phone, diet) VALUES (?, ?, ?, ?, ?)", (name, weight, age, phone, diet))
        conn.commit()
    
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        phone = request.form['phone']  # Search by phone number
        with sqlite3.connect('nutrition.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE phone=?", (phone,))
            results = c.fetchall()
    
    return render_template('search.html', results=results)

@app.route('/update_diet/<int:id>', methods=['POST'])
def update_diet(id):
    diet = request.form['diet']
    print(f"Updating diet for user ID {id} to: {diet}")  # Debugging line
    
    # Update the diet plan in the users table
    with sqlite3.connect('nutrition.db') as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET diet=? WHERE id=?", (diet, id))
        conn.commit()

    return redirect(url_for('search'))

@app.route('/delete_user/<int:id>', methods=['GET'])
def delete_user(id):
    with sqlite3.connect('nutrition.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (id,))
        conn.commit()

    return redirect(url_for('search'))  # Or you can redirect to the index page if you prefer


if __name__ == '__main__':
    app.run(debug=True)
