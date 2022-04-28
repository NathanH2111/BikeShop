from flask import *
import bcrypt
import data 

app = Flask(__name__)
con = data.connect()
cur = con.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS users (id BIGSERIAL PRIMARY KEY NOT NULL, email text NOT NULL, password BYTEA,role VARCHAR(5))')
con.commit()
cur.execute('CREATE TABLE IF NOT EXISTS bikeStock (name TEXT,type TEXT,price DOUBLE PRECISION,image text,description TEXT')
cur.execute('CREATE TABLE IF NOT EXISTS bikesold (name TEXT,type TEXT,price DOUBLE PRECISION,image TEXT,description TEXT,customer BIGINT,FOREIGN KEY(customer) REFERENCES users(id))')
con.commit()
cur.close() 
con.close()

@app.route("/")
def renderIndex():
   return render_template('index.html')

@app.route("/login")
def renderLogin():
   return render_template('login.html')

@app.route("/register")
def renderRegister():
   return render_template('register.html')

@app.route("/shop")
def renderShop():
   return render_template('shop.html')

if __name__ == '__main__':
   app.run(debug=True)