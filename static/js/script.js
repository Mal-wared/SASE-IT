var current_user = localStorage.getItem('current_user');
console.log(current_user)
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
        create_content(coursework);
    })
    .catch(function (error) {
        console.log('Error:', error);
    });
}

//signup form action
document.getElementById('signupForm').addEventListener('submit', function(event){
    event.preventDefault();
    
    //Grab the values in each input box
    var email = this.elements['email'].value;
    var username = this.elements['username'].value;
    var password = this.elements['password'].value;
    var confirm_password = this.elements['confirm_password'].value;
    console.log(email);
    data = {
        "email": email,
        "username": username,
        "password": password,
        "confirm_password": confirm_password
    }
    send_post_request(data, '/signup').then(response =>
    {
    if(response == "Account created successfully"){
        console.log(response)
        localStorage.setItem('current_user', username); // Save current_user to localStorage
        window.location.href = "/templates/index.html";
    }
    else{
        alert(response)
    }})
})

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
    if(e.target.isClicked == null){
        for (var key in coursework[e.target.id]){
            // Create a new list item element'
            var new_div = document.createElement('div');
            var new_butt = document.createElement('button');
            new_butt.innerHTML = "V";
            new_butt.id = key;
            new_butt.onclick = display_sublists;
            var new_li = document.createElement('li');
            new_li.innerHTML = key;

            new_div.className = "folder_list_item";
            new_div.appendChild(new_butt);
            new_div.appendChild(new_li);

            e.target.parentNode.appendChild(new_div);
        }
        e.target.isClicked = true;
        console.log("Creating sublists");
    }
    else if(e.target.isClicked){
        e.target.parentNode.childNodes.forEach(function(child){
            if(child.className == "folder_list_item"){
                child.style.display = "none";
            }
        });
        e.target.isClicked = false;
        console.log("Hiding sublists");
    }
    else if(!e.target.isClicked){
        e.target.parentNode.childNodes.forEach(function(child){
            if(child.className == "folder_list_item"){
                child.style.display = "block";
            }
        });
        e.target.isClicked = true;
        console.log("Showing sublists");
    }
}

// Displays the content of the dictionary
// function create_content(coursework){
//     // Create the header(s)
//     document.getElementById('content_header').innerHTML = Object.keys(coursework)[0];
//     document.getElementById('content').innerHTML = '';
    
//     // Create the content based on the keys in the coursework object
//     for (var key in coursework["phys_2111"]){
//         var new_div = document.createElement("div");
//         var key_header = document.createElement("h2");
//         key_header.innerHTML = key;
//         new_div.appendChild(key_header);
//         document.getElementById('content').appendChild(new_div);
//         current_coursework = coursework["phys_2111"];
//         for(var idx in current_coursework[key]){
//             var coursework_div = document.createElement("div");
//             var homework_title = document.createElement("p");
//             homework_title.innerHTML = current_coursework[key][idx]["name"];
//             coursework_div.appendChild(homework_title);
//             new_div.appendChild(coursework_div);
//         }
//     }
// }

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

function send_post_request(data, url){
    return fetch(`http://127.0.0.1:5000/${url}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        //console.log(data);
        return data;
    });
}

function goHome(){
    window.location.href = "/templates/landingpage.html";
}

function check_user(){
    var storedUser = localStorage.getItem('current_user'); // Retrieve current_user from localStorage
    console.log(storedUser)
    var nav = document.querySelector('nav');
    if(storedUser){
        console.log("Deleting")
        var loginAnchor = nav.querySelector('a[href="/templates\\login.html"]');
        var signupAnchor = nav.querySelector('a[href="/templates\\signup.html"]');
        if (loginAnchor) {
            nav.removeChild(loginAnchor);
        }
        if (signupAnchor) {
            nav.removeChild(signupAnchor);
        }
    }
    else{
        console.log("adding")
        // Create new login and signup anchors
        var newLoginAnchor = document.createElement('a');
        newLoginAnchor.setAttribute('href', '/templates\\login.html');
        newLoginAnchor.textContent = 'LOGIN';

        var newSignupAnchor = document.createElement('a');
        newSignupAnchor.setAttribute('href', '/templates\\signup.html');
        newSignupAnchor.textContent = 'SIGN UP';

        // Append the new anchors to the navigation menu
        nav.appendChild(newLoginAnchor);
        nav.appendChild(newSignupAnchor);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    check_user();
});