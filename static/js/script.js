var coursework = {};
var created_content = new Map();
var top_course = "";
var next_course = "";

function call(){
    fetch('http://127.0.0.1:5000/grab_user_info')
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        coursework = data;
        console.log(coursework);
        display_lists(coursework);
        create_initial_content(coursework);

    })
    .catch(function (error) {
        console.log('Error:', error);
    });
}

function display_lists(coursework){
    document.getElementById('lists').innerHTML = '';
    var courses = coursework["1"]

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
    // If the course I clicked is already on, do nothing
    // If the course I clicked isn't already on 
    //      If it hasn't been created, hide current content and create it
    //      If it has been created, hide current content and show it

    var courseName = coursework["1"][e.target.id].coursename; // Get the name of the course
    next_course = courseName;
    console.log("Top Course: " + top_course);
    console.log("Next Course: " + next_course);

    if (top_course != next_course){
        if (created_content.has(next_course)) {
            var top_course_content = created_content.get(top_course); // Retrieve the course content from the Map
            console.log(top_course)
            var next_course_content = created_content.get(next_course); // Retrieve the course content from the Map
            top_course_content.style.display = "none"; // Show the course content
            next_course_content.style.display = "block"; // Show the course content
            console.log(created_content);
            top_course = next_course;
            
        } else {
            var top_course_content = created_content.get(top_course); // Retrieve the course content from the Map
            top_course_content.style.display = "none"; // Show the course content
            create_content(coursework["1"][e.target.id]); // Create the course content
            top_course = next_course;
        }
    }
}

// function display_sublists(e){
//     if(e.target.isClicked == null){
//         for (var key in coursework[e.target.id]){
//             // Create a new list item element'
//             var new_div = document.createElement('div');
//             var new_butt = document.createElement('button');
//             new_butt.innerHTML = "V";
//             new_butt.id = key;
//             new_butt.onclick = display_sublists;
//             var new_li = document.createElement('li');
//             new_li.innerHTML = key;

//             new_div.className = "folder_list_item";
//             new_div.appendChild(new_butt);
//             new_div.appendChild(new_li);

//             e.target.parentNode.appendChild(new_div);
//         }
//         e.target.isClicked = true;
//         console.log("Creating sublists");
//     }
//     else if(e.target.isClicked){
//         e.target.parentNode.childNodes.forEach(function(child){
//             if(child.className == "folder_list_item"){
//                 child.style.display = "none";
//             }
//         });
//         e.target.isClicked = false;
//         console.log("Hiding sublists");
//     }
//     else if(!e.target.isClicked){
//         e.target.parentNode.childNodes.forEach(function(child){
//             if(child.className == "folder_list_item"){
//                 child.style.display = "block";
//             }
//         });
//         e.target.isClicked = true;
//         console.log("Showing sublists");
//     }
// }

// Displays the content of the dictionary
function create_initial_content(coursework){
    // Create the header(s)
    var current_course = coursework["1"][1]
    document.getElementById('content_header').innerHTML = current_course.coursename;
    document.getElementById('content').innerHTML = '';

    var course_div = document.createElement("div");
    course_div.id = "course_content";
    

    var hw_head_div = document.createElement("div");
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
        var hw_header = document.createElement("p");
        var hw_date = document.createElement("p");

        hw_header.innerHTML = current_homework.title;
        hw_date.innerHTML = current_homework.duedate;

        hw_div.appendChild(hw_header);
        hw_div.appendChild(hw_date);

        hw_head_div.appendChild(hw_div);
    }

    var exam_head_div = document.createElement("div");
    var exam_head = document.createElement("h2");

    exam_head.innerHTML = "Exams/Quizzes";
    exam_head_div.appendChild(exam_head);

    course_div.appendChild(exam_head_div);

    // Create the homework content for the course
    for (var i = 0; i < current_course.quizzes.length; i++){
        // Get the current homework
        var current_exam = current_course.quizzes[i];

        // Create the div for the homework
        var exam_div = document.createElement("div");
        var exam_header = document.createElement("p");
        var exam_date = document.createElement("p");

        exam_header.innerHTML = current_exam.title;
        exam_date.innerHTML = current_exam.date;

        exam_div.appendChild(exam_header);
        exam_div.appendChild(exam_date);

        exam_head_div.appendChild(exam_div);
    }
    document.getElementById('content').appendChild(course_div);
    created_content.set(current_course.coursename, course_div);
    top_course = current_course.coursename;
    //exam_head_div.style.display = "none";
}

function create_content(current_course){
    // Create the header(s)
    document.getElementById('content_header').innerHTML = current_course.coursename;
    document.getElementById('content').innerHTML = '';

    var course_div = document.createElement("div");
    course_div.id = "course_content";
    

    var hw_head_div = document.createElement("div");
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
        var hw_header = document.createElement("p");
        var hw_date = document.createElement("p");

        hw_header.innerHTML = current_homework.title;
        hw_date.innerHTML = current_homework.duedate;

        hw_div.appendChild(hw_header);
        hw_div.appendChild(hw_date);

        hw_head_div.appendChild(hw_div);
    }

    var exam_head_div = document.createElement("div");
    var exam_head = document.createElement("h2");

    exam_head.innerHTML = "Exams/Quizzes";
    exam_head_div.appendChild(exam_head);

    course_div.appendChild(exam_head_div);

    // Create the homework content for the course
    for (var i = 0; i < current_course.quizzes.length; i++){
        // Get the current homework
        var current_exam = current_course.quizzes[i];

        // Create the div for the homework
        var exam_div = document.createElement("div");
        var exam_header = document.createElement("p");
        var exam_date = document.createElement("p");

        exam_header.innerHTML = current_exam.title;
        exam_date.innerHTML = current_exam.date;

        exam_div.appendChild(exam_header);
        exam_div.appendChild(exam_date);

        exam_head_div.appendChild(exam_div);
    }
    document.getElementById('content').appendChild(course_div);
    created_content.set(current_course.coursename, course_div);
    //exam_head_div.style.display = "none";
}

function add_course(){
    json_course = {
        "action": "add_course",
        "course_name": new_course
    }
    send_post_request(json_course)
}

function add_homework(){
    console.log("Adding homework");
    new_homework = document.getElementById("new_homework").value;
    new_date = document.getElementById("new_date").value;

    json_homework = {
        "action": "add_homework",
        "course_name": "phys_2111",
        "hw_name": new_homework,
        "date": new_date
    }
    send_post_request(json_homework)
}

function add_exam(){
    console.log("Adding Exam");
    new_exam = document.getElementById("new_exam").value;
    new_examdate= document.getElementById("new_examdate").value;

    json_exam ={
        "action": "add_exam",
        "course_name": "phys_2111",
        "ex_name": new_exam,
        "ex_date": new_examdate
    }
    send_post_request(json_exam)
}

function send_post_request(data){
    fetch('http://127.0.0.1:5000/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        display_lists(data);
    })
}

function goHome(){
    window.location.href = "/templates/landingpage.html";
}