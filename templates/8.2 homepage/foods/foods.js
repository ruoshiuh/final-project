document.addEventListener("DOMContentLoaded", function() {
    let subMenu = document.getElementById("subMenu");
    let imgBox = document.querySelectorAll(".img-box");
    let contentBox = document.querySelectorAll(".content-box");
    for (let i = 0; i < imgBox.length; i++)
    {
        imgBox[i].addEventListener("mouseover", function() {
            contentBox[i].style.opacity = "1";
        });
        imgBox[i].addEventListener("mouseout", function() {
            contentBox[i].style.opacity = "0";
        });
    };



});


function toggleMenu() {
    subMenu.classList.toggle("open-menu");
};
function goHome() {
    window.location.href = '../index.html';
};



