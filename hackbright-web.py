from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def home_page():

    student_names = hackbright.get_student_names()
    titles = hackbright.get_project_titles()

    return render_template("homepage.html", student_names=student_names, titles=titles)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github','jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    projects = hackbright.all_projects(first,last)
    return render_template("student_info.html",first=first,last=last,github=github,projects=projects)

@app.route("/student-add")
def student_add():
    """Add a student."""
    return render_template("student_add.html")

@app.route("/student-added", methods=['GET','POST'])
def student_added():
    first_name = request.form.get("first")
    last_name = request.form.get("last")
    github = request.form.get("github")

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("student_added.html",first=first_name, last=last_name, github = github)

@app.route("/project-info")
def get_project_info():
    return render_template("get_project_info.html")

@app.route("/project")
def project_info():
    title = request.args.get("title")
    description, max_grade = hackbright.project_info(title)
    # grades = hackbright.students_grades(title)
    students_info = hackbright.get_student_info(title)

    return render_template("get_project_info.html", title=title, description=description, max_grade = max_grade, students_info=students_info)

if __name__ == "__main__":
    app.run(debug=True)