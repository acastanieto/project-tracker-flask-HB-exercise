"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    first, last, github = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (first, last, github)
    return (first, last, github)


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[2]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "get_project_by_title":
            title = args[0]
            get_project_by_title(title)

        elif command == "get_student_grade":
            github, project_title = args
            get_student_grade(github, project_title)

        elif command == "give_a_grade":
            first_name, last_name, new_grade = args
            give_a_grade(first_name, last_name, new_grade)

def make_new_student(first_name,last_name,github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """
        INSERT INTO Students VALUES(?,?,?)
        """
    db_cursor.execute(QUERY,(first_name, last_name, github))
    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name) 

def get_project_by_title(title):

    QUERY = """
        SELECT * FROM Projects WHERE title = ?
        """
    db_cursor.execute(QUERY,(title,))
    row = db_cursor.fetchone()
    print "Title for this project is %s, the description is %s, and the max grade is %d" % (row[1],row[2],row[3]) 

def get_student_grade(github, project_title):
    QUERY = """
        SELECT grade FROM Grades WHERE project_title = ? AND student_github = ?
        """

    db_cursor.execute(QUERY,(project_title, github,))
    grade = db_cursor.fetchone()
    print type(grade)
    print "The grade for the student with github %s for the project %s is %d" % (github, project_title, grade[0])

def give_a_grade(first_name, last_name, new_grade):

    QUERY = """
        INSERT INTO Grades (student_github, grade) VALUES 
        ((SELECT github FROM Students WHERE first_name = ? AND
        last_name = ?),?);
        """

    db_cursor.execute(QUERY,(first_name, last_name, new_grade,))
    db_connection.commit()
    print "%s %s received a grade %s" % (first_name, last_name, new_grade)

def all_projects(first_name, last_name):

    QUERY = """
        SELECT Grades.project_title, Grades.grade FROM Grades WHERE student_github = 
        (SELECT github FROM Students WHERE first_name = ? AND last_name = ?)
        """  

    db_cursor.execute(QUERY,(first_name, last_name))
    projects = db_cursor.fetchall()

    return projects

def project_info(title):

    QUERY = """
        SELECT description, max_grade FROM Projects WHERE title = ?
        """

    db_cursor.execute(QUERY, (title,))
    project = db_cursor.fetchone()

    return project

def students_grades(title):

    QUERY = """
        SELECT first_name, last_name, grade FROM Students JOIN Grades ON 
        student_github = github WHERE project_title = ?
        """

    db_cursor.execute(QUERY, (title,))
    grades = db_cursor.fetchall()

    return grades

def get_student_info(title):

    QUERY = """
        SELECT first_name, last_name, github, grade FROM Grades 
        JOIN Students ON github = student_github
        WHERE project_title = ?
        """

    db_cursor.execute(QUERY, (title,))
    students_info = db_cursor.fetchall()

    return students_info


if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
