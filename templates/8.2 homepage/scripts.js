document.addEventListener('DOMContentLoaded', function() {
    // "Welcome to my home page" effect
    let mainText2 = document.querySelector('#main-text2');
    mainText2.addEventListener('mouseover', function() {
        mainText2.style.backgroundColor = '#ffd700';
        mainText2.style.color = '#1f528f';
        mainText2.innerHTML = 'My name is Ruo Shiuh';
        mainText2.style.fontWeight = '790';

    });
    mainText2.addEventListener('mouseout', function() {
        mainText2.style.backgroundColor = 'transparent';
        mainText2.style.color = '#ffd700';
        mainText2.innerHTML = 'Welcome to my home page';
        mainText2.style.fontWeight = 'bold';
    });

    let arrow = document.querySelectorAll('.arrow');
    let bottom_box = document.querySelectorAll('.bottom-box');
    for(let i = 0; i < bottom_box.length; i++)
    {
        bottom_box[i].addEventListener('mouseover', function() {
            arrow[i].style.color = 'white';
            arrow[i].style.transition = 'transform 0.4s';
            arrow[i].style.transform = 'translateX(10px)';
        });
        bottom_box[i].addEventListener('mouseout', function() {
            arrow[i].style.color = 'black';
            arrow[i].style.transition = 'transform 0.8s';
            arrow[i].style.transform = 'translateX(0px)';

        });
        bottom_box[i].addEventListener('click', function() {
            switch (i) {
                case 0:
                    window.location.href = 'homeland/homeland.html';
                    break;
                case 1:
                    window.location.href = 'hobbies/hobbies.html';
                    break;
                case 2:
                    window.location.href = 'foods/foods.html';
                    break;
                case 3:
                    window.location.href = 'footprints/footprints';
                    break;
            };
        });

    };





});

