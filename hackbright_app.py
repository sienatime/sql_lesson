import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    return "Successfully added student: %s %s" % (first_name, last_name)

def get_project_by_title(project):
    query = """SELECT title, description, max_grade from Projects WHERE title = ?"""
    DB.execute(query, (project,))
    row = DB.fetchone()
    return """\
Project: %s
Description: %s
Max Grade: %d""" % (row[0],row[1],row[2])

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects values (?, ?, ?)"""
    desc = " ".join(description)

    DB.execute(query, (title, desc, max_grade))
    CONN.commit()
    return "Successfully added Project: %s" % title

def get_student_grade_on_project(first_name, last_name, title):
    query = """SELECT first_name, last_name, title, grade from ReportCardView WHERE first_name = ? AND last_name = ? AND title = ?"""
    DB.execute(query, (first_name, last_name, title))
    row = DB.fetchone()
    return """\
Student: %s %s
Project: %s
Grade: %d""" % (row[0],row[1],row[2],row[3])

def grade(first_name, last_name, title, grade):
    query = """SELECT github from Students where first_name = ? and last_name = ?"""
    DB.execute(query, (first_name, last_name))
    row = DB.fetchone()
    #use the data we just fetched to then insert into Grades
    if row:
        query = """INSERT into Grades VALUES (?, ?, ?)"""
        DB.execute(query, (row[0], title, grade))
        CONN.commit()
        return "Successfully added grade for %s %s" % (first_name, last_name)
    else:
        return "Did not find student by that name."

def get_student_grades(first_name, last_name):
    query = """SELECT title, grade FROM ReportCardView WHERE first_name = ? AND last_name = ?"""
    DB.execute(query, (first_name, last_name))
    rows = DB.fetchall()
    # return rows
    for thing in rows:
        return thing[0], thing[1]

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(args[0], args[1:-1], args[-1])
        elif command == "student_grade_on_project":
            get_student_grade_on_project(*args)
        elif command == "grade":
            grade(*args)
        elif command == "student_grades":
            get_student_grades(*args)

    CONN.close()

if __name__ == "__main__":
    main()
