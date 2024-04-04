from flask import Flask,jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine
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

# for user in users:
#     print(f'{user.id}:{user.username}')


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
    new_user = User(username = new_username, password=new_password, email = new_email )
    session.add(new_user)
    session.commit()
    session.close()

signup('Dan', 'djfdsfff', 'sdfljail.com')
users = session.query(User).all()
for user in users:
    print(f'{user.id}:{user.username}')

# dictionary that holds task information
course_list = {
    "phys_2111":{
        "homework":
            [{"name": "14.1","date": "02-20-2024"},{"name": "template", "date": "due date"}],
        "quizzes/tests":
            [{"Exam": "Exam 1", "Date": "due-date"}]
    },
    "phys_2222": {
        "homework":[],
        "quizzes/tests":[]
    }
}

def add_course(course_name):
    course_list[course_name] = {"homework":[],"quizzes/tests":[]}

def remove_course(course_name):
    course_list.pop(course_name)

def add_homework(course_name, hw, date):
    course_list[course_name]["homework"].append({"name":hw, "date":date})

def remove_homework(course_name, hw):
    for assignment in course_list[course_name]["homework"]:
        if assignment["name"] == hw:
            course_list[course_name]["homework"].remove(assignment)

def add_quiz(course_name, exam, date):
    course_list[course_name]["quizzes/tests"].append({"Exam":exam, "date":date})

def remove_quiz(course_name, quiz_name):
    for quiz in course_list[course_name]["quizzes/tests"]:
        if quiz["Exam"] == quiz_name:
            course_list[course_name]["quizzes/tests"].remove(quiz)
    print(course_list)

#Server side
@app.route('/get_lists')
def get_lists():
    # remove_homework("phys_2111", "14.1")
    # print(course_list)

    # remove_quiz("phys_2111", "Exam 1")
    # print(course_list)
    return jsonify(course_list)


@app.route('/add', methods=["POST"])
def add_course_url():
    data = request.json
    print(data)
    if(data["action"] == "add_course"):
        course_name = data["course_name"]
        #print(course_name)
        add_course(course_name)
    elif(data["action"] == "add_homework"):
        course_name = data["course_name"]
        new_hw = data["hw_name"]
        date = data["date"]
        add_homework(course_name, new_hw, date)
    elif(data["action"]=="add_exam"):
        course_name = data["course_name"]
        new_exam = data["ex_name"]
        exam_date = data["ex_date"]
        add_quiz(course_name,new_exam,exam_date)
    return jsonify(course_list)


if __name__ == '__main__':
    app.run(debug=True)







