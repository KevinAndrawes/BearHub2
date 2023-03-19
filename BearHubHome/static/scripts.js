function showInfo() {
    var infoWindow = document.getElementById("infoWindow");
    infoWindow.classList.add("show");
}

function hideInfo() {
    var infoWindow = document.getElementById("infoWindow");
    infoWindow.classList.remove("show");
}
var infoButton = document.querySelector(".topnav button");
infoButton.addEventListener("mouseover", showInfo);
infoButton.addEventListener("mouseout", hideInfo);

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    document.body.style.backgroundColor = "white";
}

