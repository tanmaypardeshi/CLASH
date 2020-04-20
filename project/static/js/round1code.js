var score = document.getElementById("user_score").value;
function startTimer(duration, display1,display2) {
    var timer = duration;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10),
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        var score = document.getElementById("user_score").value;
        display1.textContent = minutes; 
        display2.textContent = seconds;
        if (--timer < 0) {
            document.getElementById("time1").textContent="00";
            document.getElementById("time2").textContent="00";
            if (score >= 40){
                document.getElementById('bonusModal').style.display = "block";
                window.onclick = function(event){
                if(event.target==document.getElementById('bonusModal'))
                document.getElementById('bonusModal').style.display = "block";
                }
            }
            else
            window.location.href = "../logout/";

        }
    }, 1000);
}
var logout = document.getElementById("lgout");
logout.onclick = function(){
if(score >= 40)
$('#bonusModal').modal("show");
}

window.onload = function () {
    var buff_cntr = document.getElementById("buff_cntr").value;
    var buffnumber = document.getElementById("buffnumber").value;
    var buff1 = document.getElementById("buff1").value;
    var buff2 = document.getElementById("buff2").value;
    var buff3 = document.getElementById("buff3").value;
    var stack = document.getElementById("stack").value;
    var life = document.getElementById("life").value;
    var life2 = document.getElementById("life2").value;
    var life1 = document.getElementById("life").value;
    if(buff1 !=0 && buff2 != 0 && buff3 != 0)
    {
        document.getElementById("facility").disabled = true;
    }
    if(buff1 !=0 && buff2 != 0 && buff3 != 0 && life1 == 1)
    {
        document.getElementById("facility").disabled = true;
    }
    else if(buff1 !=0 && buff2 != 0 && buff3 != 0 && life2 == 2)
    {
        document.getElementById("facility").disabled = true;
    }
    if(buff1 == 0 && buff2 == 0 && buff3 == 0)
    {
        document.getElementById("bffr1").style.visibility = "hidden";
        document.getElementById("bffr2").style.visibility = "hidden";
        document.getElementById("bffr3").style.visibility = "hidden";
    }
    else if(buff1 != 0 && buff2 == 0 && buff3 == 0)
    {
        document.getElementById("bffr2").style.visibility = "hidden";
        document.getElementById("bffr3").style.visibility = "hidden";
    }
    else if(buff2 != 0 && buff1 != 0 && buff3 == 0)
    {
        document.getElementById("bffr3").style.visibility = "hidden";
    }
    else if(buff1 == 0 && buff2 == 0 && buff3 != 0)
    {
        document.getElementById("bffr1").style.visibility = "hidden";
        document.getElementById("bffr2").style.visibility = "hidden";
    }
    else if(buff1 == 0 && buff2 != 0 && buff3 == 0)
    {
        document.getElementById("bffr1").style.visibility = "hidden";
        document.getElementById("bffr3").style.visibility = "hidden";
    }
    else if(buff1 != 0 && buff2 == 0 && buff3 != 0)
    {
        document.getElementById("bffr2").style.visibility = "hidden";
    }
    else if(buff1 == 0 && buff2 != 0 && buff3 != 0)
    {
        document.getElementById("bffr1").style.visibility = "hidden";
    }
    var life = document.getElementById("life").value;
    var life2 = document.getElementById("life2").value;
    if(life == 1)
    {
        document.getElementById("facility").disabled = true;
        document.getElementById("bffr1").disabled = true;
        document.getElementById("bffr2").disabled = true;
        document.getElementById("bffr3").disabled = true;
    }
    else if(life2 == 2)
    {
        document.getElementById("facility").disabled = true;
        document.getElementById("bffr1").disabled = true;
        document.getElementById("bffr2").disabled = true;
        document.getElementById("bffr3").disabled = true;
        document.getElementById("lifeline").disabled = true;
    }
    if(stack < 6)
    {
        document.getElementById("lifeline").disabled = true;
    }
    var Minutes = document.getElementById("time").value,
        display1 = document.getElementById("time1"),
        display2 =document.getElementById("time2");
    startTimer(Minutes, display1,display2);
};
// $(document).ready(function(){

//     $('#bonusModal').modal("toggle");
// });
