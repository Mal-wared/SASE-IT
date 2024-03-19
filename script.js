function call(){
    fetch('http://127.0.0.1:5000/get_lists')
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        console.log(data);
    })
    .catch(function (error) {
        console.log('Error:', error);
    });

}