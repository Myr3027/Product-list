from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route('/add', methods=["POST"])
def add_product():
    name = request.form.get("name")
    price = request.form.get("price")
    country = request.form.get("country")
    
    if name and price and country:
        new_product = Product(name=name, price=float(price), country=country)
        db.session.add(new_product)
        db.session.commit()
    
    return redirect('/')

@app.route('/delete/<int:product_id>', methods=["POST"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:product_id>', methods=["GET", "POST"])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == "POST":
        product.name = request.form.get("name")
        product.price = float(request.form.get("price"))
        product.country = request.form.get("country")
        db.session.commit()
        return redirect('/')
    
    return render_template("edit.html", product=product)

if __name__ == '__main__':
    app.run(debug=True)
