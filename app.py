from flask import Flask, render_template, request, url_for, redirect,Response, url_for
from flask_pymongo import PyMongo
from bson.objectid import *




app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/SoloProject"
Mongo = PyMongo(app)
db = Mongo.db

# landing page
@app.route('/')
def landing():
        return render_template("index.html")


# Signup page

@app.route('/signup', methods=["POST","GET"])
def signup():
  if request.method =="POST":
     
     full_name = request.form["name"]
     email = request.form["email"]
     Cell_No = request.form["CellNo."]
     password = request.form["password"]
     Confirm_Pasword = request.form["confirmpassword"]
     
    #  confirming password§
   
     if password != Confirm_Pasword:
      return "passwords do not match"


     signupdetails = {"full_name":full_name, "email":email, "Cell_No":Cell_No, "password":password}

     db.signup.insert_one(signupdetails)
     
     if ('form submission success'):
                     return redirect (url_for('login'))
     else:

                if ('form submission failed'):
                   return 'form unsuccessful'
                
  return render_template('register.html')


#Login Page

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        
        logindetails = {'name': name, 'password':password}
        

    try:
     
        user = db.signup.find_one(logindetails)

        if user is None:
         return redirect(url_for('signup'))
        else:
         return redirect(url_for('index'))
    except Exception as e:
     print("An error occurred:", e)


    return render_template('login.html')


if __name__ == "__main__":
    app.run (debug=True)