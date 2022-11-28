from flask import Flask, render_template, json, request, redirect, session
import database.db_connector as db
import os

app = Flask(__name__)
app.secret_key = '1234'
db_connection = db.connect_to_database()

app.config['MYSQL_CURSORCLASS'] = "DictCursor"


@app.route('/login', methods=["GET", "POST"])
def login():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        query = 'SELECT * FROM Users WHERE username = %s AND password = %s'
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['userId']
            session['username'] = account['username']
            # Redirect to home page
            return render_template('index.html')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            return render_template('login.html', msg=msg)

    # Show the login form with message (if any)
    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        query = 'SELECT * FROM Users WHERE username = %s AND password = %s'
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['userId']
            session['username'] = account['username']
            # Redirect to home page
            return render_template('index.html')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            return render_template('login.html', msg=msg)

    # Show the login form with message (if any)
    return render_template('login.html')

@app.route('/', methods=["GET", "POST"])
def index():
    if 'loggedin' in session:
        if session['loggedin']:
            return render_template('index.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')




# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8251))
    app.run(port=port, debug=True)