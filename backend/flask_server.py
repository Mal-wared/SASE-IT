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

# Given the user's ID and the course name, remove the course from the specified user's table
def remove_course(user_id, course_name):
    course = session.query(Course).filter_by(user_id=user_id, coursename = course_name).first()
    if course:
        # Delete the new course to the database and commit changes
        session.delete(course)
        session.commit()
    session.close()

# Given the course ID and the homework name, add the homework under the specified course table
def add_homework(course_id, course_name, hw_name, due_date):
    # Check if the homework exists
    course = session.query(Course).filter_by(id=course_id).first()
    if not course:
        print("Course doesn't exist.")
        return False
    
    # Check if homework already exists for that specific user
    homework = session.query(Homework).filter_by(course_id=course_id, title = hw_name, duedate=due_date).first()
    if homework:
        print("Homework already exists for this course.")
        return False
    
    # Create a new Homework object
    new_homework = Homework(title = hw_name, duedate=due_date, course_id=course_id)

    # Add and commit the new course to the database, and close the session
    session.add(new_homework)
    session.commit()
    session.close()

    # Add course to course_list
    course_list[course_name] = {"homework":[],"quizzes/tests":[]}

    return True

    # course_list[course_name]["homework"].append({"name":hw, "date":date})

# Given the course ID and the homework name, remove the homework under the specified course table
def remove_homework(course_id, course_name, hw_name):
    homework = session.query(Homework).filter_by(course_id=course_id, title = hw_name).first()
    if homework:

        # Delete the homework from the database and commit changes
        session.delete(homework)
        session.commit()
    session.close()

    # for assignment in course_list[course_name]["homework"]:
    #     if assignment["name"] == hw:
    #         course_list[course_name]["homework"].remove(assignment)

# Given the course ID and the quiz name, add the quiz under the specified course table
def add_quiz(course_id, course_name, quiz_name, due_date):

    # Check if the course exists
    course = session.query(Course).filter_by(id=course_id).first()
    if not course:
        print("Course doesn't exist.")
        return False
    
    # Check if homework already exists for that specific user
    quiz = session.query(Quiz).filter_by(course_id=course_id, title = quiz_name, duedate=due_date).first()
    if quiz:
        print("Quiz already exists for this course.")
        return False
    
    # Create a new Quiz object
    new_quiz = Quiz(title = quiz_name, duedate=due_date, course_id=course_id)

    # Add and commit the new quiz to the database, and close the session
    session.add(new_quiz)
    session.commit()
    session.close()

    # Add course to course_list
    #course_list[course_name]["quizzes/tests"].append({"Exam":quiz_name, "date":due_date})

    return True

# Given the course ID and the quiz name, remove the quiz under the specified course table
def remove_quiz(course_id, course_name, quiz_name):
    quiz = session.query(Quiz).filter_by(course_id=course_id, title = quiz_name).first()
    if quiz:

        # Delete the quiz from the database and commit changes
        session.delete(quiz)
        session.commit()
    session.close()

    # for quiz in course_list[course_name]["quizzes/tests"]:
    #     if quiz["Exam"] == quiz_name:
    #         course_list[course_name]["quizzes/tests"].remove(quiz)
    # print(course_list)

################################################## Server side ##################################################
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        #Check if username is taken
        for user in users:
            if user.username == username:
                flash('Username already exists')
                return redirect(url_for('signup'))

        #Check if password is valid (above 6 charcaters)
        if (len(password) < 6):
            flash('Password invalid, need to be at least 6 characters')
            return redirect(url_for('signup'))

        #Check if email is valid
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        # Use re.match to check if the email matches the pattern
        if not re.match(pattern, email):
            flash('Please input valid email')
            return redirect(url_for('signup'))

        # Confirm passwords match
        if password!= confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('signup'))

        user = User(email=email, username=username, password=password)
        session.add(user)
        session.commit()

        flash('Account created successfully')
        return redirect(url_for('login'))

    return render_template('signup.html')


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

@app.route('/grab_user_info')
def get_user_info():
    user_id = 1
    user_course_info = {}

    user_courses = []
    courses = session.query(Course).filter_by(user_id=user_id).all()
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
    user_course_info[user_id] = user_courses
    return jsonify(user_course_info)


course_list_needed = [
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

################################################## Server side ##################################################


# NOTE: This function below is for manually checking a login (WONT BE ACCESSIBLE TO USERS) 
def login(username, password):
    for user in users:
        if user.username == username and user.password == password:
            return True
    return False

# NOTE: This function below is for manually signing up (WONT BE ACCESSIBLE TO USERS) 
def signup(new_username, new_password, new_email):

    #Check if username is taken
    for user in users:
        if user.username == new_username:
            print("Username already exists")
            return False
    
    #Check if password is valid (above 6 charcaters)
    if (len(new_password) < 6):
        print("Password invalid, need to be at least 6 characters")
        return False

    #Check if email is valid (Chatgpt)
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    # Use re.match to check if the email matches the pattern
    if not re.match(pattern, new_email):
        print("Please input valid email")
        return False

    #Open session with database
    new_user = User(username = new_username, password=new_password, email = new_email)
    #Add to database
    session.add(new_user)
    #Commit to database
    session.commit()
    #Close database
    session.close()






add_course(1, "Object-Oriented Programming")




if __name__ == '__main__':
    app.run(debug=True)