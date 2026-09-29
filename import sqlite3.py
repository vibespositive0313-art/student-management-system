import sqlite3
from datetime import datetime


DB_NAME = "student_management.db"


def connect():
    return sqlite3.connect(DB_NAME)




def create_tables():
    con = connect()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            course TEXT,
            semester INTEGER,
            phone TEXT,
            email TEXT,
            address TEXT,
            admission_date TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject TEXT,
            marks REAL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject TEXT,
            total_classes INTEGER,
            attended_classes INTEGER,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    con.commit()
    con.close()




def add_student():
    print("\n========== ADD STUDENT ==========")

    name = input("Enter student name: ").strip()

    if not name:
        print("Student name cannot be empty.")
        return

    try:
        age = int(input("Enter age: "))
        semester = int(input("Enter semester: "))
    except ValueError:
        print("Age and semester must be numbers.")
        return

    gender = input("Enter gender: ")
    course = input("Enter course: ")
    phone = input("Enter phone number: ")
    email = input("Enter email: ")
    address = input("Enter address: ")

    admission_date = datetime.now().strftime("%d-%m-%Y")

    con = connect()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO students
        (name, age, gender, course, semester, phone, email,
         address, admission_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        age,
        gender,
        course,
        semester,
        phone,
        email,
        address,
        admission_date
    ))

    con.commit()

    student_id = cur.lastrowid

    con.close()

    print("\nStudent added successfully.")
    print("Student ID:", student_id)




def view_students():
    print("\n========== STUDENT LIST ==========")

    con = connect()
    cur = con.cursor()

    cur.execute("""
        SELECT id, name, age, gender, course,
               semester, phone, email, address,
               admission_date
        FROM students
        ORDER BY id
    """)

    students = cur.fetchall()

    con.close()

    if not students:
        print("No students found.")
        return

    for student in students:
        print("\n----------------------------------------")
        print("Student ID      :", student[0])
        print("Name            :", student[1])
        print("Age             :", student[2])
        print("Gender          :", student[3])
        print("Course          :", student[4])
        print("Semester        :", student[5])
        print("Phone           :", student[6])
        print("Email           :", student[7])
        print("Address         :", student[8])
        print("Admission Date  :", student[9])

    print("----------------------------------------")




def search_student():
    print("\n========== SEARCH STUDENT ==========")

    keyword = input("Enter student name, ID or course: ").strip()

    con = connect()
    cur = con.cursor()

    if keyword.isdigit():
        cur.execute("""
            SELECT * FROM students
            WHERE id = ?
        """, (int(keyword),))
    else:
        cur.execute("""
            SELECT * FROM students
            WHERE name LIKE ?
               OR course LIKE ?
        """, (
            "%" + keyword + "%",
            "%" + keyword + "%"
        ))

    students = cur.fetchall()

    con.close()

    if not students:
        print("No student found.")
        return

    for student in students:
        print("\n--------------------------------")
        print("ID       :", student[0])
        print("Name     :", student[1])
        print("Age      :", student[2])
        print("Gender   :", student[3])
        print("Course   :", student[4])
        print("Semester :", student[5])
        print("Phone    :", student[6])
        print("Email    :", student[7])
        print("Address  :", student[8])



def update_student():
    print("\n========== UPDATE STUDENT ==========")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid student ID.")
        return

    con = connect()
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cur.fetchone()

    if student is None:
        print("Student not found.")
        con.close()
        return

    print("\nEnter new details.")

    name = input("Name: ")
    gender = input("Gender: ")
    course = input("Course: ")

    try:
        age = int(input("Age: "))
        semester = int(input("Semester: "))
    except ValueError:
        print("Age and semester must be numbers.")
        con.close()
        return

    phone = input("Phone: ")
    email = input("Email: ")
    address = input("Address: ")

    cur.execute("""
        UPDATE students
        SET name = ?,
            age = ?,
            gender = ?,
            course = ?,
            semester = ?,
            phone = ?,
            email = ?,
            address = ?
        WHERE id = ?
    """, (
        name,
        age,
        gender,
        course,
        semester,
        phone,
        email,
        address,
        student_id
    ))

    con.commit()
    con.close()

    print("Student details updated successfully.")


def delete_student():
    print("\n========== DELETE STUDENT ==========")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid student ID.")
        return

    con = connect()
    cur = con.cursor()

    cur.execute(
        "SELECT name FROM students WHERE id = ?",
        (student_id,)
    )

    student = cur.fetchone()

    if student is None:
        print("Student not found.")
        con.close()
        return

    confirm = input(
        "Delete " + student[0] + "? (yes/no): "
    ).lower()

    if confirm == "yes":

        cur.execute(
            "DELETE FROM marks WHERE student_id = ?",
            (student_id,)
        )

        cur.execute(
            "DELETE FROM attendance WHERE student_id = ?",
            (student_id,)
        )

        cur.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        con.commit()

        print("Student deleted successfully.")

    else:
        print("Delete operation cancelled.")

    con.close()



def add_marks():
    print("\n========== ADD MARKS ==========")

    try:
        student_id = int(input("Enter student ID: "))
        marks = float(input("Enter marks: "))
    except ValueError:
        print("Please enter valid numbers.")
        return

    subject = input("Enter subject: ")

    if marks < 0 or marks > 100:
        print("Marks must be between 0 and 100.")
        return

    con = connect()
    cur = con.cursor()

    cur.execute(
        "SELECT name FROM students WHERE id = ?",
        (student_id,)
    )

    student = cur.fetchone()

    if student is None:
        print("Student not found.")
        con.close()
        return

    cur.execute("""
        INSERT INTO marks
        (student_id, subject, marks)
        VALUES (?, ?, ?)
    """, (
        student_id,
        subject,
        marks
    ))

    con.commit()
    con.close()

    print("Marks added successfully.")




