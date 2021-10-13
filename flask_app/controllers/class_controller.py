from flask.helpers import flash
from flask_app import app
from flask import redirect, render_template, session, request, url_for
from flask_app.models.classroom import Class
from flask_app.models.enrollment import Enrollment


@app.route('/classes')
def show_classes():
    all_classes = Class.show_classes()
    return render_template('classes.html', all_classes=all_classes)


@app.route('/add_class/<int:class_id>')
def add_class(class_id):
    data = {
        "student_id": session['student_id'],
        "class_id": class_id
    }
    Enrollment.add_student_to_class(data)
    return redirect('/student_dashboard')
