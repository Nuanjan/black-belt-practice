from flask.helpers import flash
from flask_app import app
from flask import redirect, render_template, session, request, url_for
from flask_app.models.student import Student
from flask_app.models.classroom import Class


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt,


@app.route('/')
def index():
    isShow = ""
    if 'isShow' in session:
        isShow = session["isShow"]
    return render_template('index.html', isShow=isShow)


@app.route('/register-login', methods=['POST'])
def register_student():
    print("this is request form", request.form)
    if request.form['which_form'] == "register":
        if not Student.validate_student(request.form):
            session['isShow'] = request.form['which_form']
            return redirect('/')
        hashed_password = bcrypt.generate_password_hash(
            request.form['password'])
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['e_mail'],
            "password": hashed_password
        }
        addStudent = Student.add_student(data)
        if not addStudent:
            return redirect('/')
        session['student_id'] = addStudent
        return redirect('/student_dashboard')
    elif request.form['which_form'] == "login":
        data = {"email": request.form['e_mail']}
        student_in_db = Student.get_student_by_email(data)
        validation_data = {
            "student_in_db": student_in_db,
            "password": request.form["password"]
        }
        if not Student.validate_login_student(validation_data):
            session['isShow'] = request.form['which_form']
            return redirect('/')
        elif not bcrypt.check_password_hash(student_in_db.password, request.form['password']):
            print(bcrypt.check_password_hash(
                student_in_db.password, request.form['password']))
            flash("Invalid student/password")
            return redirect('/')
        session['isShow'] = request.form['which_form']
        session['student_id'] = student_in_db.id
        return redirect('/student_dashboard')


@app.route('/student_dashboard')
def student_dashboard():
    show_table = ""
    if 'student_id' in session:
        data = {
            "id": session['student_id']
        }
        one_student = Student.get_student_by_id(data)
        classes_enrolled_students = Class.class_with_enrolled_students()
        print(" this is class with students:", classes_enrolled_students)
        return render_template('student_dashboard.html', one_student=one_student, show_table=show_table, classes_enrolled_students=classes_enrolled_students)
    else:
        return redirect('/forbidden')


@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')


@app.route('/forbidden')
def unauthorize():
    return render_template('forbidden.html')
