from cryptography.fernet import Fernet
import psycopg2
import bcrypt
import random
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
    
def initialInsert():
    insertList  = ([(f"Slash 99XTR",f"mountain",f"{500.86}",f"Slash99XTR_22_35220_B_Primary.jpeg",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    (f"Checkpoint SLR7",f"street",f"{520.86}",f"CheckpointSLR7_22_35294_C_Primary.png",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    (f"Domane PlusLT7",f"street",f"{500.86}",f"DomanePlusLT7_22_35759_C_Primary.jpeg",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    (f"Domane SLR9",f"street",f"{500.86}",f"DomaneSLR9_22_35714_C_Primary.png",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    (f"Emonda SLR7Disc",f"street",f"{500.86}",f"EmondaSLR7DiscEtap_21_33139_B_Primary.jpg",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    (f"Madone SL7",f"street",f"{500.86}",f"MadoneSL7_22_35179_A_Primary.png",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    (f"Rail 98XT",f"mountain",f"{500.86}",f"Rail98XT_22_35672_C_Primary.jpeg",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    (f"Slash 99XTR",f"mountain",f"{500.86}",f"Slash99XTR_22_35220_B_Primary.png",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    (f"Speed ConceptSLR6e",f"street",f"{500.86}",f"SpeedConceptSLR6eTap_22_35754_A_Primary.jpg",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    (f"Speed ConceptSLR7",f"street",f"{500.86}",f"SpeedConceptSLR7_22_35577_D_Primary.jpeg",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    (f"Speed ConceptSLR7e",f"street",f"{500.86}",f"SpeedConceptSLR7eTap_22_35755_E_Primary.png",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    (f"Speed ConceptSLR9e",f"street",f"{500.86}",f"SpeedConceptSLR9eTap_22_35756_B_Primary.png",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    (f"Super Caliber",f"mountain",f"{500.86}",f"Supercaliber99XX1AXS_22_35145_C_Primary.png",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    (f"Top Fuel",f"mountain",f"{500.86}",f"TopFuel99XX1AXS_22_35326_B_Primary.png",f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")])
    con = connect()
    cur = con.cursor()
    # create all tables needed for the app to run and insert the initial Administrator account
    cur.execute('CREATE TABLE IF NOT EXISTS users (id BIGSERIAL PRIMARY KEY NOT NULL, email text UNIQUE NOT NULL,address BYTEA, password BYTEA,role VARCHAR(5))')
    con.commit()
    pw = 'abc123'
    pw = pw.encode('utf-8')
    cur.execute('INSERT INTO users (email, address, password, role) VALUES(%s,%s,%s,%s) ON CONFLICT DO NOTHING;',('gmdombach211@stevenscollege.edu','4 spite rode',bcrypt.hashpw(pw,bcrypt.gensalt(10)),'A'))
    cur.execute('INSERT INTO users (email, address, password, role) VALUES(%s,%s,%s,%s) ON CONFLICT DO NOTHING;',('nbhedemark211@stevenscollege.edu','4 spite rode',bcrypt.hashpw(pw,bcrypt.gensalt(10)),'A'))
    cur.execute('CREATE TABLE IF NOT EXISTS bikestock (name TEXT UNIQUE NOT NULL,type TEXT,price DOUBLE PRECISION,image text,description TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS bikesold (name TEXT,type TEXT,price DOUBLE PRECISION,image TEXT,description TEXT,color varchar(7),gears INT,rimsize INT,  customer BIGINT,FOREIGN KEY(customer) REFERENCES users(id))')
    cur.executemany('INSERT INTO bikestock (name,type,price,image,description) VALUES(%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING',insertList,)
    con.commit()
    cur.close() 
    con.close()