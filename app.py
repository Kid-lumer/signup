from flask import Flask, render_template, request, url_for, redirect, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__, static_url_path=('/static'))
app.secret_key = 'super_secret_key'
app.config["MONGO_URI"] = "mongodb://localhost:27017/SoloProject"
Mongo = PyMongo(app)
db = Mongo.db

# landing page
@app.route('/')
def landing():
    cart_count = len(session.get('cart', []))
    return render_template("index.html", cart_count=cart_count)

# Signup page
@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        full_name = request.form["name"]
        email = request.form["email"]
        cell_no = request.form["CellNo."]
        password = request.form["password"]
        role = request.form['role']
        signup_details = {"full_name": full_name, "email": email, "Cell_No": cell_no, "password": password, 'role': role}

        db.signup.insert_one(signup_details)
        if signup_details:
            return render_template('register.html', success=True)
        else:
            return render_template('register.html', success=False)
    return render_template('register.html')

# Buyer Login
@app.route('/login_buyer', methods=["POST", "GET"])
def buyer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['signin_password']
        role = request.form['role']
        user = db.signup.find_one({'email': email, 'password': password})
        if user:
            session['user_id'] = str(user['_id'])
            session['role'] = role
            cart_count = len(session.get('cart', []))
            if role == 'artist':
                items = db.Items.find({'email': email})
                return render_template("profile.html", item=items, cart_count=cart_count)
            else:
                items = db.Items.find()
                return render_template("catalog.html", item=items, cart_count=cart_count)
    return render_template("login.html")

# Add Item
@app.route('/AddItem', methods=["POST"])
def add_item():
    if request.method == 'POST':
        return render_template("AddItem.html")
    return render_template("AddItem.html")

@app.route('/profile', methods=["GET"])
def getItems():
    items = db.Items.find()
    cart_count = len(session.get('cart', []))
    return render_template("profile.html", item=items, cart_count=cart_count)

@app.route('/AddItem1', methods=["POST", "GET"])
def add_item1():
    if request.method == 'POST':
        Name = request.form['Name']
        email = request.form['email']
        Amount = request.form['Amount']
        Description = request.form['Description']
        image = request.form['image']
        item = {'Name': Name, 'email': email, 'Amount': Amount, 'Description': Description, 'image': image}
        db.Items.insert_one(item)
        items = db.Items.find()
        cart_count = len(session.get('cart', []))
        return render_template("profile.html", item=items, cart_count=cart_count)
    return "Success"

# Display Catalog
@app.route("/getCatalog")
def getCatalog():
    items = list(db.Items.find())
    cart_count = len(session.get('cart', []))
    return render_template("catalog.html", item=items, cart_count=cart_count)

@app.route('/delete_item', methods=["POST"])
def delete_product():
    if request.method == 'POST':
        delete_id = request.form['delete_id']
        db.Items.delete_one({"_id": ObjectId(delete_id)})
    items = list(db.Items.find())
    cart_count = len(session.get('cart', []))
    return render_template("profile.html", item=items, cart_count=cart_count)

# View item
@app.route('/viewproduct', methods=['GET', 'POST'])
def view():
    if request.method == 'POST':
        id = request.form['id']
        Name = request.form['Name']
        Amount = request.form['Amount']
        Description = request.form['Description']
        image = request.form['image']
        cart_count = len(session.get('cart', []))
        return render_template('ViewItem.html', id=id, Name=Name, Description=Description, Amount=Amount, image=image, cart_count=cart_count)

@app.route('/AddToCart', methods=['POST'])
def add_to_cart():
    id = request.form.get('id')
    Name = request.form.get('Name')
    Amount = request.form.get('Amount')
    image = request.form['image']
    item = {'id': id, 'Name': Name, 'Amount': Amount, 'image': image}
    cart_items = session.get('cart', [])
    cart_items.append(item)
    session['cart'] = cart_items
    return redirect(url_for('cart'))

@app.route('/ViewCart')
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(float(item['Amount']) for item in cart_items)
    cart_count = len(session.get('cart', []))
    return render_template('ViewCart.html', cart_items=cart_items, total_price=total_price, cart_count=cart_count)

# fix delete 
@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    selected_items = request.form.getlist('selected_items')
    cart_items = session.get('cart', [])
    cart_items = [item for item in cart_items if item['id'] not in selected_items]
    session['cart'] = cart_items
    return redirect(url_for('cart'))

@app.route('/cart/checkout', methods=['POST'])
def checkout():
    session.pop('cart', None)
    return redirect('/checkout_success')

@app.route('/Edit', methods=['POST'])
def edit_item():
    if request.method == 'POST':
        update_id = request.form['update_id']
        email = request.form['email']
        item_id = ObjectId(update_id)
        cart_count = len(session.get('cart', []))
        return render_template("edit.html", item_id=item_id, email=email, cart_count=cart_count)

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
        db.Items.update_one({'_id': item_id}, {'$set': {'Name': name, 'email': email, 'Description': description, 'Amount': Amount, 'image': image}})
        items = db.Items.find({'email': email})
        cart_count = len(session.get('cart', []))
        return render_template("profile.html", item=items, cart_count=cart_count)

if __name__ == "__main__":
    app.run(debug=True)
