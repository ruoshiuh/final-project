(() => {
    const canvas = document.querySelector('#main');

    // get the 2D context, and then I am able to draw somnething on it 
    let ctx = canvas.getContext('2d');


    // map
    // 0: road      1: wall      2: roads with points
    const map = [1, 1, 1, 1, 1, 1, 1, 1];
    pos_x = 50;
    pos_y = 50;
    scale_x = 1000;
    scale_y = 12;
    ctx.lineWidth = 3;
    map.forEach(item => {
        if(item == 1) {
            ctx.fillStyle = 'black';
            ctx.strokeStyle = '#393ff1';
            ctx.fillRect(pos_x, pos_y, scale_x, scale_y);
            ctx.strokeRect(pos_x, pos_y, scale_x, scale_y);
            pos_x += scale_x;
        };
    });

    // draw a rectangle with fill and stroke

})();