
var uploadBtn = document.getElementById("upload-button");
var realBtn = document.getElementById("real-file");
var output;
var file;

function Upload() {
    var realBtn = document.getElementById("real-file"); 
    realBtn.click();  
    return false;
}

function Reset(){
    document.getElementById("diagnose-form").reset();
    document.getElementById("upload-button").disabled = false;
}


function Changed(event) {
    var realBtn = document.getElementById("real-file");
    var text = document.getElementById("custom-text");
    var checkButton = document.getElementById("check-disease");
    var uploadBtn = document.getElementById("upload-button");
    var resetBtn = document.getElementById("reset-button");
    if(realBtn.value){
        uploadBtn.disabled = true;
        text.innerHTML = realBtn.value
        checkButton.hidden = false;
        resetBtn.hidden = false;
    }
    file = event.target.files[0];
    output = document.getElementById('myImg');
    output.src = URL.createObjectURL(event.target.files[0]);
    text.innerHTML = realBtn.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];      
}
 
function checkDisease(event) {
    event.preventDefault()
    let req = new XMLHttpRequest();
    let formData = new FormData();
    var textOver = document.getElementById("textOver");
    let disease = document.getElementById("disease").value;
    let fname = document.getElementById("fname").value;
    let lname = document.getElementById("lname").value;
    let ins_ID = document.getElementById("insuranceID").value;
    let city = document.getElementById("city").value;
    let dob = document.getElementById("dob").value;
    let date = document.getElementById("date").value;
    
    
    formData.append("photo", file);                                
    req.open("POST", 'http://localhost:5000/prediction?model='+disease+'&fname='+fname+'&lname='+lname+'&ins_ID='+ins_ID+'&city='+city+'&dob='+dob+'&date='+date);
    // req.open("POST", 'https://3c492ad4.ngrok.io?model='+disease+'&fname='+fname+'&lname='+lname+'&ins_ID='+ins_ID+'&city='+city+'&dob='+dob+'&date='+date);
    req.onreadystatechange = function() {
        
        let pred = JSON.parse(this.response).Prediction.toString();
        

        if(pred === "1"){
            textOver.innerHTML = "Infected";
            textOver.style.color = "red";
        }
        if(pred === "0") {
            textOver.innerHTML = "Not Infected";
            textOver.style.color = "green";
        }
    };
    req.send(formData);
}