from flask import Flask, render_template,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
def index():
    # remove_homework("phys_2111", "14.1")
    # print(course_list)

    # remove_quiz("phys_2111", "Exam 1")
    # print(course_list)

    return jsonify(course_list)

# @app.route('/change_list', METHODS=["POST"])
# def index():
#     add_course("Course Name from Request")


if __name__ == '__main__':
    app.run(debug=True)







