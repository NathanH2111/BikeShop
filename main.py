from flask import *

app = Flask(__name__)

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