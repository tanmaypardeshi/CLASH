var countDownDate = new Date().getTime();
var remTime = document.getElementById("time").value;
            var x = setInterval(function () {


                var seconds = Math.floor((remTime) % 60);
                var minutes = Math.floor((remTime / 60));

                if((minutes>0)||(seconds>0)){
                    if (minutes < 10) {
                        document.getElementById("min").innerHTML = "0" + minutes;
                    }
                    else {
                        document.getElementById("min").innerHTML = minutes;
                    }
                    if (seconds < 10) {
                        document.getElementById("sec").innerHTML = "0" + seconds;
                    }
                    else {
                        document.getElementById("sec").innerHTML = seconds;
                    }
                }
                else if(minutes==0&&seconds==0){
                    document.getElementById("min").innerHTML = "0"+"0";
                    document.getElementById("sec").innerHTML = "0"+"0";

                        document.getElementById("min").style.color="#F32013";
                        document.getElementById("sec").style.color="#F32013";


                }

                if(seconds<50){
                    document.getElementById("br1").style.backgroundColor="black";
                    document.getElementById("br1").style.opacity=0.2

                }
                if(seconds<40){
                    document.getElementById("br2").style.backgroundColor="black";
                    document.getElementById("br2").style.opacity=0.2

                }
                if(seconds<30){
                    document.getElementById("br3").style.backgroundColor="black";
                    document.getElementById("br3").style.opacity=0.2

                }
                if(seconds<20){
                    document.getElementById("br4").style.backgroundColor="black";
                    document.getElementById("br4").style.opacity=0.2

                }
                if(seconds<10){
                    document.getElementById("br5").style.backgroundColor="black";
                    document.getElementById("br5").style.opacity=0.2

                }
                if(seconds==0){
                    document.getElementById("br6").style.backgroundColor="black";
                    document.getElementById("br6").style.opacity=0.2

                }
                if(minutes<25){
                    document.getElementById("ar1").style.backgroundColor="black";
                    document.getElementById("ar1").style.opacity=0.2

                }
                if(minutes<20){
                    document.getElementById("ar2").style.backgroundColor="black";
                    document.getElementById("ar2").style.opacity=0.2

                }
                if(minutes<15){
                    document.getElementById("ar3").style.backgroundColor="black";
                    document.getElementById("ar3").style.opacity=0.2

                }
                if(minutes<10){
                    document.getElementById("ar4").style.backgroundColor="black";
                    document.getElementById("ar4").style.opacity=0.2

                }
                if(minutes<5){
                    document.getElementById("ar5").style.backgroundColor="black";
                    document.getElementById("ar5").style.opacity=0.2

                }
                if(minutes==0){
                    document.getElementById("ar6").style.backgroundColor="black";
                    document.getElementById("ar6").style.opacity=0.2

                }

                  if(seconds>50){
                    document.getElementById("br1").style.backgroundColor="rgb(255,255,230) 	";
                    document.getElementById("br2").style.backgroundColor="rgb(255,255,230) 	";
                    document.getElementById("br3").style.backgroundColor="rgb(255,255,230) 	";
                    document.getElementById("br4").style.backgroundColor="rgb(255,255,230) 	";
                    document.getElementById("br5").style.backgroundColor="rgb(255,255,230) 	";
                    document.getElementById("br6").style.backgroundColor="rgb(255,255,230) 	";
                    document.getElementById("br1").style.opacity=0.7;
                    document.getElementById("br2").style.opacity=0.7;
                    document.getElementById("br3").style.opacity=0.7;
                    document.getElementById("br4").style.opacity=0.7;
                    document.getElementById("br5").style.opacity=0.7;
                    document.getElementById("br6").style.opacity=0.7;
                }

                if(minutes>50){
                    document.getElementById("ar1").style.backgroundColor="rgb(255,255,230) 	";
                    document.getElementById("ar2").style.backgroundColor="rgb(255,255,230) 	";
                    document.getElementById("ar3").style.backgroundColor="rgb(255,255,230) 	";
                    document.getElementById("ar4").style.backgroundColor="rgb(255,255,230) 	";
                    document.getElementById("ar5").style.backgroundColor="rgb(255,255,230) 	";
                    document.getElementById("ar6").style.backgroundColor="rgb(255,255,230) 	";
                    document.getElementById("ar1").style.opacity=0.7;
                    document.getElementById("ar2").style.opacity=0.7;
                    document.getElementById("ar3").style.opacity=0.7;
                    document.getElementById("ar4").style.opacity=0.7;
                    document.getElementById("ar5").style.opacity=0.7;
                    document.getElementById("ar6").style.opacity=0.7;
                }
                remTime--;
                if(remTime <= 0)
                {
                    window.location.href = "../logout/";
                }

            }, 1000);

