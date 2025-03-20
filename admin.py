from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user
from extensions import db
from models import Product, User

# Главная страница админки
class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for("login"))
        return super().index()

# Ограничение доступа к админке
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

# Админка пользователей
class UserAdmin(AdminModelView):
    column_list = ("username", "is_admin")
    column_labels = {"username": "Логин", "is_admin": "Администратор"}
    form_excluded_columns = ("password",)

# Админка товаров
class ProductAdmin(AdminModelView):
    column_list = ("name", "price", "country", "description", "picture")
    column_labels = {"name": "Название", "price": "Цена", "country": "Страна", "description": "Описание", "picture": "Изображение"}
    form_columns = ["name", "price", "country", "description", "picture"]

# Создание объекта админки
admin = Admin(
    name="Панель администратора",
    template_mode="bootstrap4",
    index_view=MyAdminIndexView(),
)

# Добавление ссылок и моделей в админку
admin.add_link(MenuLink(name="🏠 На главную", url="/"))
admin.add_view(ProductAdmin(Product, db.session))
admin.add_view(UserAdmin(User, db.session))
