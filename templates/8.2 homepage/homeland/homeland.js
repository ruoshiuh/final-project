document.addEventListener("DOMContentLoaded", function() {
    let subMenu = document.getElementById("subMenu");
});


function toggleMenu() {
    subMenu.classList.toggle("open-menu");
}
function goHome() {
    window.location.href = '../index.html';
}
