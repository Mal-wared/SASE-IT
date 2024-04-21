var current_user = localStorage.getItem('current_user');
console.log(current_user)
var coursework = {};
var created_content = new Map();
var top_course = "";
var next_course = "";
var current_course_name = localStorage.getItem('current_course')
console.log(`Current course:${current_course_name}`)

function getUserData(){
    data = {"current_user": current_user}
    send_post_request(data, '/get_user').then(response =>
        {
        console.log(response)
        if(response['course_list']){
            coursework = response['course_list'];
            display_lists(coursework);
            create_initial_content(coursework);
            console.log(coursework);
        }
        else{
            console.log("No user found")
    }})
}

function display_lists(coursework){
    document.getElementById('lists').innerHTML = '';
    console.log(coursework)
    var courses = coursework

    // Display the data on client
    for (var i = 0; i < courses.length; i++){
        // Create a new list item element
        var new_div = document.createElement('div');

        var new_butt = document.createElement('button');

        new_butt.innerHTML = "V";
        new_butt.id = i;
        
        new_butt.onclick = display_course;

        var new_li = document.createElement('li');
        new_li.innerHTML = courses[i].coursename;
        console.log(courses[i].coursename)

        new_div.className = "list_item";
        new_div.appendChild(new_butt);
        new_div.appendChild(new_li);


        document.getElementById('lists').appendChild(new_div);
    }
}

function display_course(e){
    var courseName = coursework[e.target.id].coursename; // Get the name of the course
    localStorage.setItem('current_course',courseName)
    current_course_name = courseName;
    console.log(`Current course set to :${current_course_name}`)

    next_course = courseName;
    console.log("Top Course: " + top_course);
    console.log("Next Course: " + next_course);

    var top_course_content = created_content.get(top_course);
    var next_course_content = created_content.get(next_course);


    if (top_course != next_course){
        if (created_content.has(next_course)) {
            top_course_content.style.display = "none"; // Show the course content
            document.getElementById('content_header').innerHTML = next_course;
            next_course_content.style.display = "block"; // Show the course content
            console.log(created_content);
            top_course = next_course;
        } else if (created_content.has(top_course)) {
             // Retrieve the course content from the Map
            top_course_content.style.display = "none"; // Show the course content
            create_content(coursework[e.target.id]); // Create the course content
            top_course = next_course;
        }
        else{
            create_content(coursework[e.target.id]); // Create the course content
            top_course = next_course;
        }
    }
}

