
function register() {
    event.preventDefault()

    var req = new XMLHttpRequest();
    var formData = new FormData();

    var email = document.getElementById("email").value;
    var pwd1 = document.getElementById("pwd1").value;
    var pwd2 = document.getElementById("pwd2").value;
    var reference = document.getElementById("reference").value;
    req.open("POST", 'http://localhost:5000/register?email='+email+'&pwd1='+pwd1+'&reference='+reference)
    // req.open("POST", 'https://3c492ad4.ngrok.io/register?email='+email+'&pwd1='+pwd1+'&reference='+reference)
    req.onreadystatechange = function() {

        let nw = JSON.parse(this.response).nw.toString();

        if(nw === '1'){
            window.location.href = "homepage.html"; // Redirecting to other page.
        }


    };
    req.send(formData);


    // if(pwd1 === pwd2 && email.length > 1 ){
    //    window.location.href = "homepage.html";
    //     return false;
    // } else if (email.length < 1) {
    //     alert("Email cannot be blank")
    //     return false
    // } else if (reference.length < 1) {
    //     alert("Reference No. cannot be blank")
    //     return false
    // }
    //
    // else{
    //     alert("Passwords do not match");
    //     return false;
    // }


}
