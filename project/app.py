from flask import Flask, render_template, json, request, redirect
import database.db_connector as db
import os

app = Flask(__name__)
db_connection = db.connect_to_database()

app.config['MYSQL_CURSORCLASS'] = "DictCursor"

@app.route('/')
def index():
    return render_template('index.html')


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8251))
    app.run(port=port, debug=True)