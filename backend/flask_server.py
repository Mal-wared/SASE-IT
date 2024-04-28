from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_cors import CORS
from sqlalchemy import create_engine, MetaData, Table
from flask_sqlalchemy import SQLAlchemy
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
engine = create_engine(f"sqlite:///{db_path}", echo=True, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()


users = session.query(User).all()
courses = session.query(Course).all()
homeworks = session.query(Homework).all()
quizzes = session.query(Quiz).all()

print('\n\nUSERS\n2 ')
for user in users:
    print(f'id: {user.id} Username: {user.username} pass: {user.password}')

user_id = ''

course_list = [
    {
        "coursename": "Physics 2111", 
        "course_id": "1", 
        "homeworks": [{"title": "14.1 linear systems", "duedate": "2-14-24"}, 
                      {"title": "14.2 linear combinations", "duedate": "2-18-24"}], 
        "quizzes": [{"title": "Exam 1", "date": "2-20-24"}, 
                    {"title": "Exam 2", "date": "2-25-24"}]
    },
    {
        "coursename": "Physics 2222",
        "course_id": "2",
        "homeworks": [{"title": "17.2 line integrals", "duedate": "2-16-24"},
                      {"title": "17.3 conservative vector fields", "duedate": "2-23-24"}],
        "quizzes": [{"title": "Exam 1", "date": "3-30-24"},
                    {"title": "Exam 2", "date": "4-01-24"}]
    }
]



# Given the user's ID and the course name, add the course under the specified user's table
def add_course(username, course_name):
    users = session.query(User).all()
    courses = session.query(Course).all()
    print(f'\n\nThe username is {username} and the coursename:{course_name}')
    # Check if the user exists
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print("User doesn't exist.")
        return False

    # Check if course already exists for that specific user
    course = session.query(Course).filter_by(user_id=user.id, coursename=course_name).first()
    if course:
        print("Course already exists for this user.")
        return False
    
    # Create a new Course object
    new_course = Course(coursename=course_name, user_id=user.id)

    # Add and commit the new course to the database, and close the session
    session.add(new_course)
    session.commit()
    session.close()
    for course in courses:
        print(f'id:{course.id} coursename:{course.coursename}')
    return True

def remove_course(user_id, course_name):
    course = session.query(Course).filter_by(user_id=user_id, coursename = course_name).first()
    if course:
        session.delete(course)
        session.commit()
    session.close()

def add_homework(username, course_name, hw_name, due_date):
    user = session.query(User).filter_by(username = username).first()
    if not user:
        print("user doesnt exist")
        return False
    user_id = user.id
    course = session.query(Course).filter_by(user_id=user_id, coursename=course_name).first()
    if not course:
        print("Course doesn't exist.")
        return False
    new_homework = Homework(title = hw_name, duedate=due_date, course_id=course.id)

    session.add(new_homework)
    session.commit()
    session.close()
    return True

def delete_homework(username, course_name, hw_id):
    user = session.query(User).filter_by(username = username).first()
    if not user:
        print("user doesnt exist")
        return False
    user_id = user.id
    course = session.query(Course).filter_by(user_id=user_id, coursename=course_name).first()
    if not course:
        print("Course doesn't exist.")
        return False
    print(f'\n\nCourseid:{course.id} hw_id:{hw_id}')
    homework = session.query(Homework).filter_by(course_id=course.id, id=hw_id).first()
    if not homework:
        print("Homework doesn't exist.")
        return False
    
    session.delete(homework)
    session.commit()
    session.close()
    return True

def delete_quiz(username, course_name, quiz_id):
    user = session.query(User).filter_by(username = username).first()
    if not user:
        print("user doesnt exist")
        return False
    user_id = user.id
    course = session.query(Course).filter_by(user_id=user_id, coursename=course_name).first()
    if not course:
        print("Course doesn't exist.")
        return False
    print(f'\n\nCourseid:{course.id} quiz_id:{quiz_id}')
    quiz = session.query(Quiz).filter_by(course_id=course.id, id=quiz_id).first()
    if not quiz:
        print("Quiz doesn't exist.")
        return False

    session.delete(quiz)
    session.commit()
    session.close()
    return True

def remove_homework(course_id, hw_name):
    homework = session.query(Homework).filter_by(course_id=course_id, title = hw_name).first()
    if homework:
        session.delete(homework)
        session.commit()
    session.close()

def add_quiz(username, course_name, quiz_name, quiz_date):
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print("user doesn't exist.")
        return False
    user_id=user.id
    course = session.query(Course).filter_by(user_id=user_id, coursename=course_name).first()
    if not course:
        print("Course doesn't exist.")
        return False
    new_quiz = Quiz(title = quiz_name, date=quiz_date, course_id=course.id)

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
        print(f'User data = {data}')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        users = session.query(User).all()

        #Check if username or email is taken
        for user in users:
            if user.username == username:
                return jsonify('Username already exists')
            if user.email == email:
                return jsonify('Email already exists')

        #Check if password is valid (above 6 charcaters)
        if (len(password) < 6):
            return jsonify('Password invalid, need to be at least 6 characters')

        #Check if email is valid
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        # Use re.match to check if the email matches the pattern
        if not re.match(pattern, email):
            return jsonify('Please input valid email')

        # Confirm passwords match
        if password!= confirm_password:
            return jsonify('Passwords do not match')

        user = User(email=email, username=username, password=password)
        session.add(user)
        session.commit()
        users = session.query(User).all()
        print("User added successfully\n\nPrinting Users")
        for user in users:
            print(user.username)
        return jsonify("Account created successfully")
    return "ERROR"

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Attemping login")
    if request.method == 'POST':
        data = request.json
        print(f'User data = {data}')
        username = data.get('username')
        password = data.get('password')

        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            # Store user information in a session
            user_id = user.id
            print("\nLog in successful\n")
            return jsonify("Account logged in")
        else:
            print("\nLog in unsuccessful\n")
            return jsonify("User does not exist")

@app.route('/get_user', methods=['POST'])
def get_user():
    data = request.json
    username = data.get("current_user")

    print(f"\nUsername = {username}")
    users = session.query(User).all()
    courses = session.query(Course).all()
    homeworks = session.query(Homework).all()
    quizzes = session.query(Quiz).all()

    user_data = []
    for user in users:
        if user.username == username:
            user_id = user.id
            for course in courses:
                if course.user_id == user_id:
                    user_hw = []
                    user_quizzes = []
                    for homework in homeworks:
                        if homework.course_id == course.id:
                            user_hw.append({
                                "title": homework.title,
                                "duedate": homework.duedate,
                                "id": homework.id
                            })
                    for quiz in quizzes:
                        if quiz.course_id == course.id:
                            user_quizzes.append({
                                "title": quiz.title,
                                "date": quiz.date,
                                "id": quiz.id
                            })    
                    user_data.append({
                        "coursename": course.coursename,
                        "course_id": course.id,
                        "homeworks": user_hw,
                        "quizzes": user_quizzes
                    })
    print(f'\n\nUSER DATA = {user_data}')
    course_list = user_data
    return {"course_list":course_list}

@app.route('/')
def home():
    return render_template('landingpage.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')


@app.route('/add_course', methods=["POST"])
def user_add_course():
    data = request.json
    print(f'\n\nData = {data}')
    course_name = data.get('course_name')
    username = data.get('username')
    result = add_course(username, course_name)
    if result:
        return jsonify("Success")
    else:
        return jsonify("Failure to add course")
    
@app.route('/add_homework',methods= ["POST"])
def user_add_homework():
    data = request.json
    print(f'\n\nData = {data}')
    course_name=data.get('course_name')
    hw_name = data.get('hw_name')
    date = data.get('date')
    username = data.get('username')

    result = add_homework(username, course_name,hw_name,date)

    if result:
        return jsonify("Success")
    else:
        return jsonify("Failure")
    
@app.route('/delete_homework',methods= ["POST"])
def user_delete_homework():
    data = request.json
    print(f'\n\nData = {data}')
    course_name=data.get('course_name')
    hw_id = data.get('hw_id')
    username = data.get('username')

    result = delete_homework(username, course_name, hw_id)

    if result:
        return jsonify("Success")
    else:
        return jsonify("Failure")
    
@app.route('/add_quiz',methods= ["POST"])
def user_add_quiz():
    data = request.json
    print(f'\n\nData = {data}')
    course_name = data.get('course_name')
    quiz_name = data.get('quiz_name')
    quiz_date = data.get('quiz_date')
    username = data.get('username')

    result = add_quiz(username, course_name,quiz_name,quiz_date)

    if result:
        return jsonify("Success")
    else:
        return jsonify("Failure")
    
@app.route('/delete_quiz',methods= ["POST"])
def user_delete_quiz():
    data = request.json
    print(f'\n\nData = {data}')
    course_name=data.get('course_name')
    quiz_id = data.get('quiz_id')
    username = data.get('username')

    result = delete_quiz(username, course_name, quiz_id)

    if result:
        return jsonify("Success")
    else:
        return jsonify("Failure")

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
                    "duedate": homework.duedate,
                    "id": homework.id
                })
            quizzes = session.query(Quiz).filter_by(course_id=course.id).all()
            for quiz in quizzes:
                course_info["quizzes"].append({
                    "title": quiz.title,
                    "date": quiz.date,
                    "id": quiz.id
                })
            course_info["homeworks"] = course_info["homeworks"]
            course_info["quizzes"] = course_info["quizzes"]
            user_courses.append(course_info)
        user_course_info[user.username] = user_courses
    return jsonify(user_course_info)


if __name__ == '__main__':
    app.run(debug=True, port=8080)