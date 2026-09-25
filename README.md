# Student Management System

A web-based **Student Management System** developed using **Python Flask**, **SQLite**, **Bootstrap 5**, **HTML**, **CSS**, and **JavaScript**. The application allows administrators to register, log in securely, and perform complete CRUD (Create, Read, Update, Delete) operations on student records through a responsive dashboard.

---

## Features

* User Registration & Login Authentication
* Secure session-based login
* Add new student records
* View all students
* Search students by name or roll number
* Edit student details
* Delete student records
* Responsive Bootstrap dashboard
* SQLite database integration

---

## Tech Stack

| Technology  | Purpose                   |
| ----------- | ------------------------- |
| Python      | Backend programming       |
| Flask       | Web framework             |
| SQLite      | Database                  |
| HTML5       | Web page structure        |
| CSS3        | Styling                   |
| Bootstrap 5 | Responsive user interface |
| JavaScript  | Client-side interactions  |
| Jinja2      | Dynamic HTML templates    |

---

## Project Structure

student_management/

├── app.py

├── students.db

├── static/

│ ├── css/

│ │ └── style.css

│ └── js/

│ └── script.js

├── templates/

│ ├── login.html

│ ├── register.html

│ ├── dashboard.html

│ ├── students.html

│ ├── add_student.html

│ ├── edit_student.html

│ └── student_details.html

└── README.md

---

## Database Schema

### Users Table

* **id** – INTEGER (Primary Key)
* **name** – TEXT
* **email** – TEXT (Unique)
* **password** – TEXT

### Students Table

* **id** – INTEGER (Primary Key)
* **name** – TEXT
* **roll_no** – TEXT (Unique)
* **department** – TEXT
* **year** – TEXT
* **email** – TEXT
* **phone** – TEXT

---

## Installation

1. Clone the project repository.
2. Open the project folder in VS Code.
3. Install Flask using pip.
4. Run the application with `python app.py`.
5. Open your browser and visit: `http://127.0.0.1:5000`

---

## How to Use

1. Register a new administrator account.
2. Log in using your email and password.
3. Open the Dashboard.
4. Add student information.
5. View all student records.
6. Search students by name or roll number.
7. Edit or delete student details whenever required.
8. Log out securely after completing your work.

---

## Modules

* Login
* Register
* Dashboard
* Add Student
* View Students
* Edit Student
* Student Details

---

## CRUD Operations

**Create:** Add a new student record.

**Read:** View and search student information.

**Update:** Modify existing student details.

**Delete:** Remove student records from the database.

---

## Future Enhancements

* Student profile photo upload
* Attendance management
* Marks and grade management
* PDF report generation
* Role-based login (Admin & Faculty)
* Encrypted password security

---

## Author

**Grande Akanksha**

B.Tech – Computer Science & Engineering

Sri Mittapalli College of Engineering

---

## License

**This project is developed for **academic and educational purposes only.**
