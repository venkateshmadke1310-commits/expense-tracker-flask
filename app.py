import sqlite3
from flask import Flask, render_template, request, redirect, session, Response

app = Flask(__name__)
app.secret_key = "expense_tracker_secret"

def get_db_connection():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        category TEXT,
        description TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

setup_database()

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    category = request.args.get("category")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    query = "SELECT * FROM expenses WHERE user_id=?"
    total_query = "SELECT SUM(amount) FROM expenses WHERE user_id=?"
    params = [user_id]

    if category:
        query += " AND category=?"
        total_query += " AND category=?"
        params.append(category)
    if from_date:
        query += " AND date>=?"
        total_query += " AND date>=?"
        params.append(from_date)
    if to_date:
        query += " AND date<=?"
        total_query += " AND date<=?"
        params.append(to_date)

    query += " ORDER BY date DESC"

    conn = get_db_connection()
    expenses = conn.execute(query, params).fetchall()
    total = conn.execute(total_query, params).fetchone()[0] or 0
    conn.close()

    return render_template("view.html", expenses=expenses, total=total)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists"
        conn.close()
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/")

        return "Invalid login"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
            (
                session["user_id"],
                request.form["amount"],
                request.form["category"],
                request.form["description"],
                request.form["date"]
            )
        )
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    expense = conn.execute(
        "SELECT * FROM expenses WHERE id=? AND user_id=?",
        (id, session["user_id"])
    ).fetchone()

    if not expense:
        conn.close()
        return "Not allowed", 403

    if request.method == "POST":
        conn.execute(
            "UPDATE expenses SET amount=?, category=?, description=?, date=? WHERE id=? AND user_id=?",
            (
                request.form["amount"],
                request.form["category"],
                request.form["description"],
                request.form["date"],
                id,
                session["user_id"]
            )
        )
        conn.commit()
        conn.close()
        return redirect("/")

    conn.close()
    return render_template("edit.html", expense=expense)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    conn.execute(
        "DELETE FROM expenses WHERE id=? AND user_id=?",
        (id, session["user_id"])
    )
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/summary")
def summary():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    data = conn.execute(
        "SELECT category, SUM(amount) AS total FROM expenses WHERE user_id=? GROUP BY category",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    return render_template("summary.html", summary=data)

@app.route("/monthly")
def monthly_summary():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    data = conn.execute("""
        SELECT strftime('%Y-%m', date) AS month, SUM(amount) AS total
        FROM expenses
        WHERE user_id=?
        GROUP BY month
        ORDER BY month DESC
    """, (session["user_id"],)).fetchall()
    conn.close()

    return render_template("monthly.html", monthly=data)

@app.route("/export/<month>")
def export_month(month):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    expenses = conn.execute("""
        SELECT date, amount, category, description
        FROM expenses
        WHERE strftime('%Y-%m', date)=? AND user_id=?
        ORDER BY date
    """, (month, session["user_id"])).fetchall()
    conn.close()

    def generate():
        yield "Date,Amount,Category,Description\n"
        for e in expenses:
            yield f"{e['date']},{e['amount']},{e['category']},{e['description']}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=expenses_{month}.csv"}
    )

if __name__ == "__main__":
    app.run()
