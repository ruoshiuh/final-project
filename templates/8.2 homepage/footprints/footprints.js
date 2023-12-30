document.addEventListener("DOMContentLoaded", function() {
    let subMenu = document.getElementById("subMenu");
    let sliderNav = document.querySelectorAll(".lbtn");
    let contentBox = document.querySelectorAll(".content-box");
    for (let i = 0; i < sliderNav.length; i++) {
        sliderNav[i].addEventListener('click', function() {
            for (let k = 0; k < contentBox.length; k++) {
                contentBox[k].style.opacity = '0';
            };
            contentBox[i].style.opacity = '1';
        });
    };
});


function toggleMenu() {
    subMenu.classList.toggle("open-menu");
};
function goHome() {
    window.location.href = '../index.html';
};



