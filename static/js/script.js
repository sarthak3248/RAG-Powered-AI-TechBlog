const btn=document.getElementById("dark-btn");

btn.onclick=function(){

document.body.classList.toggle("dark");

if(btn.innerHTML=="🌙")

btn.innerHTML="☀";

else

btn.innerHTML="🌙";

}