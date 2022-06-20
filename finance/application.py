import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Select all stocks from user logged in
    userId = session["user_id"]

    # Structure each row of the table
    tableRows = []

    userPortfolio = db.execute("SELECT * FROM user_stock WHERE user_id = ?", userId)
    userCash = db.execute("SELECT cash FROM users WHERE id = ?", userId)
    currentCash = float(userCash[0]['cash'])
    totalCash = currentCash

    for stock in userPortfolio:
        row = []
        symbol = stock['stock']
        stockInfo = lookup(symbol)
        stockShares = stock['quantity']

        # Table data
        row.append(stockInfo['symbol'])
        row.append(stockInfo['name'])
        row.append(stockShares)
        row.append(stockInfo['price'])
        row.append(stockInfo['price'] * stockShares)
        tableRows.append(row)

        totalCash += (stockInfo['price'] * stockShares)
        
    print(tableRows)

    return render_template("index.html", tableRows=tableRows, currentCash=currentCash, totalCash=totalCash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Show preview order
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        stock = lookup(symbol)
        if not stock:
            return apology("Stock not found", 400)
            # return render_template("buy.html", errorMessage='Stock not found')
        elif not shares:
            return apology("Enter a number in shares field", 400)
        # Check if value of shares is valid
        try:
            int(shares)
        except ValueError:
            return apology("Invalid number of shares", 400)
            
        if int(shares) < 0:
            return apology("Invalid number of shares", 400)
            # return render_template("buy.html", errorMessage='Enter a number in shares field')

        else:
            userId = session["user_id"]
            price = stock["price"]
            orderValue = price * int(shares)
            userCash = db.execute("SELECT cash FROM users WHERE id = ?", userId)
            currentCash = int(userCash[0]['cash'])
            if (currentCash - orderValue) > 0:
                # Add into history
                db.execute("INSERT INTO user_history(stock, shares, price, user_id) VALUES (?, ?, ?, ?)", symbol, shares, price, userId)

                # Check if stock already in user's 'wallet'
                userShares = db.execute("SELECT quantity FROM user_stock WHERE user_id = ? AND stock = ?", userId, symbol)
                if not userShares:
                    # Insert new stock in user's table
                    db.execute("INSERT INTO user_stock(user_id, stock, quantity) VALUES(?, ?, ?)", userId, symbol, shares)
                    # Update user's cash in account
                    updateCash = currentCash - orderValue
                    db.execute("UPDATE users SET cash = ? WHERE id = ?", updateCash, userId)
                else:
                    # Update user's shares
                    currentShares = int(userShares[0]['quantity'])
                    updateShares = currentShares + (int(shares))
                    db.execute("UPDATE user_stock SET quantity = ? WHERE user_id = ? AND stock = ?", updateShares, userId, symbol)
                    # Update user's cash in account
                    updateCash = currentCash - orderValue
                    db.execute("UPDATE users SET cash = ? WHERE id = ?", updateCash, userId)
            else:
                return apology("Cash insufficient", 400)
                # return render_template("buy.html", errorMessage='Cash insufficient')
            return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    userId = session["user_id"]
    transactionDetails = db.execute("SELECT * FROM user_history WHERE user_id = ?", userId)
    return render_template("history.html", transactionDetails=transactionDetails)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        # List of rows, each row being a dict
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Search for stock's symbol
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Invalid symbol", 400)
        stock = lookup(symbol)
        print(stock)
        if not stock:
            return apology("Invalid symbol", 400)
            # return render_template("quote.html", errorMessage='Stock not found')
        else:
            return render_template("quoted.html", stock=stock)
    return render_template("quote.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Check if user provided a user and a password
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        username = request.form.get("username")
        # Check if username already exists
        existentUser = db.execute("SELECT id FROM users WHERE username=?", username)

        if not existentUser:
            # Check if both passwords match
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")
            if password == confirmation:
                # We will insert into the table the hashed password
                hash_pass = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", username, hash_pass)
                #Redirect to login
                return redirect("/login")
            else:
                return apology("Passwords don't match", 400)
                # return render_template("register.html", errorMessage="Passwords don't match")

        else:
            return apology("Username is already in use", 400)
            # return render_template("register.html", errorMessage="Username is already in use")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Select all stocks from user logged in
    userId = session["user_id"]
    # GET request = render user's stocks
    userPortfolio = db.execute("SELECT * FROM user_stock WHERE user_id = ?", userId)
    # List of available stocks to sell
    availableStocks = []
    for stock in userPortfolio:
        symbol = stock['stock']
        availableStocks.append(symbol)

    # POST request = sell stocks
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("Choose a stock", 400)
            # return render_template("sell.html", errorMessage='Choose a stock')
        elif not shares:
            return apology("Enter a number in shares field", 400)
            #return render_template("sell.html", errorMessage='Enter a number in shares field')
        elif int(shares) < 0:
            return apology("Invalid number of shares", 400)
        else:
            userShares = db.execute("SELECT quantity FROM user_stock WHERE user_id = ? AND stock = ?", userId, symbol)
            currentShares = int(userShares[0]['quantity'])
            if (int(shares) > currentShares):
                return apology("Insufficient shares", 400)
                # return render_template("sell.html", errorMessage='Insufficient shares')

            # Transaction's data
            stockInfo = lookup(symbol)
            price = stockInfo["price"]
            orderValue = price * int(shares)
            userCash = db.execute("SELECT cash FROM users WHERE id = ?", userId)
            currentCash = int(userCash[0]['cash'])
            # Add into history
            formattedShares = ("-"+str(shares))
            db.execute("INSERT INTO user_history(stock, shares, price, user_id) VALUES (?, ?, ?, ?)", symbol, formattedShares, price, userId)
            
            # Update user's portfolio
            updateShares = currentShares - int(shares)
            if updateShares == 0:
                # If user sells all shares
                db.execute("DELETE FROM user_stock WHERE user_id = ? AND stock = ?", userId, symbol)
            else:
                # If user sells only part of shares
                db.execute("UPDATE user_stock SET quantity = ? WHERE user_id = ? AND stock = ?", updateShares, userId, symbol)

            # Update user's cash in account
            updateCash = currentCash + orderValue
            db.execute("UPDATE users SET cash = ? WHERE id = ?", updateCash, userId)
            return redirect("/")

    return render_template("sell.html", availableStocks=availableStocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