var modal0 = document.getElementById("myModal");

var btn0 = document.getElementById("hints");

var span = document.getElementsByClassName("close")[0];

btn0.onclick = function() {
  modal0.style.display = "block";
}

span.onclick = function() {
  modal0.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal0) {
      modal1.style.display = "none";
    }
}

var modal1 = document.getElementById("myModal1");

var btn1 = document.getElementById("instr");

var span1 = document.getElementsByClassName("close4")[0];

btn1.onclick = function() {
  modal1.style.display = "block";
}

span1.onclick = function() {
  modal1.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal1) {
    modal1.style.display = "none";
  }
}


var modal2 = document.getElementById("myModal2");

var btn2 = document.getElementById("logout");

var span2 = document.getElementsByClassName("close2")[0];

btn2.onclick = function() {
  modal2.style.display = "block";
}

span2.onclick = function() {
  modal2.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal2) {
    modal2.style.display = "none";
  }
}


var t1= document.getElementById('a1');
var t2= document.getElementById('a2');
var btn= document.getElementById('submit');
var x= document.getElementById('ddd');
var y= document.getElementById('ccc');
var txt= document.getElementById('invalidtxt');
var txt2= document.getElementById('invalidtxt2');

t2.disabled= true;
t2.classList.add('disabled');



    function sb() {
        if (t1.disabled==true) {
            if (((document.getElementById('a2')).value.length)==0) {
                t2.style.border= '1px solid red';
                y.classList.add("shake");
                txt2.classList.add("appear");
                setTimeout(removey,500);
                setTimeout(remmy,1000);
            }
            else {
                if (parseInt(document.getElementById("a2").value)!=100) {
                    t2.style.border='2px solid red';
                    t2.disabled=true;
                    t2.classList.add("disabled");
                    t2.disabled=true;
                    t2.classList.add("disabled");
                    t2.classList.add("inchoice");
                    txt2.style.paddingRight='223px';
                    txt2.innerHTML= "Incorrect Answer";
                    txt2.classList.add("appear");
                }
                else {
                    t2.style.border='2px solid #1eff00';
                    txt2.style.color= '#1eff00';
                    txt2.style.paddingRight='233px';
                    txt2.innerHTML= "Correct Answer";
                    txt2.classList.add("appear");
                }
            }
        }
        else {
            if (((document.getElementById('a1')).value.length)==0) {
                t1.style.border= '1px solid red';
                x.classList.add("shake");
                txt.classList.add("appear");
                setTimeout(remove,500);
                setTimeout(remm,1000);
            }
            else {
                if (parseInt(document.getElementById("a1").value)!=100) {
                    t1.style.border='2px solid red';
                    t1.disabled=true;
                    t1.classList.add('inchoice');
                    t1.classList.add("disabled");
                    t2.disabled=false;
                    t2.classList.remove("disabled");
                    txt.innerHTML= "Incorrect Answer";
                    txt.classList.add("appear");
                }
                else {
                    t1.style.border='2px solid #1eff00';
                    txt.style.color= '#1eff00';
                    txt.innerHTML= "Correct Answer";
                    txt.classList.add("appear");
                }
            }
        }
    }

    function remove() {
        x.classList.remove("shake");
        t1.style.border= 'none';
    }

    function remm() {
        txt.classList.remove("appear");
    }

    function removey() {
        y.classList.remove("shake");
        t2.style.border= 'none';
    }

    function remmy() {
        txt2.classList.remove("appear");
    }