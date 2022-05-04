from flask import *
import os
import bcrypt
from app import app
import urllib.request

import re
import data
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 102
con = data.connect()
cur = con.cursor()
global tempData
tempData =[]
cur.execute('CREATE TABLE IF NOT EXISTS users (id BIGSERIAL PRIMARY KEY NOT NULL, email text UNIQUE NOT NULL,address BYTEA, password BYTEA,role VARCHAR(5))')
con.commit()
pw = 'abc123'
pw = pw.encode('utf-8')
cur.execute('INSERT INTO users (email, address, password, role) VALUES(%s,%s,%s,%s) ON CONFLICT DO NOTHING;',('gmdombach211@stevenscollege.edu','4 spite rode',bcrypt.hashpw(pw,bcrypt.gensalt(10)),'A'))
cur.execute('CREATE TABLE IF NOT EXISTS bikeStock (name TEXT,type TEXT,price DOUBLE PRECISION,image text,description TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS bikesold (name TEXT,type TEXT,price DOUBLE PRECISION,image TEXT,description TEXT,customer BIGINT,FOREIGN KEY(customer) REFERENCES users(id))')
con.commit()
cur.close() 
con.close()

@app.route('/administrator')
def admin():
   con = data.connect()
   cur = con.cursor()
   cur.execute('SELECT * FROM bikestock')
   dat = cur.fetchall()
   return render_template('admin.html',bikes = dat )

@app.route('/administrator',methods=['POST','GET'])
def addbikes():
   name = request.form.get('name')
   type = request.form.get('type')
   desc = request.form.get('description')
   price = float(request.form.get('price'))
   if 'file' not in request.files:
      return render_template('admin.html')
   file = request.files['file']
   if file.filename == '':
      return render_template('admin.html')
   if file and allowed_file(file.filename):
      print(file.filename)
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
      print('upload_image filename: ' + filename)
      con = data.connect()
      cur = con.cursor()
      cur.execute('INSERT INTO  bikestock (name,type,price,image,description) VALUES(%s,%s,%s,%s,%s)',(f'{name}',f'{type}',f'{price}',f'{filename}',f'{desc}'))
      con.commit()
      cur.close() 
      con.close()
      return redirect(url_for('admin'))
   else: 
      return redirect(url_for('admin'))


@app.route("/")
def renderIndex():return render_template('index.html')

@app.route('/login/administrator')
def adminLogin():return render_template('login.html',error = 'please enter admin credentials')

@app.route("/login/administrator",methods =['POST','GET'])
def mngrAuth():
   userName = request.form.get('nm')
   password = request.form.get('pw')
   password = password.encode('utf-8')

   conn = data.connect()
   curr = conn.cursor()
   curr.execute("SELECT email,role, password,id FROM users WHERE email = %s",(f"{userName}",))
   users = curr.fetchall()
   curr.close()
   conn.close()

   if not users:return render_template('Login.html',error='Incorrect Username or Password')

   print(users)
   tempPass = bytes(users[0][2])
   print(tempPass)
   
   if bcrypt.checkpw(password,tempPass) and users[0][1] == 'A':
      con = data.connect()
      curr = con.cursor()
      curr.execute("INSERT INTO users (email,address,role,password) VALUES(%s,%s,%s,%s)",(tempData[0],tempData[1],'A',tempData[2]))
      con.commit()
      curr.close()
      con.close()
      userName = ''
      password = ''
      
      return redirect(url_for('renderLogin'))

   else:return redirect(url_for('renderRegister',error='Invalid code'))

@app.route("/login")
def renderLogin():return render_template('login.html',error = '')
   
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
   if not users:return render_template('Login.html',error='Incorrect Username or Password')

   print(users)
   tempPass = bytes(users[0][2])
   print(tempPass)
   if bcrypt.checkpw(password,tempPass):
      if users[0][1] == 'A':return redirect(url_for('admin'))

      if users[0][1] == 'U':return redirect(url_for('renderShop',idcode = users[0][3]))
      return render_template('Login.html',error=' oops! An error occured please try to log in again in a few minutes')
   else:return render_template('Login.html',error='Incorrect Username or Password')


@app.route("/register")
def renderRegister():return render_template('register.html',error = '')

@app.route('/register',methods=['POST','GET'])
def register_register():
   if request.method == 'POST':
      userName = request.form.get('eml')
      userAddress = request.form.get('adr')
      password = request.form.get('pwd')
      mgr = request.form.get('mngr')
      conn = data.connect()
      curr = conn.cursor()
      curr.execute('SELECT email from users WHERE email = %s',(f"{userName}",))
      check = curr.fetchall()

      print(check)

      if password == None:return render_template('Register.html',error=' please input a password')

      if not check:
         if re.match('(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$',password):return render_template('register.html',error='Passwords must contaion one uppercase one lowercase one number and one symbol \n passwords must be at least 8 characters long')
         if mgr == '1':
            global tempData
            tempData = [userName,data.encrypt_text(userAddress),bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt(10))]
            return redirect(url_for('adminLogin'))

         newpass = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt(10))
         curr.execute("INSERT INTO users (email,address,role,password) VALUES(%s,%s,%s,%s)",(f"{userName}",data.encrypt_text(userAddress),f"U",newpass))
         conn.commit()
         cur.close()
         conn.close()
         return redirect(url_for('renderLogin'))

      else:return render_template('register.html',error ='User already Exists')

@app.route("/shop")
def renderShop():
   return render_template('shop.html')

if __name__ == '__main__':app.run(debug=True)