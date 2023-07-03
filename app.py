from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.secret_key = 'Vaibhav'

app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "clothingstore"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route("/")
def index():
    if 'loginEmail' in session:
        return 'Logged in as ' + session['loginEmail']
    return 'Not logged in'
    # return render_template('index.html')
    

#home
@app.route("/home")
def home():

    return render_template('index.html')

#checkout
@app.route("/checkout")
def checkout():
    return render_template('checkout.html')

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        loginEmail = request.form['loginEmail']
        LoginPassword = request.form['LoginPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE email = %s AND password = %s', (loginEmail, LoginPassword))
        user = cur.fetchone()

        if user:
            session['loginEmail'] = user['name']  # Store username in session
            return redirect('/home')
        else:
            return 'Invalid username or password'

    return render_template('login.html')



# signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query to insert user data into the database
        cur.execute("INSERT INTO user (name, gender, email, password) VALUES (%s, %s, %s, %s)",
                    (name, gender, email, password))

        # Commit to the database
        mysql.connection.commit()

        # Close cursor
        cur.close()

        # Redirect to a success page or display a success message
        return redirect('/login')

    # Render the registration form template for GET requests
    return render_template('signup.html')


UPLOAD_FOLDER = 'static/ProductsImage'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/products', methods=['GET', 'POST'])
def products():
    

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()


    if request.method == 'POST':
        pname = request.form['name']
        pdesc = request.form['Description']
        price = request.form['price']

        
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO products (pname, pdesc, price, pimg) VALUES (%s, %s, %s, %s)",
                    (pname, pdesc, price))

        mysql.connection.commit()
        cur.close()
    
    return render_template('products.html', products=products)

if __name__ == "__main__":
    app.run(debug=True)