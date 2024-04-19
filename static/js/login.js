//signup form action
document.getElementById('loginForm').addEventListener('submit', function(event){
    event.preventDefault();
    
    //Grab the values in each input box
    var username = this.elements['username'].value;
    var password = this.elements['password'].value;
    console.log(username);
    data = {
        "username": username,
        "password": password,
    }
    send_post_request(data, '/login').then(response =>
    {
    if(response == "Account logged in"){
        window.location.href = "/templates/index.html";
        //console.log(response)
        localStorage.setItem('current_user', username); // Save current_user to localStorage
    }
    else{
        alert(response)
    }})
})