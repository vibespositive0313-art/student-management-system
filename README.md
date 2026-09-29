# Student Management System

## Project Overview
A simple **Python + SQLite Student Management System** for storing and managing student information.

The program provides a main menu for student registration, viewing, searching, and viewing student details. An admin menu provides additional operations such as update, delete, marks, and attendance management.

## Technologies Used
- Python
- SQLite3
- Console / Command Line Interface

## Main Features
- Admin login
- Register student
- View all students
- Search student by name, ID, or course
- View student details
- Update and delete student records
- Add and view marks
- Add and view attendance
- SQLite database storage

## Database
The program creates a database named `student_management.db` with these tables:
- `students`
- `marks`
- `attendance`

## How to Run
1. Install Python 3.
2. Keep the Python file and run:

```bash
python "import sqlite3.py"
```

3. Follow the menu shown in the terminal.

> The current source code uses `admin123` as the admin password.


## Screenshots

### Student List
<img width="477" height="501" alt="Screenshot 2026-09-29 203911" src="https://github.com/user-attachments/assets/cccdc225-469b-46ac-9583-a18ded1f44ec" />

### Student Registration
<img width="518" height="627" alt="Screenshot 2026-09-29 203924" src="https://github.com/user-attachments/assets/103da6cc-1478-40a4-be79-e7593ac82061" />


## Project Structure

```text
Student Management System/
├── import sqlite3.py
├── student_management.db        # created when the program runs
├── system_flowchart.png
├── admin_flowchart.png
├── student_list.png
├── student_registration.png
└── README.md
```

## Conclusion
This project demonstrates basic student record management using Python functions and SQLite database operations. It is suitable as a simple console-based academic project and can be extended later with a graphical interface, stronger authentication, and more validation.