def view_marks():
    print("\n========== VIEW MARKS ==========")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid student ID.")
        return

    con = connect()
    cur = con.cursor()

    cur.execute("""
        SELECT students.name,
               marks.subject,
               marks.marks
        FROM marks
        JOIN students
        ON students.id = marks.student_id
        WHERE students.id = ?
    """, (student_id,))

    records = cur.fetchall()

    con.close()

    if not records:
        print("No marks found.")
        return

    print("\nStudent:", records[0][0])

    total = 0

    for record in records:
        print(
            "Subject:",
            record[1],
            "| Marks:",
            record[2]
        )

        total += record[2]

    percentage = total / len(records)

    print("--------------------------------")
    print("Total Subjects :", len(records))
    print("Total Marks    :", total)
    print("Percentage     :", round(percentage, 2), "%")


# -----------------------------------------
# ADD ATTENDANCE
# -----------------------------------------

def add_attendance():
    print("\n========== ADD ATTENDANCE ==========")

    try:
        student_id = int(input("Enter student ID: "))
        total_classes = int(
            input("Total classes: ")
        )
        attended_classes = int(
            input("Attended classes: ")
        )
    except ValueError:
        print("Please enter numbers only.")
        return

    if total_classes <= 0:
        print("Total classes must be greater than zero.")
        return

    if attended_classes < 0 or attended_classes > total_classes:
        print("Invalid attended class value.")
        return

    subject = input("Enter subject: ")

    con = connect()
    cur = con.cursor()

    cur.execute(
        "SELECT name FROM students WHERE id = ?",
        (student_id,)
    )

    student = cur.fetchone()

    if student is None:
        print("Student not found.")
        con.close()
        return

    cur.execute("""
        INSERT INTO attendance
        (student_id, subject,
         total_classes, attended_classes)
        VALUES (?, ?, ?, ?)
    """, (
        student_id,
        subject,
        total_classes,
        attended_classes
    ))

    con.commit()
    con.close()

    percentage = (
        attended_classes / total_classes
    ) * 100

    print("Attendance added successfully.")
    print("Attendance:", round(percentage, 2), "%")


# -----------------------------------------
# VIEW ATTENDANCE
# -----------------------------------------

def view_attendance():
    print("\n========== VIEW ATTENDANCE ==========")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid student ID.")
        return

    con = connect()
    cur = con.cursor()

    cur.execute("""
        SELECT students.name,
               attendance.subject,
               attendance.total_classes,
               attendance.attended_classes
        FROM attendance
        JOIN students
        ON students.id = attendance.student_id
        WHERE students.id = ?
    """, (student_id,))

    records = cur.fetchall()

    con.close()

    if not records:
        print("No attendance record found.")
        return

    print("\nStudent:", records[0][0])

    for record in records:

        subject = record[1]
        total = record[2]
        attended = record[3]

        percentage = (attended / total) * 100

        print("\nSubject:", subject)
        print("Total Classes:", total)
        print("Attended:", attended)
        print(
            "Attendance:",
            round(percentage, 2),
            "%"
        )



def student_details():
    print("\n========== STUDENT DETAILS ==========")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    con = connect()
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cur.fetchone()

    con.close()

    if student is None:
        print("Student not found.")
        return

    print("\n================================")
    print("         STUDENT PROFILE")
    print("================================")
    print("ID            :", student[0])
    print("Name          :", student[1])
    print("Age           :", student[2])
    print("Gender        :", student[3])
    print("Course        :", student[4])
    print("Semester      :", student[5])
    print("Phone         :", student[6])
    print("Email         :", student[7])
    print("Address       :", student[8])
    print("Admission Date:", student[9])
    print("================================")



def admin_menu():
    while True:

        print("\n================================")
        print("          ADMIN MENU")
        print("================================")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Add Marks")
        print("7. View Marks")
        print("8. Add Attendance")
        print("9. View Attendance")
        print("10. Student Details")
        print("11. Logout")
        print("================================")

        choice = input("Enter choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            add_marks()

        elif choice == "7":
            view_marks()

        elif choice == "8":
            add_attendance()

        elif choice == "9":
            view_attendance()

        elif choice == "10":
            student_details()

        elif choice == "11":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")




def main():

    create_tables()

    while True:

        print("\n")
        print("==========================================")
        print("       STUDENT MANAGEMENT SYSTEM")
        print("==========================================")
        print("1. Admin Login")
        print("2. Register Student")
        print("3. View Students")
        print("4. Search Student")
        print("5. View Student Details")
        print("6. Exit")
        print("==========================================")

        choice = input("Enter your choice: ")

        if choice == "1":

            password = input("Enter admin password: ")

            if password == "admin123":
                print("Login successful.")
                admin_menu()
            else:
                print("Wrong password.")

        elif choice == "2":
            add_student()

        elif choice == "3":
            view_students()

        elif choice == "4":
            search_student()

        elif choice == "5":
            student_details()

        elif choice == "6":
            print("Thank you for using Student Management System.")
            break

        else:
            print("Invalid choice. Please try again.")




if __name__ == "__main__":
    main()