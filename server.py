from flask_app import app
from flask_app.controllers import student_controller, class_controller


if __name__ == "__main__":
    app.run(debug=True)
