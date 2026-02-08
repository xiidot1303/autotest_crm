obj = document.getElementById('alert-box');
if (obj) {
    setTimeout(function(){
        obj.style.opacity = 0;
    }, 3000);
    
    setTimeout(function(){
        obj.style.display = "none";
    }, 8000);

}
