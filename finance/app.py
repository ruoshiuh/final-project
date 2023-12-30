import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import pytz

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    # the user wants to deposit money
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        # make sure the input is valid
        if (not amount) or (amount <= 0):
            return apology("The deposit amount is less than or equal to zero")
        # update cash info
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash_new = amount + cash[0]["cash"]
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", cash_new, session["user_id"]
        )
        # UTC time
        tz_London = pytz.timezone("Europe/London")
        datetime_UTC = datetime.now(tz_London)
        datetime_UTC = datetime_UTC.strftime("%Y-%m-%d %H:%M")
        # update deposit transfer record
        db.execute(
            "INSERT INTO transfers (user_id, amount, datetime, status) VALUES (?, ?, ?, ?)",
            session["user_id"],
            amount,
            datetime_UTC,
            "deposit",
        )

        return redirect("/")

    data = db.execute(
        "SELECT symbol, shares FROM holdings WHERE user_id = ?", session["user_id"]
    )
    data_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    current_price = {}
    symbol_value = {}
    cash_balance = data_cash[0]["cash"]
    grand_total = 0

    for row in data:
        # record the current price for each symbol
        current_price[row["symbol"]] = lookup(row["symbol"])["price"]
        # record the value of each symbol
        symbol_value[row["symbol"]] = row["shares"] * current_price[row["symbol"]]
        # record for grand_value
        grand_total += symbol_value[row["symbol"]]

        # format numbers to USD string
        current_price[row["symbol"]] = usd(current_price[row["symbol"]])
        symbol_value[row["symbol"]] = usd(symbol_value[row["symbol"]])

    grand_total += cash_balance
    return render_template(
        "index.html",
        user_id=session["user_id"],
        data=data,
        current_price=current_price,
        symbol_value=symbol_value,
        cash_balance=usd(cash_balance),
        grand_total=usd(grand_total),
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        data = lookup(symbol)

        # check if the input is blank or the symbol does not exist
        if (not symbol) or (not data):
            return apology("Symbol does not exists")
        # check if the share is integer > 0
        if (not shares) or (not shares.isdigit()) or (float(shares) <= 0):
            return apology("Shares is not a positive integer")

        # check if the user has the ability to buy
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if float(cash[0]["cash"]) < (int(shares) * data["price"]):
            return apology("not enough cash to conduct the transaction")

        # update cash number
        cash[0]["cash"] -= int(shares) * data["price"]
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            cash[0]["cash"],
            session["user_id"],
        )

        # UTC time
        tz_London = pytz.timezone("Europe/London")
        datetime_UTC = datetime.now(tz_London)
        datetime_UTC = datetime_UTC.strftime("%Y-%m-%d %H:%M")
        # update buys record
        db.execute(
            "INSERT INTO buys (user_id, price, shares, symbol, datetime, status) VALUES (?, ?, ?, ?, ?, ?)",
            session["user_id"],
            data["price"],
            int(shares),
            data["name"],
            datetime_UTC,
            "buy",
        )

        # update holdings
        holdings = db.execute(
            "SELECT symbol, SUM(shares) FROM holdings WHERE user_id = ? AND symbol = ?",
            session["user_id"],
            symbol.upper(),
        )

        if holdings[0]["symbol"] is None:
            # the first time buy this symbol
            db.execute(
                "INSERT INTO holdings (user_id, symbol, shares) VALUES (?, ?, ?)",
                session["user_id"],
                symbol.upper(),
                int(shares),
            )
        else:
            # the user has bought this symbol before
            shares_new = int(shares) + holdings[0]["SUM(shares)"]
            db.execute(
                "UPDATE holdings SET shares = ? WHERE user_id = ? AND symbol = ?",
                shares_new,
                session["user_id"],
                symbol.upper(),
            )

        # completed! return to home page
        return redirect("/")
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history_symbol = db.execute(
        "SELECT * FROM (SELECT * FROM buys UNION SELECT * FROM sells) WHERE user_id = ? ORDER BY datetime",
        session["user_id"],
    )
    history_transfers = db.execute(
        "SELECT * FROM transfers WHERE user_id = ? ORDER BY datetime",
        session["user_id"],
    )
    for row in history_symbol:
        row["price"] = usd(row["price"])
    for r in history_transfers:
        r["amount"] = usd(r["amount"])
    return render_template(
        "history.html",
        history_symbol=history_symbol,
        history_transfers=history_transfers,
        user_id=session["user_id"],
    )


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    # User reached route via POST
    if request.method == "POST":
        symbol = request.form.get("symbol")
        data = lookup(symbol)

        if (not symbol) or data is None:
            return apology("symbol does not exists")

        # format the price
        data["price"] = usd(data["price"])
        return render_template("quoted.html", data=data)

    # User reached route via GET
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # to see if thers's an id with the same username
        id = db.execute("SELECT id FROM users WHERE username = ?", username)
        if len(id) > 0:
            return apology("username already exits")

        if not username:
            return apology("username is blank")
        if (not password) or (not confirmation):
            return apology("password or confirmation is blank")
        if password != confirmation:
            return apology("Password and Confirm Password not match")

        # add the username and password to database
        hash = generate_password_hash(password, method="pbkdf2", salt_length=16)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        data = db.execute(
            "SELECT shares FROM holdings WHERE user_id = ? AND symbol = ?",
            session["user_id"],
            symbol,
        )

        #### check if the inputs are valid #####
        if not symbol:
            return apology("Please select a symbol")
            # shares is not positive integer or blank
        if (not shares) or (not float(shares).is_integer()) or (float(shares) < 0):
            return apology("Shares is not a positive integer")
            # user doesn't have enough shares
        if int(shares) > data[0]["shares"]:
            return apology("not having enough shares")

        #### update holdings info #####
        shares_new = data[0]["shares"] - int(shares)
        if shares_new == 0:
            db.execute(
                "DELETE FROM holdings WHERE user_id = ? AND symbol = ?",
                session["user_id"],
                symbol,
            )
        else:
            db.execute(
                "UPDATE holdings SET shares = ? WHERE user_id = ? AND symbol = ?",
                shares_new,
                session["user_id"],
                symbol.upper(),
            )

        #### update cash number #####
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash[0]["cash"] += int(shares) * lookup(symbol)["price"]
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            cash[0]["cash"],
            session["user_id"],
        )

        #### update sells info #####
        # UTC time
        tz_London = pytz.timezone("Europe/London")
        datetime_UTC = datetime.now(tz_London)
        datetime_UTC = datetime_UTC.strftime("%Y-%m-%d %H:%M")
        # update sells records
        db.execute(
            "INSERT INTO sells (user_id, price, shares, symbol, datetime, status) VALUES (?, ?, ?, ?, ?, ?)",
            session["user_id"],
            lookup(symbol)["price"],
            int(shares),
            symbol,
            datetime_UTC,
            "sell",
        )
        # completed! return to home page
        return redirect("/")

    data = db.execute(
        "SELECT symbol FROM holdings WHERE user_id = ?", session["user_id"]
    )
    return render_template("sell.html", data=data)
