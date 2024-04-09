from flask import Flask,jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from tables import Base, User, Course, Homework, Quiz
import os
import re

app = Flask(__name__)
CORS(app)

directory = 'backend'
db_filename = 'User.db'
db_path = f"{os.path.join(os.getcwd(), directory, db_filename)}"

# Create an engine object to connect to the SQLite database
engine = create_engine(f"sqlite:///{db_path}")

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Query the data
users = session.query(User).all()
courses = session.query(Course).all()
homeworks = session.query(Homework).all()
quizzes = session.query(Quiz).all()

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

# Given the user-input username and password, check to see if it's inside of the database. If true, then return True,  otherwise return False
def login(username, password):
    for user in users:
        if user.username == username and user.password == password:
            return True
    return False

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

    # Add course to course_list
    # course_list[course_name] = {"homework":[],"quizzes/tests":[]}

    return True

# Given the user's ID and the course name, remove the course from the specified user's table
def remove_course(user_id, course_name):
    course = session.query(Course).filter_by(user_id=user_id, coursename = course_name).first()
    if course:

        # Delete the new course to the database and commit changes
        session.delete(course)
        session.commit()
    session.close()

    # Remove from course_list
    # course_list.pop(course_name)

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

#Server side
@app.route('/get_lists')
def get_lists():
    return jsonify(course_list)

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