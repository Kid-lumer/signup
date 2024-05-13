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

@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        full_name = request.form["name"]
        email = request.form["email"]
        cell_no = request.form["CellNo."]
        password = request.form["password"]

        signup_details = {"full_name": full_name, "email": email, "Cell_No": cell_no, "password": password}

        db.signup.insert_one(signup_details)

        # Check if insertion was successful
        if signup_details:
            return render_template('login.html', success=True)
        else:
            return render_template('register.html', success=False)

    return render_template('register.html')

#Artist register
@app.route('/ArtistRegister', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        full_name = request.form["name"]
        email = request.form["email"]
        cell_no = request.form["CellNo."]
        password = request.form["password"]

        register_details = {"full_name": full_name, "email": email, "Cell_No": cell_no, "password": password}

        db.ArtistRegister.insert_one(register_details)

        # Check if insertion was successful
        if register_details:
            return render_template('ArtistRegister.html', success=True)
        else:
            return render_template('ArtistRegister.html', success=False)

    return render_template('ArtistRegister.html')


#Buyer Login
@app.route('/login_buyer', methods=["POST", "GET"])
def buyer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['signin_password']

        # Query the database for the user
        user = db.signup.find_one({'email': email, 'password': password })  # Exclude password from the result

        if ('form submission success'):
                    item = []
                    for i in db.Items.find():
                        item.append(i)
                    print(item)
                    return render_template("catalog.html", item = item)
        else:
            # Login failed, render login page with an error message
            error_message = "Invalid email or password. Please try again."
            return render_template("register.html", error_message=error_message)
   
    # GET request, render login page
    return render_template("login.html")

# Artist Login Page

@app.route('/login_artist', methods=["POST", "GET"])
def artist_login():
    if request.method == 'POST':
        email = request.form['email']
        signin_password = request.form['signin_password']

        # Query the database for the user
        profile = db.ArtistRegister.find_one({'email': email, 'password': signin_password})  # Exclude password from the result
    
        if profile:
            # Login successful, render profile page
            return render_template("profile.html", profile=profile)
            
        else:
            # Login failed, render login page with an error message
            error_message = "Invalid email or password. Please try again."
            return render_template("register.html", error_message=error_message)

    # GET request, render login page
    return render_template("profile.html")

    
    
    
    
    
    # try:
      
 
    #     if role == "buyer":
    #      item = []
    #      i =db.signup.find_one({'email':email, 'password':password})
    #      print(i)
    #      return render_template("catalog.html",item=i)
        
    #     if role =="seller":
    #      itemt = []
    #      for i in db.signup.find_one({'email':email, 'password':password}):
    #                     item.append(i)
    #      db.signup.find_one({'email':email, 'password':password, 'role':role})
     
    #      return render_template("profile.html", item = item)

    # except Exception as e:
    #  print("An error occurred:", e)



 #Add Item
@app.route('/AddItem')
def add_item():   
    return render_template("AddItem.html")

@app.route('/AddItem1', methods=["POST", "GET"])
def add_item1():
    if request.method == 'POST':
        Name = request.form['Name']
        email = request.form['email']
        Amount = request.form['Amount']
        Description = request.form['Description']
        image = request.form['image']
        
        item = {'Name': Name, 'email': email , 'Amount': Amount, 'Description': Description, 'image':image}

        db.Items.insert_one(item)
        if ('form submission success'):
                    print(request.form['Name'])
                    item = []
                    for i in db.Items.find():

                        item.append(i)
                    print(item)
                    return render_template("profile.html", item = item)
        else:

                  if ('form submission failed'):
                   return 'form unsuccessful'
     
        
    return ("Success")




# @app.route('/catelog', methods= ["GET"])
# def catalog():
#     # Retrieve data from MongoDB
#     Item = Mongo.db.Items.find()

#     # Render the catalog template with the data
#     return render_template("catelog.html", Item=Item)

# Display Catalog
@app.route("/getCatalog")
def getCatalog():
    item = []
    for i in db.Items.find():
        item.append(i)

    return render_template("catalog.html" , item = item)

#Display Profile
# @app.route("/profile", methods=["POST", "GET"] )
# def getProfile():
#      if request.method == 'GET':
#           artists = []

#           for i in db.ArtistRegister.find():
#                artists.append(i)

#      return render_template("profile.html", artist=artists)

# @app.route('/profile')
# def profile():   
#     return render_template("profile.html")

@app.route('/artist/<artist_id>')
def artist_profile(artist_id):
    # Logic to fetch artist details and their items and pass them to the template
    artist = artist(artist_id)
    items = items(artist_id)
    return render_template('artist_profile.html', artist=artist, items=items)


if __name__ == "__main__":
    app.run (debug=True)