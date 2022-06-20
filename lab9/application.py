import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    errorMessage = " "
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get('name')
        month = request.form.get('month')
        day = request.form.get('day')

        # Additional: if the user changes the HTML code, they can bypass the min/max restrictions.
        # so we will do an additional check here. Also, if the user inserts an input other than a number,
        # it will result in an error and the POST won't be made
        
        checkMonth = int(month)
        checkDay = int(day)
        if (checkMonth >= 1 and checkMonth <= 12) and (checkDay >=1 and checkDay <= 31):
            db.execute("INSERT INTO birthdays(name, month, day) VALUES(?, ?, ?)", name, month, day)
            return redirect("/")

        else:
            birthdaysList = db.execute("SELECT * FROM birthdays")
            return render_template("index.html", errorMessage="Insert a valid date", birthdaysList=birthdaysList)

    else:

        # TODO: Display the entries in the database on index.html
        birthdaysList = db.execute("SELECT * FROM birthdays")
        # Each row is a dictionary

        #print(birthdays)
        return render_template("index.html", birthdaysList=birthdaysList)


