from werkzeug.security import generate_password_hash

# Введи свой пароль сюда
new_password = "123456"
hashed = generate_password_hash(new_password, method="sha256")
print("Новый хэш:", hashed)