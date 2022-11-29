from flask import Flask, render_template, json, request, redirect, session, url_for
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
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
 
        # Check if account exists using MySQL
        query = 'SELECT * FROM Users WHERE username = %s AND password = %s'
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table, return error
        if account:
            msg = "User already exists!"
            return render_template('register.html', msg=msg)
        else:
            # Account doesnt exist
            query = 'INSERT INTO `Users` (`username`, `email`, `password`) VALUES (%s, %s, %s);'
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(username, password, email))
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['userId']
            session['username'] = account['username']
            # Redirect to home page
            return render_template('index.html')
    # Show the login form with message (if any)
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'loggedin' in session:
        if session['loggedin']:
            # clear user data from session
            session['loggedin'] = False
            session['id'] = None
            session['username'] = None
            return render_template('login.html')
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/', methods=["GET", "POST"])
def index():
    if 'loggedin' in session:
        if session['loggedin'] and session['username']:
            if request.method == "GET":
                # get the meal log for the user, which gives us the mealLogEntries_mealLogEntryId
                meal_log_query = "SELECT * FROM MealLogs WHERE users_userId = '%s';" % (session['id'])
                cursor = db.execute_query(db_connection=db_connection, query=meal_log_query)
                meal_log_data = cursor.fetchall()


                return render_template('index.html', meal_log_data=meal_log_data)
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/settings', methods=["GET", "POST"])
def settings():
    if session['loggedin']:
        if request.method == "GET":
            query = "SELECT * FROM Users WHERE userId = '%s';" % (session['id'])
            cursor = db.execute_query(db_connection=db_connection, query=query)
            data = cursor.fetchone()

            return render_template('settings.html', data=data)
        if request.method == "POST":
            return render_template('settings.html')

@app.route('/edit_metrics', methods=["GET", "POST"])
def edit_metrics():
    if request.method == "GET":
        query = "SELECT height, weight, age FROM Users WHERE userId = '%s';" % (session['id'])
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchone()
        return render_template('edit_metrics.html', data=data)
    if request.method == "POST":
        # run sql query to update
        # run sql query to update
        if request.form.get("edit_metrics"):
            height = request.form["height"]
            weight = request.form["weight"]
            age = request.form["age"]

            query = "UPDATE Users SET height = %s, weight = %s, age = %s WHERE userId = %s;"
            query_params=(height, weight, age, session['id'])
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_params)
        
        return redirect(url_for('settings'))

@app.route('/edit_contact', methods=["GET", "POST"])
def edit_contact():
    if request.method == "GET":
        query = "SELECT username, email FROM Users WHERE userId = '%s';" % (session['id'])
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchone()
        return render_template('edit_contact.html', data=data)
    if request.method == "POST":
        # run sql query to update
        if request.form.get("edit_metrics"):
            height = request.form["height"]
            weight = request.form["weight"]
            age = request.form["age"]

            query = "UPDATE Users SET height = '%s', weight = '%s', age = '%s' WHERE userId = '%s';"
            query_params=(height, weight, age, session['id'])
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_params)

            query = "SELECT * FROM Users WHERE userId = '%s';" % (session['id'])
            cursor = db.execute_query(db_connection=db_connection, query=query)
            data = cursor.fetchone()
            return render_template('settings.html', data=data)
        else:
            return redirect('index.html')


@app.route('/learning')
def learning():
    return render_template('learning.html')

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8251))
    app.run(port=port, debug=True)