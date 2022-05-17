from flask import *
import os
import bcrypt
import re
import data
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','jfif','pjpeg','pjp','svg','webp','apng'])
global cusr 
cusr = ''
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 102
con = data.connect()
cur = con.cursor()
global tmpDta
tmpDta =[]

data.initialInsert() #Initialize DB tables if not exists

@app.route("/login")
def renderLogin():return render_template('login.html',error = '') # render login template
@app.route('/login',methods = ['POST','GET'])
def loginFunc():
   eml = request.form.get('nm')
   pwr = request.form.get('pw')
   pwr = pwr.encode('utf-8')

   con = data.connect()
   cur = con.cursor()
   cur.execute("SELECT email,role, password,id FROM users WHERE email = %s",(f"{eml}",))# check for user in db
   users = cur.fetchall()
   cur.close()
   con.close()
   if not users:return render_template('Login.html',error='Incorrect Username or Password') # return error if username incorrect or desnt exist

   print(users)
   tmpPwr = bytes(users[0][2])# convert pw to bytes
   print(tmpPwr)
   print(bcrypt.checkpw(pwr,tmpPwr))
   if bcrypt.checkpw(pwr,tmpPwr):
      global cusr
      cusr = int(users[0][3])# save user code for later use
      if users[0][1] == 'A':return redirect(url_for('admin'))#if user is an admin redirect to admin page

      if users[0][1] == 'U':return redirect(url_for('renderShop',idcode = cusr))#if user is a regular user redirect to the shop
      return render_template('Login.html',error=' oops! An error occured please try to log in again in a few minutes')
   else:return render_template('Login.html',error='Incorrect Username or Password')# errors

@app.route("/shop")
def renderShop():
   conn = data.connect()
   cur = conn.cursor()
   cur.execute("SELECT * FROM bikestock")
   bikes = cur.fetchall()
   if data.check_user(cusr) and not data.check_admin(cusr):
      return render_template('shop.html',admin='none',logout = 'inline',bikestock = bikes)
   elif data.check_admin(cusr):
      return render_template('shop.html',admin='inline',logout='inline',bikestock = bikes)
   else:
      return render_template('shop.html',admin='none',logout = 'none',bikestock = bikes)

   # if not data.check_user(cusr):return render_template('shop.html',bikestock = bikes,logout = 'hidden',admin='hidden')
   # elif data.check_admin(cusr):return render_template('shop.html',bikestock = bikes,logout = 'hidden',admin='visible')
   # return render_template('shop.html', bikestock = bikes,logout = 'visible',admin='hidden') # render the shop template

@app.route("/shop", methods = ["GET", "POST"])
def buyBike():
   if request.method == "POST":
      selected_bike = request.form.get("submitBtn")
      print(selected_bike)
      conn = data.connect()
      cur = conn.cursor()
      cur.execute("SELECT * FROM bikestock WHERE name = %s", (f"{selected_bike}",))
      bike_data = cur.fetchall()
      global bike_name, bike_price, bike_desc, bike_img
      bike_img = bike_data[0][3]
      bike_name = bike_data[0][0]
      bike_price = bike_data[0][2]
      bike_desc = bike_data[0][4]
      return redirect(url_for("renderCustom"))

@app.route("/custom")
def renderCustom():
   if not data.check_user(cusr): return render_template('login.html',error='Please log in before purchasing a bike')
   return render_template('custom.html')

