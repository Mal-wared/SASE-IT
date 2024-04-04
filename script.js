var coursework = {};

function call(){
    fetch('http://127.0.0.1:5000/get_lists')
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        coursework = data;
        console.log(coursework);
        display_courses(coursework);
    })
    .catch(function (error) {
        console.log('Error:', error);
    });
}

function display_courses(coursework){
    var i = 0;
    document.getElementById('lists').innerHTML = '';
    // Display the data on client
    for (var key in coursework){
        // Create a new list item element
        var new_div = document.createElement('div');
        var new_butt = document.createElement('button');
        new_butt.innerHTML = "V";
        new_butt.id = key;
        
        // Added custom attribute to the button "isClicked"
        // isClicked is used to determine if the button has been clicked
        //          if null, create sublists
        //          if true, hide sublists
        //          if false, show sublists
        //          I realize in hindsight this is a horrible var name change it if you want
        new_butt.isClicked;
        new_butt.onclick = display_sublists;
        

        var new_li = document.createElement('li');
        new_li.innerHTML = key;

        new_div.className = "list_item";
        new_div.appendChild(new_butt);
        new_div.appendChild(new_li);

        document.getElementById('lists').appendChild(new_div);
    }
}

function display_sublists(e){
    
    
    if(e.target.isClickNew == null){
        for (var key in coursework[e.target.id]){
            // Create a new list item element'
            var new_div = document.createElement('div');
            var new_butt = document.createElement('button');
            new_butt.innerHTML = "V";
            new_butt.id = key;
            new_butt.onclick = display_sublists;
            var new_li = document.createElement('li');
            new_li.innerHTML = key;

            new_div.className = "list_item";
            new_div.appendChild(new_butt);
            new_div.appendChild(new_li);

            e.target.parentNode.appendChild(new_div);
        }
        e.target.isClicked = true;
        console.log("Creating sublists");
    }
    else if(e.target.isClicked){
        e.target.parentNode.childNodes.forEach(function(child){
            if(child.className == "list_item"){
                child.style.display = "none";
            }
        });
        e.target.isClicked = false;
        console.log("Hiding sublists");
    }
    else if(!e.target.isClicked){
        e.target.parentNode.childNodes.forEach(function(child){
            if(child.className == "list_item"){
                child.style.display = "block";
            }
        });
        e.target.isClicked = true;
        console.log("Showing sublists");
    }
    
    
}

function add_course(){
    console.log("Adding course");
    new_course = document.getElementById("new_course").value;
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
        display_courses(data);
    })
}
