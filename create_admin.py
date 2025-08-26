from main import db, create_app
from main.models import User
from werkzeug.security import generate_password_hash

# Создаем приложение и активируем контекст
app = create_app()
with app.app_context():
    # Настройки нового админа
    email = "admin@example.com"
    password = "admin123"  # потом поменяешь
    role = "admin"

    # Проверка — есть ли уже админ с таким email
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        print(f"❌ Пользователь с email {email} уже существует.")
    else:
        hashed_password = generate_password_hash(password)
        new_admin = User(email=email, password=hashed_password, role=role)
        db.session.add(new_admin)
        db.session.commit()
        print(f"✅ Админ создан! Email: {email} | Пароль: {password}")