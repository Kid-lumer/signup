from flask import Flask, render_template, request, url_for, redirect,Response, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__ ,static_url_path=('/static'))
app.secret_key = 'super_secret_key'
app.config["MONGO_URI"] = "mongodb://localhost:27017/SoloProject"
Mongo = PyMongo(app)
db = Mongo.db
collection = db['Items']

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
        role = request.form['role']
        signup_details = {"full_name": full_name, "email": email, "Cell_No": cell_no, "password": password, 'role':role}

        db.signup.insert_one(signup_details)

        # Check if insertion was successful
        if signup_details:
            return render_template('register.html', success=True)
        else:
            return render_template('register.html', success=False)

    return render_template('register.html')

#Artist register
# @app.route('/ArtistRegister', methods=["POST", "GET"])
# def register():
#     if request.method == "POST":
#         full_name = request.form["name"]
#         email = request.form["email"]
#         cell_no = request.form["CellNo."]
#         password = request.form["password"]
#         role = request.form['role']
#         register_details = {"full_name": full_name, "email": email, "Cell_No": cell_no, "password": password, 'role':role}

#         db.ArtistRegister.insert_one(register_details)

#         # Check if insertion was successful
#         if register_details:
#             return render_template('ArtistRegister.html', success=True)
#         else:
#             return render_template('ArtistRegister.html', success=False)

#     return render_template('ArtistRegister.html')


#Buyer Login
@app.route('/login_buyer', methods=["POST", "GET"])
def buyer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['signin_password']
        role = request.form['role']
        # Query the database for the user
        user = db.signup.find_one({'email': email, 'password': password })  # Exclude password from the result
        if user:
            if role == 'artist':
                item = db.Items.find({'email': email})  # Exclude password from the result
                return render_template("profile.html", item = item)
            else:
                item = db.Items.find()  # Exclude password from the result
                return render_template("catalog.html", item = item)
            
        
    # GET request, render login page
    return render_template("login.html")




 #Add Item
@app.route('/AddItem', methods=["POST"])
def add_item():   
    if request.method == 'POST':
        return render_template("AddItem.html")
    return render_template("AddItem.html")

@app.route('/profile', methods=["GET"])
def getItems(): 
    items = db.Items.find  # Retrieve all items from the database
    return render_template("profile.html" , item =items)

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
                    # print(request.form['Name'])
                    item = db.Items.find()  # Exclude password from the result
                    # return redirect(url_for('getItems', item = item))
                    return render_template("profile.html", item = item)
        
        else:

                  if ('form submission failed'):
                   return 'form unsuccessful'
     
         
    return ("Success")



# Display Catalog
@app.route("/getCatalog")
def getCatalog():
    item = []
    for i in db.Items.find():
        item.append(i)
    print(item)
    return render_template("catalog.html" , item = item)

@app.route('/delete_item', methods=["POST"])
def delete_product():
    # Delete the product from MongoDB

    if request.method == 'POST':
        delete_id = request.form['delete_id']
        print(delete_id)

    db.Items.delete_one({"_id": ObjectId(delete_id)})

    # Redirect back to the catalog page
    item = []
    for i in db.Items.find():
        item.append(i)
        print(item)
    return render_template("profile.html", item = item)

#View item
# from flask import Blueprint, render_template, request, redirect, url_for, flash
@app.route('/viewproduct', methods=['GET', 'POST'])
def view():
    
    if request.method == 'POST':
       
        id = request.form['id']
        Name = request.form['Name']
        Amount = request.form['Amount']
        Description = request.form['Description']
        image = request.form['image']
    
        return render_template('ViewItem.html', id=id, Name=Name, Description=Description, Amount=Amount, image=image)


@app.route('/AddToCart', methods=['POST'])
def add_to_cart():
    # Get item details from the form submission
    id = request.form.get('id')
    Name = request.form.get('Name')
    Amount = request.form.get('Amount')

    # Create item dictionary
    item = {'id': id, 'Name': Name, 'Amount': Amount}

    # Retrieve the cart items from the session
    cart_items = session.get('cart', [])

    # Add the item to the cart
    cart_items.append(item)

    # Update the cart items in the session
    session['cart'] = cart_items

    # Redirect to the view cart page
    return redirect(url_for('cart'))

@app.route('/ViewCart')
def cart():
    # Retrieve the cart items from the session
    cart_items = session.get('cart', [])

    # Pass the cart items to the cart.html template
    return render_template('ViewCart.html', item=cart_items)

@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    selected_items = request.form.getlist('selected_items')

    # Retrieve the cart items from the session
    cart_items = session.get('cart', [])

    # Remove the selected items from the cart
    cart_items = [item for item in cart_items if item.id not in selected_items]

    # Update the cart items in the session
    session['cart'] = cart_items

    return redirect('/cart')

@app.route('/cart/checkout', methods=['POST'])
def checkout():
    # Retrieve the cart items from the session
    cart_items = session.get('cart', [])

    # Perform the necessary operations for checkout, such as processing payment, updating inventory, etc.

    # Clear the cart after successful checkout
    session.pop('cart', None)

    return redirect('/checkout_success')


@app.route('/Edit', methods=['POST'])
def edit_item():
    if request.method == 'POST':
        update_id = request.form['update_id']
        email = request.form['email']
        item_id = ObjectId(update_id)
    
    # Retrieve the item from MongoDB collection
        
        return render_template("edit.html", item_id = item_id, email=email)

@app.route('/Edit2', methods=['POST'])
def edit_item2():
    if request.method == 'POST':
        update_id = request.form['update_id']
        email = request.form['email']
        name = request.form['Name']
        Amount = request.form['Amount']
        description = request.form['Description']
        image = request.form['image']
        item_id = ObjectId(update_id)
    
    # Retrieve the item from MongoDB collection
        item = db.Items.update_one({'_id': item_id}, {'$set': {'Name':name, 'email':email, 'Description':description, 'Amount' :Amount, 'image':image  }})
    
        item = db.Items.find({'email': email})  # Exclude password from the result
        # return redirect(url_for('getItems', item = item))
        return render_template("profile.html", item = item)

if __name__ == "__main__":
    app.run (debug=True)
















































# @app.route('/AddItem1', methods=["POST", "GET"])
# def add_item1():
#     if request.method == 'POST':
#         Name = request.form['Name']
#         email = request.form['email']
#         Amount = request.form['Amount']
#         Description = request.form['Description']
#         image = request.form['image']
        
#         item = {'Name': Name, 'email': email , 'Amount': Amount, 'Description': Description, 'image':image}
        
#         db.Items.insert_one(item)
        
   
        
#         return redirect(url_for('getCatalog', item = item))
#         # return render_template("catalog.html", item = item)

#     return "Success"

# @app.route('/profile', methods=["GET"])
# def getItems(): 
#     if 'email' in session:  # Check if user is logged in
#         email = session['email']
#         # Retrieve items associated with the user's email
#         item = list(db.Items.find({'email': email}))
#         return render_template("profile.html" , items=item)
#     else:
#         return "Please login to view your profile"  



#Display Profile
# @app.route("/profile", methods=["POST", "GET"] )
# def getProfile():
#      if request.method == 'GET':
#           item = []

#           for i in db.Items.find():
#                item.append(i)

#      return render_template("profile.html", item=item)

# @app.route('/profile')
# def profile():   
#     return render_template("profile.html",)
