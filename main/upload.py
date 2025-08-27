from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from main.models import Product
from main import db
import os

adm = Blueprint('adm', __name__)

UPLOAD_FOLDER = 'main/static/images'  # путь к папке для сохранения картинок
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@adm.route('/upload', methods=['GET', 'POST'])
@login_required
def admin1():
    email = current_user.email
    if email != 'srk@gmail.com':
        flash('You are not an admin!')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Получаем данные формы
        name = request.form.get('name')
        price_new = request.form.get('price_new')
        price_old = request.form.get('price_old')
        description = request.form.get('description')
        image_main = request.files.get('image_main')

        if not name or not price_new or not description or not image_main:
            flash('Please fill out all required fields!')
            return redirect(url_for('adm.admin1'))

        # Сохраняем изображение
        image_filename = image_main.filename
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        image_main.save(image_path)

        # Создаем новый продукт
        new_prod = Product(
            name=name,
            price_new=float(price_new),
            price_old=float(price_old) if price_old else None,
            description=description,
            img=image_filename
        )

        # Добавляем в базу
        db.session.add(new_prod)
        db.session.commit()
        flash('Product uploaded successfully!')

        return redirect(url_for('adm.admin1'))

    return render_template("upload.html", user=current_user)