
// Below function Executes on click of login button.
function validate(){
    event.preventDefault()

    let req = new XMLHttpRequest();
    let formData = new FormData();
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;


    req.open("POST", 'http://localhost:5000/login?email='+email+'&password='+password)
    // req.open("POST", 'https://3c492ad4.ngrok.io/login?email='+email+'&password='+password)
    req.onreadystatechange = function() {
        let resp = JSON.parse(this.response).OK.toString();

        if(resp === '1'){
            window.location.href = "homepage.html"; // Redirecting to other page.
        }
        else{
            alert("Invalid Username or Password")
            return false
        }


    };
    req.send(formData);

}


