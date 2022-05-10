from flask import *
import os
import bcrypt
from app import app
import re
import data
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
global cusr 
cusr = ''
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 102
con = data.conect()
cur = con.cursor()
global tmpDta
tmpDta =[]

# create all tables needed for the app to run and insert the initial Administrator account
cur.execute('CREATE TABLE IF NOT EXISTS users (id BIGSERIAL PRIMARY KEY NOT NULL, email text UNIQUE NOT NULL,address BYTEA, password BYTEA,role VARCHAR(5))')
con.commit()
pw = 'abc123'
pw = pw.encode('utf-8')
cur.execute('INSERT INTO users (email, address, password, role) VALUES(%s,%s,%s,%s) ON CONFLICT DO NOTHING;',('gmdombach211@stevenscollege.edu','4 spite rode',bcrypt.hashpw(pw,bcrypt.gensalt(10)),'A'))
cur.execute('CREATE TABLE IF NOT EXISTS bikeStock (name TEXT UNIQUE NOT NULL,type TEXT,price DOUBLE PRECISION,image text,description TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS bikesold (name TEXT,type TEXT,price DOUBLE PRECISION,image TEXT,description TEXT,color varchar(7),gears INT,rimsize INT,  customer BIGINT,FOREIGN KEY(customer) REFERENCES users(id))')
con.commit()
cur.close() 
con.close()

#render Admin page and pass bike data to the page
@app.route('/administrator')
def admin():
   if not data.check_admin(cusr):return render_template('login.html',error='Please Log in To your Account')
   else:
      con = data.conect()
      cur = con.cursor()
      cur.execute('SELECT * FROM bikestock')
      dat = cur.fetchall()
      return render_template('admin.html',bikes = dat,idcode=cusr )

@app.route('/administrator',methods=['POST','GET'])
def addBikes():
   if not data.check_admin(cusr):return render_template('login.html',error='Please Log in To your Account')
   # Proccess input from the add bikes form
   if 'add' in request.form:
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
         con = data.conect()
         cur = con.cursor()
         cur.execute('INSERT INTO  bikestock (name,type,price,image,description) VALUES(%s,%s,%s,%s,%s)',(f'{name}',f'{type}',f'{price}',f'{filename}',f'{desc}'))
         con.commit()
         cur.close() 
         con.close()
         return redirect(url_for('admin'))

      else: 
         return redirect(url_for('admin'))

#proccess a bike deletion
   if 'delete' in request.form:
      con = data.conect() 
      cur = con.cursor()
      name = request.form.get('bikes')
      print(name)
      cur.execute('DELETE FROM bikestock WHERE name = %s;',(f"{name}",))
      con.commit()
      cur.close()
      con.close()
      return redirect(url_for('admin'))

   print('Error')
   return redirect(url_for('admin'))

@app.route("/")
def renderIndex():return render_template('index.html')

@app.route('/login/administrator') # login error for administrator registration
def adminLogin():return render_template('login.html',error = 'please enter admin credentials')

@app.route("/login/administrator",methods =['POST','GET']) #check if administrator auth to create a new admin is authentic
def mngrAuth():
   eml = request.form.get('nm')
   pwr = request.form.get('pw')
   pwr = pwr.encode('utf-8')

   con = data.conect()
   cur = con.cursor()
   cur.execute("SELECT email,role, password,id FROM users WHERE email = %s",(f"{eml}",)) #check if the admin email adress exists
   users = cur.fetchall()
   cur.close()
   con.close()

   if not users:return render_template('Login.html',error='Incorrect Username or Password') # return error if username is incorrect or does not exist.

   print(users)
   tmpPwr = bytes(users[0][2])
   print(tmpPwr)
   
   if bcrypt.checkpw(pwr,tmpPwr) and users[0][1] == 'A': # check if password is correct and that the user is an administrator
      con = data.conect()
      cur = con.cursor()
      cur.execute("INSERT INTO users (email,address,role,password) VALUES(%s,%s,%s,%s)",(tmpDta[0],tmpDta[1],'A',tmpDta[2]))#insert data to db for new user
      con.commit()
      cur.close()
      con.close()
      eml = ''
      pwr = ''
      
      return redirect(url_for('renderLogin')) # redirect to login page

   else:return redirect(url_for('renderRegister',error='Invalid code')) # return error if password is incorrect

