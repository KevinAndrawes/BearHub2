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