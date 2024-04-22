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