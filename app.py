from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "student_management_secret_key"

DATABASE = "database.db"


# ---------------- DATABASE CONNECTION ----------------

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- HOME ----------------

@app.route("/")
def home():
    return redirect(url_for("login"))


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Check passwords
        if password != confirm_password:
            return render_template(
                "register.html",
                error="Passwords do not match"
            )

        conn = get_db()

        # Check if username already exists
        existing_user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing_user:
            conn.close()

            return render_template(
                "register.html",
                error="Username already exists"
            )

        # Insert user
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        # Check if username exists
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()

        if user is None:
            conn.close()
            return render_template(
                "login.html",
                message="Please register before login!",
                alert_type="warning"
            )

        # Check password
        valid = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        conn.close()

        if valid:
            session["user"] = username
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            message="Incorrect password!",
            alert_type="danger"
        )

    return render_template("login.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    # Total students
    total = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    # CSE students
    cse_count = conn.execute(
        "SELECT COUNT(*) FROM students WHERE department = 'CSE'"
    ).fetchone()[0]

    # Average marks
    avg_marks = conn.execute(
        "SELECT AVG(marks) FROM students"
    ).fetchone()[0]

    # Average attendance
    avg_attendance = conn.execute(
        "SELECT AVG(attendance) FROM students"
    ).fetchone()[0]

    conn.close()

    # Handle empty database
    if avg_marks is None:
        avg_marks = 0

    if avg_attendance is None:
        avg_attendance = 0

    return render_template(
        "dashboard.html",
        total=total,
        cse_count=cse_count,
        avg_marks=round(avg_marks, 2),
        avg_attendance=round(avg_attendance, 2)
    )

# ---------------- STUDENTS ----------------

@app.route("/students")
def students():

    if "user" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "")
    department = request.args.get("department", "")
    year = request.args.get("year", "")

    query = "SELECT * FROM students WHERE 1=1"
    parameters = []

    # Search
    if search:

        query += """
        AND (
            name LIKE ?
            OR email LIKE ?
            OR id LIKE ?
        )
        """

        search_value = f"%{search}%"

        parameters.extend([
            search_value,
            search_value,
            search_value
        ])

    # Department filter
    if department:

        query += " AND department = ?"

        parameters.append(department)

    # Year filter
    if year:

        query += " AND year = ?"

        parameters.append(year)

    query += " ORDER BY id DESC"

    conn = get_db()

    students_data = conn.execute(
        query,
        parameters
    ).fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students_data,
        search=search,
        department=department,
        year=year
    )


# ---------------- ADD STUDENT ----------------

@app.route("/add", methods=["GET", "POST"])
def add_student():

    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        year = request.form["year"]
        marks = request.form["marks"]
        attendance = request.form["attendance"]

        conn = get_db()

        conn.execute(
            """
            INSERT INTO students
            (name, email, department, year, marks, attendance)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                email,
                department,
                year,
                marks,
                attendance
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    return render_template("add_student.html")


# ---------------- STUDENT DETAILS ----------------

@app.route("/student/<int:id>")
def student_details(id):

    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return "Student not found"

    return render_template(
        "student_details.html",
        student=student
    )


# ---------------- EDIT STUDENT ----------------

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        year = request.form["year"]
        marks = request.form["marks"]
        attendance = request.form["attendance"]

        conn.execute(
            """
            UPDATE students
            SET
                name = ?,
                email = ?,
                department = ?,
                year = ?,
                marks = ?,
                attendance = ?
            WHERE id = ?
            """,
            (
                name,
                email,
                department,
                year,
                marks,
                attendance,
                id
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return "Student not found"

    return render_template(
        "edit_student.html",
        student=student
    )


# ---------------- DELETE STUDENT ----------------

@app.route("/delete/<int:id>")
def delete_student(id):

    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("students"))


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)