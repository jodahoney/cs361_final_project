from flask import Flask, render_template, json, request, redirect, session, url_for
import database.db_connector as db
import os
import requests

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
            query = "INSERT INTO Users \
                (username, email, password) \
                VALUES (%s, %s, %s);"
            cursor = db.execute_query(
                db_connection=db_connection, 
                query=query, 
                query_params=(username, email, password)
                )
            return redirect(url_for('login'))
    
    if request.method == "GET":
        return render_template('register.html')

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

                food_query = "SELECT * FROM Foods"
                cursor = db.execute_query(db_connection=db_connection, query=food_query)
                food_data = cursor.fetchall()

                meal_query = "SELECT * FROM Meals WHERE createdBy = %s;" % (session['id'])
                cursor = db.execute_query(db_connection=db_connection, query=meal_query)
                meal_data = cursor.fetchall()

                return render_template('index.html', meal_log_data=meal_log_data, food_data=food_data, meal_data=meal_data)

            if request.method == "POST":
                # create meal
                if request.form.get("add_meal"):
                    foods = request.form.getlist("food-select")

                    # calculate total calories of the meal using partners microservice
                    total_calories = 0

                    for foodId in foods:
                        query = "SELECT carbohydrate, fat, protein FROM Foods WHERE foodId = %s;" % (foodId)
                        cursor = db.execute_query(db_connection=db_connection, query=query)
                        data = cursor.fetchone()
                        
                        for key in data:
                            macro_name = str(key)
                            if key in data:
                                num_macros = data[key]
                            
                                # # if key in data:
                                response = requests.get(f'http://127.0.0.1:5000/calculate-cals/{macro_name}/{num_macros}')
                                data = response.json()
                                total_calories += data['calories']

                    # so now we have total calories using partner's microservice
                    query = "INSERT INTO Meals (totalCalories, CreatedBy) VALUES (%s, %s);" % (total_calories, session['id'])
                    cursor = db.execute_query(db_connection=db_connection, query=query)




                    


                return redirect(url_for('index'))

        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/add_food', methods=["GET", "POST"])
def add_food():
    if request.method == "POST":
        if request.form.get("add_food"):
            foodName = request.form["foodName"]
            carbohydrate = request.form.get("carbohydrate")
            fat = request.form["fat"]
            protein = request.form["protein"]

            query = "INSERT INTO Foods \
                (foodName, carbohydrate, fat, protein) \
                VALUES (%s, %s, %s, %s);"

            cursor = db.execute_query(
                db_connection=db_connection, 
                query=query, 
                query_params=(foodName, carbohydrate, fat, protein)
            )
            return redirect(url_for('add_food'))

    if request.method == "GET":
        return render_template("add_food.html")

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
        if request.form.get("edit_contact"):
            username = request.form["username"]
            email = request.form["email"]

            query = "UPDATE Users SET username = %s, email = %s WHERE userId = %s;"
            query_params=(username, email, session['id'])
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_params)

            return redirect(url_for('settings'))
        else:
            return redirect(url_for('settings'))

@app.route('/advanced_settings', methods=["GET", "POST"])
def edit_advanced():
    if request.method == "GET":
        query = "SELECT password FROM Users WHERE userId = '%s';" % (session['id'])
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchone()
        return render_template('edit_advanced.html', data=data)
    if request.method == "POST":
        # run sql query to update
        if request.form.get("edit_advanced"):
            password = request.form["password"]

            query = "UPDATE Users SET password = %s WHERE userId = %s;"
            query_params=(password, session['id'])
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_params)

            return redirect(url_for('settings'))
        elif request.form.get("delete_account"):
            query = "DELETE FROM Users WHERE userId = '%s';" % (session['id'])
            cursor = db.execute_query(db_connection=db_connection, query=query)

            return redirect(url_for('logout'))
       


@app.route('/learning')
def learning():
    return render_template('learning.html')

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8251))
    app.run(port=port, debug=True)