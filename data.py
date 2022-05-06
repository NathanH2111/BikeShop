from cryptography.fernet import Fernet
import psycopg2
def connect(): return psycopg2.connect(
    database = 'flask_db',
    user = 'postgres',
    password = 'gabe1972',
    host = 'localhost'
)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_text(text):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(bytes(text, "utf-8"))

def decrypt_text(encrypted_text):
    key = load_key()
    f = Fernet(key)
    decoded = f.decrypt(encrypted_text)
    return decoded.decode("utf-8")

print(encrypt_text('3 appple lane'))