// Displays the content of the dictionary
function create_initial_content(coursework){
    if (current_course_name == ""){
        var current_course = coursework[0]
    }
    else{
        for(var i = 0; i < coursework.length; i++){
            //console.log(coursework[i])
            if (coursework[i].coursename == current_course_name){
                var current_course = coursework[i]
            }
        }
    }
    // Create the header(s)
    document.getElementById('content_header').innerHTML = current_course.coursename;
    document.getElementById('content').innerHTML = '';

    var course_div = document.createElement("div");
    course_div.className = "course_div"
    course_div.id = "course_content";
    

    var hw_head_div = document.createElement("div");
    hw_head_div.className = "hw_head_div";
    var hw_head = document.createElement("h2");

    hw_head.innerHTML = "Homework";
    hw_head_div.appendChild(hw_head);

    course_div.appendChild(hw_head_div);

    // Create the homework content for the course
    for (var i = 0; i < current_course.homeworks.length; i++){
        // Get the current homework
        var current_homework = current_course.homeworks[i];

        // Create the div for the homework
        var hw_div = document.createElement("div");
        var hw_checkbox = document.createElement("input");
        hw_checkbox.type = "checkbox";
        hw_checkbox.className = "hw_checkbox";
        hw_div.appendChild(hw_checkbox);

        var hw_header = document.createElement("p");
        hw_header.className = "hw_header";
        

        var hw_date = document.createElement("p");
        hw_date.className = "hw_date";

        var trash_icon = document.createElement("img");
        trash_icon.className = "trash_icon";
        trash_icon.src = "../static/images/trash.png";

        var delete_butt = document.createElement('button');
        delete_butt.appendChild(trash_icon);
        delete_butt.onclick = delete_homework
        delete_butt.className = "delete_butt";
        delete_butt.id = current_course.homeworks[i].id;

        hw_header.innerHTML = current_homework.title;
        hw_date.innerHTML = current_homework.duedate;

        hw_div.className = "listing"; 
        hw_div.appendChild(hw_checkbox);
        hw_div.appendChild(hw_header);
        hw_div.appendChild(hw_date);
        hw_div.appendChild(delete_butt);

        hw_head_div.appendChild(hw_div);
    }

    var homeworkInput = document.createElement("input");
    var dateInput = document.createElement("input");
    var addButton = document.createElement("button");

    homeworkInput.id = "new_homework";
    homeworkInput.type = "text";
    homeworkInput.placeholder = "Homework Name";
    dateInput.id = "new_date";
    dateInput.type = "text";
    dateInput.placeholder = "Due Date";
    addButton.textContent = "ADD";
    addButton.onclick = add_homework;

    hw_head_div.appendChild(homeworkInput);
    hw_head_div.appendChild(dateInput);
    hw_head_div.appendChild(addButton);

    var exam_head_div = document.createElement("div");
    exam_head_div.className = "exam_head_div";

    var exam_head = document.createElement("h2");
    exam_head.className = "exam_head";

    exam_head.innerHTML = "Exams/Quizzes";
    exam_head_div.appendChild(exam_head);

    course_div.appendChild(exam_head_div);

    // Create the homework content for the course
    for (var i = 0; i < current_course.quizzes.length; i++){
        
        // Get the current homework
        var current_exam = current_course.quizzes[i];

        // Create the div for the homework
        var exam_div = document.createElement("div");
        var exam_checkbox = document.createElement("input");
        exam_checkbox.className = "hw_checkbox";
        exam_checkbox.type = "checkbox";
        exam_div.appendChild(exam_checkbox);
        var exam_header = document.createElement("p");
        exam_header.className = "hw_header";

        var exam_date = document.createElement("p");
        exam_date.className = "hw_date";

        var trash_icon = document.createElement("img");
        trash_icon.className = "trash_icon";
        trash_icon.src = "../static/images/trash.png";

        var delete_butt = document.createElement('button');
        delete_butt.appendChild(trash_icon);
        delete_butt.onclick = delete_quiz
        delete_butt.className = "delete_butt";
        delete_butt.id = current_course.quizzes[i].id;
        

        exam_header.innerHTML = current_exam.title;
        exam_date.innerHTML = current_exam.date;
        exam_div.className = "listing"; 
        exam_div.appendChild(exam_checkbox);
        exam_div.appendChild(exam_header);
        exam_div.appendChild(exam_date);
        exam_div.appendChild(delete_butt);

        exam_head_div.appendChild(exam_div);

    }
    // Create input elements for quizzes
    var quizInput = document.createElement("input");
    var quizDateInput = document.createElement("input");
    var addQuizButton = document.createElement("button");

    // Set attributes for input elements
    quizInput.id = "new_quiz";
    quizInput.type = "text";
    quizInput.placeholder = "Exam Name";
    quizDateInput.id = "new_quiz_date";
    quizDateInput.type = "text";
    quizDateInput.placeholder = "Due Date";
    addQuizButton.textContent = "ADD";
    addQuizButton.onclick = add_quiz;

    exam_head_div.appendChild(quizInput);
    exam_head_div.appendChild(quizDateInput);
    exam_head_div.appendChild(addQuizButton);

    document.getElementById('content').appendChild(course_div);
    created_content.set(current_course.coursename, course_div);
    top_course = current_course.coursename;
    //exam_head_div.style.display = "none";
}

