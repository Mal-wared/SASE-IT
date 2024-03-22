from flask import Flask, render_template,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# dictionary that holds task information
coursework_list = {
    "coursework_list":{
        "phys 1441":{
            "assessments":
                ["14.1","14.2","14.3","14 Exam"],
            "homework":
                ["14.1 Linear","14.2 Alternative","14.3 meme"]
        },
        "phys 1442":{
            "assessments":
                ["14,1","14,2"],
            "homework":
                ["15.2","15.3"],
        }
    }   
}


def add_list(title):
    coursework_list[title]={}

def add_sublist(title, subtitle ):
    coursework_list[title][subtitle]={}

def add_tasklist(title,subtitle,task_list):
    coursework_list[title][subtitle][task_list]=[]

def add_task(title,subtitle,task_list,task):
    coursework_list[title][subtitle][task_list].append(task)

#Server side
@app.route('/get_lists')
def index():
    return jsonify(coursework_list)

if __name__ == '__main__':
    app.run(debug=True)







