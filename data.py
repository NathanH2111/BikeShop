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

def check_user(num):
    if not isinstance(num, int):
        return False
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT id FROM users")
    data = cur.fetchall()
    cur.close()
    con.close()
    print(data)
    for i in range(len(data)):
        if data[i][0] == num:
            return True
    return False

def check_admin(num):
    if not isinstance(num, int):
        return False
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT id,role FROM users")
    data = cur.fetchall()
    cur.close()
    con.close()
    print(data)
    for i in range(len(data)):
        
        if data[i][0] == num and data[i][1] == 'A':
            print(data[i][0],data[i][1])
            return True
    return False