function create_content(current_course){
    // Create the header(s)
    document.getElementById('content_header').innerHTML = current_course.coursename;

    var course_div = document.createElement("div");
    course_div.className = "course_div"
    course_div.id = "course_content";
    

    var hw_head_div = document.createElement("div");
    hw_head_div.className = "hw_head_div";
    var hw_head = document.createElement("h2");

    hw_head.innerHTML = "Homework";
    hw_head_div.appendChild(hw_head);

    course_div.appendChild(hw_head_div);

    // Create the homework content for the course
    for (var i = 0; i < current_course.homeworks.length; i++){
        // Get the current homework
        var current_homework = current_course.homeworks[i];

        // Create the div for the homework
        var hw_div = document.createElement("div");
        var hw_checkbox = document.createElement("input");
        hw_checkbox.className = "hw_checkbox";
        hw_checkbox.type = "checkbox";
        hw_div.appendChild(hw_checkbox);
        var hw_header = document.createElement("p");
        hw_header.className = "hw_header";
        var hw_date = document.createElement("p");
        hw_date.className = "hw_date";

        hw_header.innerHTML = current_homework.title;
        hw_date.innerHTML = current_homework.duedate;

        hw_div.className = "listing"; 

        var trash_icon = document.createElement("img");
        trash_icon.className = "trash_icon";
        trash_icon.src = "../static/images/trash.png";

        var delete_butt = document.createElement('button');
        delete_butt.appendChild(trash_icon);
        delete_butt.onclick = delete_homework
        delete_butt.className = "delete_butt";
        delete_butt.id = current_course.homeworks[i].id;

        hw_div.appendChild(hw_header);
        hw_div.appendChild(hw_date);
        hw_div.appendChild(delete_butt);

        hw_head_div.appendChild(hw_div);
    }

    var homeworkInput = document.createElement("input");
    var dateInput = document.createElement("input");
    var addButton = document.createElement("button");

    homeworkInput.id = "new_homework";
    homeworkInput.type = "text";
    homeworkInput.placeholder = "Homework Name";
    dateInput.id = "new_date";
    dateInput.type = "text";
    dateInput.placeholder = "Due Date";
    addButton.textContent = "ADD";
    addButton.onclick = add_homework;

    hw_head_div.appendChild(homeworkInput);
    hw_head_div.appendChild(dateInput);
    hw_head_div.appendChild(addButton);

    var exam_head_div = document.createElement("div");
    exam_head_div.className = "exam_head_div";
    var exam_head = document.createElement("h2");
    exam_head.className = "exam_head";

    exam_head.innerHTML = "Exams/Quizzes";
    exam_head_div.appendChild(exam_head);

    course_div.appendChild(exam_head_div);

    // Create the homework content for the course
    for (var i = 0; i < current_course.quizzes.length; i++){
        // Get the current homework
        var current_exam = current_course.quizzes[i];

        // Create the div for the homework
        var exam_div = document.createElement("div");
        var exam_checkbox = document.createElement("input");
        exam_checkbox.className = "exam_checkbox"
        exam_checkbox.type = "checkbox";
        exam_div.appendChild(exam_checkbox);
        var exam_header = document.createElement("p");
        exam_header.className = "hw_header";
        var exam_date = document.createElement("p");
        exam_date.className = "hw_date";


        exam_header.innerHTML = current_exam.title;
        exam_date.innerHTML = current_exam.date;
        exam_div.className = "listing"; 

        var trash_icon = document.createElement("img");
        trash_icon.className = "trash_icon";
        trash_icon.src = "../static/images/trash.png";

        var delete_butt = document.createElement('button');
        delete_butt.appendChild(trash_icon);
        delete_butt.onclick = delete_quiz
        delete_butt.className = "delete_butt";
        delete_butt.id = current_course.quizzes[i].id;
        
        exam_div.appendChild(exam_header);
        exam_div.appendChild(exam_date);
        exam_div.appendChild(delete_butt);

        exam_head_div.appendChild(exam_div);
    }
    // Create input elements for quizzes
    var quizInput = document.createElement("input");
    var quizDateInput = document.createElement("input");
    var addQuizButton = document.createElement("button");

    // Set attributes for input elements
    quizInput.id = "new_quiz";
    quizInput.type = "text";
    quizInput.placeholder = "Exam Name";
    quizDateInput.id = "new_quiz_date";
    quizDateInput.type = "text";
    quizDateInput.placeholder = "Due Date";
    addQuizButton.textContent = "ADD";
    addQuizButton.onclick = add_quiz;

    exam_head_div.appendChild(quizInput);
    exam_head_div.appendChild(quizDateInput);
    exam_head_div.appendChild(addQuizButton);
    document.getElementById('content').appendChild(course_div);
    created_content.set(current_course.coursename, course_div);
    //exam_head_div.style.display = "none";
}

