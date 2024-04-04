from flask import Flask, render_template,jsonify, request
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







