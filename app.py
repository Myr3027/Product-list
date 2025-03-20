import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from admin import admin
from config import Config
from extensions import db, login_manager
from forms import LoginForm, RegistrationForm
from models import Product, User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
admin.init_app(app)

UPLOAD_FOLDER = "static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    try:
        with app.app_context():
            products = Product.query.all()
        return render_template("index.html", products=products)
    except Exception as e:
        flash(f"Помилка загрузки продуктів: {e}", "danger")
        return render_template("index.html", products=[])

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        with app.app_context():
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash("Користувач вже існує!", "danger")
                return redirect(url_for("register"))

            hashed_password = generate_password_hash(form.password.data)
            user = User(username=form.username.data, password=hashed_password)

            db.session.add(user)
            db.session.commit()

            flash("Реєстрація успішна!", "success")
            login_user(user)
            return redirect(url_for("index"))

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with app.app_context():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Успішний вхід!", "success")
                return redirect(url_for("index"))
        flash("Неправильний логін або пароль", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/add", methods=["POST"])
@login_required
def add_product():
    name = request.form.get("name")
    price = request.form.get("price")
    country = request.form.get("country")
    description = request.form.get("description")
    picture = request.files.get("picture")

    if name and price and country:
        new_product = Product(
            name=name,
            price=float(price),
            country=country,
            description=description,
            picture=picture.filename if picture else None
        )
        try:
            if picture and picture.filename:
                picture_path = os.path.join(UPLOAD_FOLDER, picture.filename)
                picture.save(picture_path) 

            db.session.add(new_product)
            db.session.commit()
            flash("Продукт додано!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Помилка додавання продукту: {e}", "danger")

    return redirect(url_for("index"))

@app.route("/delete/<int:product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        product.name = request.form.get("name")
        product.price = float(request.form.get("price"))
        product.country = request.form.get("country")
        product.description = request.form.get("description")
        picture = request.files.get("picture")
        if picture:
            product.picture = picture.filename
            picture.save(f"static/uploads/{picture.filename}")
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", product=product)

if __name__ == "__main__":
    app.run(debug=True)
