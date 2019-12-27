const signUpButton = document.getElementById('next');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
    container.classList.add('right-panel-active');
});

signInButton.addEventListener('click', () => {
    container.classList.remove('right-panel-active');
});
var submit = [false, false, false, false];
function handleEmail(email) {
    if (email.includes("@") == false) {

        return false;
    }
    else{
        return true;
    }

   

}
function handleUsername(e) {
    var icon = document.getElementById("name1");
    

    if (e.value.length != 0) {
        
        submit[0] = true;
    }
    else {

        submit[0] = false;
    }

}
function handleMobile(e) {
    var icon = document.getElementById( "contact1");


    if (e.value.length == 10) {

        submit[2] = true;
    }
    else {

        submit[2] = false;
    }

}
function handleEmailIcon(e) {
    var icon = document.getElementById("email1");
  

    if (e.value.length != 0 && handleEmail(e.value)) {

        submit[1] = true;
    }
    else {

        submit[1] = false;
    }

}
function handleSubmit() {

    console.log(submit.indexOf(false));
    if (submit.indexOf(false) != -1) {
        return false;
    }
    else{
        return true;
    }
   
}