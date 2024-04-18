from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_cors import CORS
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from tables import Base, User, Course, Homework, Quiz
import os
import re

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.secret_key = "super secret key"
CORS(app)

directory = 'backend'
db_filename = 'User.db'
db_path = f"{os.path.join(os.getcwd(), directory, db_filename)}"

# Create an engine object to connect to the SQLite database and create a session
engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
session = Session()

# Query the data
users = session.query(User).all()
courses = session.query(Course).all()
homeworks = session.query(Homework).all()
quizzes = session.query(Quiz).all()

user_id = ''

course_list = {
    "phys_2111": {
        "homework": [
            {"name": "14.1", "date": "02-20-2024"},
            {"name": "template", "date": "due date"}
        ],
        "quizzes_tests": [
            {"name": "Exam 1", "date": "due-date"}
        ]
    },
    "phys_2222": {
        "homework": [],
        "quizzes_tests": []
    }
}



# Given the user's ID and the course name, add the course under the specified user's table
def add_course(user_id, course_name):
    # Check if the user exists
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        print("User doesn't exist.")
        return False
    
    # Check if course already exists for that specific user
    course = session.query(Course).filter_by(user_id=user_id, coursename = course_name).first()
    if course:
        print("Course already exists for this user.")
        return False
    
    # Create a new Course object
    new_course = Course(coursename=course_name, user_id=user_id)

    # Add and commit the new course to the database, and close the session
    session.add(new_course)
    session.commit()
    session.close()

    return True

def remove_course(user_id, course_name):
    course = session.query(Course).filter_by(user_id=user_id, coursename = course_name).first()
    if course:
        session.delete(course)
        session.commit()
    session.close()

def add_homework(course_id, course_name, hw_name, due_date):
    course = session.query(Course).filter_by(id=course_id).first()
    if not course:
        print("Course doesn't exist.")
        return False
    
    # Check if homework already exists for that specific user
    homework = session.query(Homework).filter_by(course_id=course_id, title = hw_name, duedate=due_date).first()
    if homework:
        print("Homework already exists for this course.")
        return False
    
    new_homework = Homework(title = hw_name, duedate=due_date, course_id=course_id)

    session.add(new_homework)
    session.commit()
    session.close()
    return True

def remove_homework(course_id, hw_name):
    homework = session.query(Homework).filter_by(course_id=course_id, title = hw_name).first()
    if homework:
        session.delete(homework)
        session.commit()
    session.close()

def add_quiz(course_id, quiz_name, due_date):
    course = session.query(Course).filter_by(id=course_id).first()
    if not course:
        print("Course doesn't exist.")
        return False
    
    quiz = session.query(Quiz).filter_by(course_id=course_id, title = quiz_name, duedate=due_date).first()
    if quiz:
        print("Quiz already exists for this course.")
        return False
    
    new_quiz = Quiz(title = quiz_name, duedate=due_date, course_id=course_id)

    session.add(new_quiz)
    session.commit()
    session.close()
    return True

def remove_quiz(course_id, quiz_name):
    quiz = session.query(Quiz).filter_by(course_id=course_id, title = quiz_name).first()
    if quiz:
        session.delete(quiz)
        session.commit()
        session.close()
    else:
        print("Quiz does not exist")

################################################## Server side ##################################################
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json
        
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # #Check if username or email is taken
        # for user in users:
        #     if user.username == username:
        #         return jsonify('Username already exists')
        #     if user.email == email:
        #         return jsonify('Email already exists')

        # #Check if password is valid (above 6 charcaters)
        # if (len(password) < 6):
        #     return jsonify('Password invalid, need to be at least 6 characters')

        # #Check if email is valid
        # pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        # # Use re.match to check if the email matches the pattern
        # if not re.match(pattern, email):
        #     return jsonify('Please input valid email')

        # # Confirm passwords match
        # if password!= confirm_password:
        #     return jsonify('Passwords do not match')

        user = User(email=email, username=username, password=password)
        session.add(user)
        session.commit()
        for user in users:
            print(user.username)
        return jsonify("Account created successfully")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            # Store user information in a session
            user_id = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/get_lists')
def get_lists():
    return jsonify(course_list)


@app.route('/')
def home():
    return render_template('landingpage.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')


@app.route('/add_course', methods=["POST"])
def user_add_course():
    course_name = request.form['new_course']
    result = add_course(user_id, course_name)
    if result:
        return "Success"
    else:
        return "Failure to add course"
    

    
## Parse through every user in the database and display their course, homework, and quiz
## Done with ChatGPT because I was too lazy to code it. Use only for reference and in understanding the database
@app.route('/database')
def database():
    user_course_info = {}

    for user in users:
        user_courses = []
        courses = session.query(Course).filter_by(user_id=user.id).all()
        for course in courses:
            course_info = {
                "coursename": course.coursename,
                "course_id": course.id,
                "homeworks": [],
                "quizzes": []
            }
            homeworks = session.query(Homework).filter_by(course_id=course.id).all()
            for homework in homeworks:
                course_info["homeworks"].append({
                    "title": homework.title,
                    "duedate": homework.duedate
                })
            quizzes = session.query(Quiz).filter_by(course_id=course.id).all()
            for quiz in quizzes:
                course_info["quizzes"].append({
                    "title": quiz.title,
                    "date": quiz.date
                })
            course_info["homeworks"] = course_info["homeworks"]
            course_info["quizzes"] = course_info["quizzes"]
            user_courses.append(course_info)
        user_course_info[user.username] = user_courses
    return jsonify(user_course_info)

if __name__ == '__main__':
    app.run(debug=True)