from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('nutrition.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            calories INTEGER NOT NULL,
            protein REAL NOT NULL,
            carbs REAL NOT NULL,
            fat REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('nutrition.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM foods')
    foods = cursor.fetchall()
    conn.close()
    return render_template('index.html', foods=foods)

@app.route('/add', methods=['GET', 'POST'])
def add_food():
    if request.method == 'POST':
        name = request.form['name']
        calories = request.form['calories']
        protein = request.form['protein']
        carbs = request.form['carbs']
        fat = request.form['fat']

        conn = sqlite3.connect('nutrition.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO foods (name, calories, protein, carbs, fat)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, calories, protein, carbs, fat))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('add_food.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
