(() => {
    const canvas = document.querySelector('#main');

    // get the 2D context, and then I am able to draw somnething on it 
    let ctx = canvas.getContext('2d');

    // set fill and stroke styles
    ctx.fillStyle = '#F0DB4F';

    // map
    const map = [1, 0, 1, 0, 1, 0, 1, 0];
    map.forEach(item => {
        console.log(`${item}`)
    });

    // draw a rectangle with fill and stroke
    ctx.fillRect(50, 50, 500, 500);

})();