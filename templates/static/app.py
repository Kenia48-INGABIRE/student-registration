from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            classroom TEXT,
            photo TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add():
    conn = get_db()
    conn.execute(
        "INSERT INTO students (name, age, classroom, photo) VALUES (?, ?, ?, ?)",
        (request.form["name"], request.form["age"], request.form["classroom"], request.form["photo"])
    )
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    conn = get_db()

    if request.method == "POST":
        conn.execute(
            "UPDATE students SET name=?, age=?, classroom=?, photo=? WHERE id=?",
            (
                request.form["name"],
                request.form["age"],
                request.form["classroom"],
                request.form["photo"],
                id
            )
        )
        conn.commit()
        conn.close()
        return redirect("/")

    student = conn.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("update.html", student=student)

app.run(debug=True)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)