@app.route("/custom", methods=["GET", "POST"])
def purchaseBike():
   if request.method == "POST":
      bike_style = request.form.get("type")
      gears = request.form.get("gears")
      tire_size = float(request.form.get("tire-size"))
      color = request.form.get("bike-color")
      ccn = request.form.get("ccn")
      cvv = request.form.get("cvv")
      print(bike_style, gears, tire_size, color)

      con = data.connect()
      cur = con.cursor()
      cur.execute("INSERT INTO bikesold (name,type,price,image,description,color,gears,rimsize,customer) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (bike_name, bike_style, bike_price, bike_img, bike_desc, color, gears, tire_size, cusr))
      con.commit()
      cur.close()
      con.close()
      return redirect(url_for('renderIndex'))

@app.route("/users")
def renderUsers():
   if not data.check_user(cusr):return render_template('login.html',error='Please log in to continue to Your Bikes')
   con = data.connect()
   cur = con.cursor()
   cur.execute("SELECT * FROM bikesold WHERE customer = %s",(cusr,))
   dat = cur.fetchall()
   if data.check_user(cusr) and not data.check_admin(cusr):
      return render_template('user.html', bikes=dat ,admin='none',logout = 'inline')
   elif data.check_admin(cusr):
      return render_template('user.html', bikes=dat, admin='inline',logout='inline')
   else: return render_template('user.html', bikes=dat, admin = "none", logout = "none")

#render Admin page and pass bike data to the page
@app.route('/administrator')
def admin():
   con = data.connect()
   cur = con.cursor()
   cur.execute('SELECT * FROM bikestock')
   dat = cur.fetchall()
   cur.close()
   con.close()
   if data.check_user(cusr) and not data.check_admin(cusr):
      return render_template('admin.html', bikes = dat, idcode = cusr, admin='none', logout = 'inline')
   elif data.check_admin(cusr):
      return render_template('admin.html', bikes = dat, idcode = cusr, admin='inline', logout='inline')
   else: return render_template('admin.html',bikes = dat, idcode=cusr, error = '', admin = "none", logout = "none")

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
         con = data.connect()
         cur = con.cursor()
         cur.execute('SELECT * FROM bikestock')
         dat = cur.fetchall()
         cur.close()
         con.close()
         return render_template('admin.html',bikes=dat,error='No filename',idcode =cusr)
      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
         con = data.connect()
         cur = con.cursor()
         cur.execute('INSERT INTO  bikestock (name,type,price,image,description) VALUES(%s,%s,%s,%s,%s)',(f'{name}',f'{type}',f'{price}',f'{filename}',f'{desc}'))
         con.commit()
         cur.execute('SELECT * FROM bikestock')
         dat = cur.fetchall()
         cur.close()
         con.close()
         return render_template('admin.html',bikes=dat,error='Upload Sucessfull',idcode =cusr)

      else: 
         con = data.connect()
         cur = con.cursor()
         cur.execute('SELECT * FROM bikestock')
         dat = cur.fetchall()
         cur.close()
         con.close()
         return render_template('admin.html',bikes=dat,error='Error Invalid file type',idcode =cusr)

#proccess a bike deletion
   if 'delete' in request.form:
      con = data.connect()
      cur = con.cursor()
      name = request.form.get('bikes')
      cur.execute('DELETE FROM bikestock WHERE name = %s;',(f"{name}",))
      con.commit()
      cur.close()
      con.close()
      return redirect(url_for('admin'))

   return redirect(url_for('admin'))

@app.route("/")
def renderIndex():
   if data.check_user(cusr) and not data.check_admin(cusr):
      return render_template('index.html', admin='none',logout = 'inline')
   elif data.check_admin(cusr):
      return render_template('index.html', admin='inline',logout='inline')
   else:
      return render_template('index.html', admin='none',logout = 'none')

@app.route("/register")
def renderRegister():return render_template('register.html',error = '')

@app.route('/register',methods=['POST','GET'])
def register_register():
   if request.method == 'POST':
      eml = request.form.get('eml')
      adr = request.form.get('adr')
      pwr = request.form.get('pwd')
      mgr = request.form.get('mngr')
      con = data.connect()
      cur = con.cursor()
      cur.execute('SELECT email from users WHERE email = %s',(f"{eml}",))
      check = cur.fetchall()


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

@app.route("/logout")#clear the cusr variable and redirect to the login page
def renderLogout():
   global cusr
   cusr = ''
   return render_template('login.html')

@app.route("/logout")
def logOut():
   global cusr
   cusr = ''
   return redirect(url_for('renderLogin'))

if __name__ == '__main__':app.run(debug=True)