function add_course(){
    var new_course = document.getElementById("new_course").value;
    json_course = {
        "action": "add_course",
        "course_name": new_course,
        "username": current_user
    }
    send_post_request(json_course, "add_course").then(response=>
    {
        console.log(response);
        window.location.reload();
    })
}

function add_homework(){
    console.log("Adding homework");
    new_homework = document.getElementById("new_homework").value;
    new_date = document.getElementById("new_date").value;
    if (new_date === "" || new_homework === "") {
        console.log("empty hw or date")
        return;
    }
    else {
        json_homework = {
            "action": "add_homework",
            "course_name": current_course_name,
            "hw_name": new_homework,
            "date": new_date,
            "username": current_user
        }
        send_post_request(json_homework,"add_homework").then(response=>{    
            console.log(response);
            window.location.reload();
        })
    }
}

function delete_homework(e){
    console.log("Deleting homework");
    var homework_id_to_delete = e.target.id;
    console.log("hw to delete: " + homework_id_to_delete);
    json_homework = {
        "action": "delete_homework",
        "course_name": current_course_name,
        "hw_id": homework_id_to_delete,
        "username": current_user
    }
    send_post_request(json_homework,"delete_homework").then(response=>{    
        console.log(response);
        window.location.reload();
    })
}

function delete_quiz(e){
    console.log("Deleting quiz");
    var quiz_id_to_delete = e.target.id;
    json_quiz = {
        "action": "delete_quiz",
        "course_name": current_course_name,
        "quiz_id": quiz_id_to_delete,
        "username": current_user
    }
    send_post_request(json_quiz,"delete_quiz").then(response=>{    
        console.log(response);
        window.location.reload();
    })
}

function add_quiz(){
    console.log("Adding Quiz");
    new_quiz = document.getElementById("new_quiz").value;
    new_quiz_date= document.getElementById("new_quiz_date").value;
    if (new_quiz_date === "" || new_quiz === "") {
        console.log("empty quiz/exam or date")
        return;
    }
    else {
        json_quiz ={
            "action": "add_quiz",
            "course_name": current_course_name,
            "quiz_name": new_quiz,
            "quiz_date": new_quiz_date,
            "username": current_user
        }
        send_post_request(json_quiz,"add_quiz").then(response=>{    
            console.log(response);
            window.location.reload();
        })
    }
    
}

function send_post_request(data, url){
    return fetch(`https://dannyle1237.pythonanywhere.com/${url}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
}

function goPage(url){
    window.location.href = `/templates/${url}`;
}

function check_user(){
    console.log("Checking user")
    var storedUser = localStorage.getItem('current_user'); // Retrieve current_user from localStorage
    console.log(`Current user: ${storedUser}`)
    var nav = document.querySelector('nav');
    if(storedUser){
        console.log("Deleting")
        var loginAnchor = document.getElementById('LOGIN');
        var signupAnchor = document.getElementById('SIGNUP');

        if (loginAnchor) {
            loginAnchor.parentNode.removeChild(loginAnchor);
        }

        if (signupAnchor) { 
            signupAnchor.parentNode.removeChild(signupAnchor);
        getUserData(current_user);
        }

        var signOut = document.createElement('a');
        signOut.textContent = 'SIGN OUT';
        signOut.addEventListener('click', function() {
            localStorage.setItem('current_user', ''); 
            console.log('User signed out');
            goPage("signup.html")
        });
        nav.appendChild(signOut);  

        var user = document.createElement('p');
        user.textContent = `${current_user}`;
        nav.appendChild(user);  
    }
    else{
        var loginAnchor = document.getElementById('LOGIN');
        var signupAnchor = document.getElementById('SIGNUP');
        if(!loginAnchor){
            var newLoginAnchor = document.createElement('a');
            newLoginAnchor.setAttribute('href', '/templates\\login.html');
            newLoginAnchor.textContent = 'LOGIN';
            nav.appendChild(newLoginAnchor);
        }
        if(!signupAnchor){
            var newSignupAnchor = document.createElement('a');
            newSignupAnchor.setAttribute('href', '/templates\\signup.html');
            newSignupAnchor.textContent = 'SIGN UP';
            nav.appendChild(newSignupAnchor);
        }
    }
}

document.addEventListener("DOMContentLoaded", function() {
    check_user();
}); 