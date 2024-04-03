var coursework = {};

function call(){
    fetch('http://127.0.0.1:5000/get_lists')
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        coursework = data;
        console.log(coursework);

        var i = 0;
        document.getElementById('lists').innerHTML = '';
        // Display the data on client
        for (var key in coursework){
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

            document.getElementById('lists').appendChild(new_div);

            
        }
    })
    .catch(function (error) {
        console.log('Error:', error);
    });

}


function display_sublists(e){
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
}