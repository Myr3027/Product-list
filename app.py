from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("products.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            price REAL,
                            country TEXT)''')
        conn.commit()

init_db()

@app.route('/')
def index():
    with sqlite3.connect("products.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    return render_template("index.html", products=products)

@app.route('/add', methods=["POST"])
def add_product():
    name = request.form.get("name")
    price = request.form.get("price")
    country = request.form.get("country")
    
    if name and price and country:
        with sqlite3.connect("products.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, country) VALUES (?, ?, ?)", (name, price, country))
            conn.commit()
    
    return redirect('/')

@app.route('/delete/<int:product_id>', methods=["POST"])
def delete_product(product_id):
    with sqlite3.connect("products.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

