from flask import *
import bcrypt
import data 

app = Flask(__name__)
con = data.connect()
cur = con.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS users (id BIGSERIAL PRIMARY KEY NOT NULL, email text NOT NULL, password BYTEA,role VARCHAR(5))')
con.commit()
cur.execute('CREATE TABLE IF NOT EXISTS bikeStock (name TEXT,type TEXT,price DOUBLE PRECISION,image text,description TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS bikesold (name TEXT,type TEXT,price DOUBLE PRECISION,image TEXT,description TEXT,customer BIGINT,FOREIGN KEY(customer) REFERENCES users(id))')
con.commit()
cur.close() 
con.close()

@app.route("/")
def renderIndex():
   return render_template('index.html')

@app.route("/login")
def renderLogin():
   return render_template('login.html',error = '')

@app.route('/login',methods = ['POST','GET'])
def loginFunc():
   userName = request.form.get('nm')
   password = request.form.get('pw')
   password = password.encode('utf-8')

   conn = data.connect()
   curr = conn.cursor()
   curr.execute("SELECT email,role, password,id FROM users WHERE email = %s",(f"{userName}",))
   users = curr.fetchall()
   curr.close()
   conn.close()
   if not users:
      return render_template('Login.html',error='Incorrect Username or Password')
   print(users)
   tempPass = bytes(users[0][2])
   print(tempPass)
   if bcrypt.checkpw(password,tempPass):
      if users[0][1] == 'A':
         return redirect(url_for('admin'))
      if users[0][1] == 'U':
         return redirect(url_for('renderShop',idcode = users[0][3]))
      return render_template('Login.html',error=' oops! An error occured please try to log in again in a few minutes')
   else:
      return render_template('Login.html',error='Incorrect Username or Password')


@app.route("/register")
def renderRegister():
   return render_template('register.html')

@app.route('/register',methods=['POST','GET'])
def register_register():
    if request.method == 'POST':
        userName = request.form.get('eml')
        userAddress = request.form.get('adr')
        password = request.form.get('pwd')
        conn = data.connect()
        curr = conn.cursor()
        curr.execute('SELECT email from users WHERE email = %s',(f"{userName}",))
        check = curr.fetchall()

        print(check)

        if password == None:return render_template('Register.html',error=' please input a password')

        if not check:
            newpass = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt(10))
            curr.execute("INSERT INTO users (name,email,phone,userrank,password) VALUES(%s,%s,%s)",(f"{userName}",f"{userAddress}",f"U",newpass))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('login'))

        else:
            return render_template('register.html',error ='User already Exists')

@app.route("/shop")
def renderShop():
   return render_template('shop.html')

@app.route("/admin")
def renderAdmin():
   return render_template('admin.html')

if __name__ == '__main__':
   app.run(debug=True)