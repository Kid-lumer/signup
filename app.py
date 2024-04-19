from flask import Flask, render_template, request, url_for, redirect,Response, url_for
from flask_pymongo import PyMongo
from bson.objectid import *




app = Flask(__name__ ,static_url_path=('/static'))
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
     role = request.form["role"]
     
     
   
     signupdetails = {"full_name":full_name, "email":email, "Cell_No":Cell_No, "password":password, "role":role}

     db.signup.insert_one(signupdetails)
     
     if ('form submission success'):
                     return render_template('register.html')
     else:

                if ('form submission failed'):
                   return 'form unsuccessful'
                
  return render_template('register.html')

#Artist Register

@app.route('/ArtistRegister', methods=["POST","GET"])
def register():
  if request.method =="POST":
     
     full_name = request.form["name"]
     email = request.form["email"]
     Cell_No = request.form["CellNo."]
     Password = request.form["Password"]
     Confirm_Pasword = request.form["confirmpassword"]
     category = request.form["category"]
    
    
    #  confirming password§
   
     if Password != Confirm_Pasword:
      return "passwords do not match"


     signupdetails = {"full_name":full_name, "email":email, "Cell_No":Cell_No, "Password":Password, "Confirm_Pasword":Confirm_Pasword, "category":category}

     db.signup.insert_one(signupdetails)
     
     if ('form submission success'):
                     return redirect (url_for('login'))
     else:

                if ('form submission failed'):
                   return 'form unsuccessful'
                
  return render_template('ArtistRegister.html')

# Login Page

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['signin-password']
        role = request.form['role']
        

    try:

        if role == "buyer":
         db.signup.find_one({'email': email, 'password':password, 'role': role})
         return render_template("catalog.html")
    
        if role =="seller":
         db.signup.find_one({'email':email, 'password':password, 'role':role})
     
         return render_template("profile.html")

    except Exception as e:
     print("An error occurred:", e)



 #Add Item
@app.route('/AddItem', methods=["POST", "GET"])
def add_item():
    if request.method == 'POST':
        Name = request.form['Name']
        Amount = request.form['price']
        Description = request.form['Description']
        image = request.form['image']
        
        item = {'Name': Name, 'Amount': Amount, 'Description': Description, 'image':image}

        db.Items.insert_one(item)
        if ('form submission success'):
                     item = []
                     return render_template("catalog.html")
        else:

                  if ('form submission failed'):
                   return 'form unsuccessful'
        
    return render_template("AddItem.html")

# Display Catalog
@app.route("/catalog", methods=["POST", "GET"] )
def getCatalog():
     if request.method == 'GET':
          item = []

          for i in db.Items.find():
               item.append(i)

     return render_template("catalog.html" , x=item)

# Display Profile
@app.route("/profile", methods=["POST", "GET"] )
def getProfile():
     if request.method == 'GET':
          artists = []

          for i in db.ArtistRegister.find():
               artists.append(i)

     return render_template("profile.html")



if __name__ == "__main__":
    app.run (debug=True)