@app.route("/login")
def renderLogin():return render_template('login.html',error = '') # render login template
   
@app.route('/login',methods = ['POST','GET'])
def loginFunc():
   eml = request.form.get('nm')
   pwr = request.form.get('pw')
   pwr = pwr.encode('utf-8')

   con = data.conect()
   cur = con.cursor()
   cur.execute("SELECT email,role, password,id FROM users WHERE email = %s",(f"{eml}",))# check for user in db
   users = cur.fetchall()
   cur.close()
   con.close()
   if not users:return render_template('Login.html',error='Incorrect Username or Password') # return error if username incorrect or desnt exist

   print(users)
   tmpPwr = bytes(users[0][2])# convert pw to bytes
   print(tmpPwr)
   if bcrypt.checkpw(pwr,tmpPwr):
      global cusr
      cusr = int(users[0][3])# save user code for later use
      if users[0][1] == 'A':return redirect(url_for('admin'))#if user is an admin redirect to admin page

      if users[0][1] == 'U':return redirect(url_for('renderShop',idcode = cusr))#if user is a regular user redirect to the shop
      return render_template('Login.html',error=' oops! An error occured please try to log in again in a few minutes')
   else:return render_template('Login.html',error='Incorrect Username or Password')# errors


@app.route("/register")
def renderRegister():return render_template('register.html',error = '')

@app.route('/register',methods=['POST','GET'])
def register_register():
   if request.method == 'POST':
      eml = request.form.get('eml')
      adr = request.form.get('adr')
      pwr = request.form.get('pwd')
      mgr = request.form.get('mngr')
      con = data.conect()
      cur = con.cursor()
      cur.execute('SELECT email from users WHERE email = %s',(f"{eml}",))
      check = cur.fetchall()

      print(check)

      if pwr == None:return render_template('Register.html',error=' please input a password')

      if not check:
         if  re.match('/^(?=.*\d).{8,}$/',pwr):return render_template('Register.html',error = ' password not strong enough')
         if mgr == '1':# if the manager checkbox is checked store the registration data in a list and redirect to the admin login page for manager authorization
            global tmpDta
            tmpDta = [eml,data.encrypt_text(adr),bcrypt.hashpw(pwr.encode('utf-8'),bcrypt.gensalt(10))]
            return redirect(url_for('adminLogin'))

         newpass = bcrypt.hashpw(pwr.encode('utf-8'),bcrypt.gensalt(10))#hash and salt the password
         cur.execute("INSERT INTO users (email,address,role,password) VALUES(%s,%s,%s,%s)",(f"{eml}",data.encrypt_text(adr),f"U",newpass))# insert the new user into the database
         con.commit()
         cur.close()
         con.close()
         return redirect(url_for('renderLogin'))

      else:return render_template('register.html',error ='User already Exists')

@app.route("/shop")
def renderShop():
   # if cusr == '':return render_template('login.html',error='Please Log in To your Account')
   return render_template('shop.html') # render the shop template
@app.route("/logout")
def renderLogout():
   global cusr
   cusr = ''
   return render_template('login.html')
@app.route("/logout")
def logOut():
   global cusr
   cusr = ''
   print(cusr)
   return redirect(url_for('renderLogin'))

@app.route("/custom")
def renderCustom():
   return render_template('custom.html')

@app.route("/custom", methods=["GET", "POST"])
def purchaseBike():
   if request.method == "POST":
      bike_style = request.form.get("type")
      gears = request.form.get("gears")
      tire_size = request.form.get("tire-size")
      color = request.form.get("bike-color")
      ccn = request.form.get("ccn")
      cvv = request.form.get("cvv")

      print(bike_style, gears, tire_size, color, ccn, cvv)
      
      return redirect(url_for('renderIndex'))

   # con = data.conect()
   # cur = con.cursor()
   # cur.execute("INSERT INTO bikessold (name,type,price,image,description,color,gears,rimsize,customer) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", ())

if __name__ == '__main__':app.run(debug=True)