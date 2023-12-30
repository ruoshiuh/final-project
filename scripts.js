(() => {
    const canvas = document.querySelector('#main');

    // get the 2D context, and then I am able to draw somnething on it 
    let ctx = canvas.getContext('2d');


    // map
    // 0: road      1: wall      2: roads with points
    const map = [
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],                    
                ];
    initial_x = 50;
    initial_y = 50;
    pos_x = initial_x;
    pos_y = initial_y;
    scale_x = 30;
    scale_y = 12;
    ctx.lineWidth = 3;
    for(let i = 0; i < map.length; i++) 
    {
        let row = map[i];

        for(let j = 0; j < map[i].length; j++) 
        {
            // printing each grid
            if(row[j] == 0) 
            {
                ctx.fillStyle = '#fff';
                ctx.fillRect(pos_x, pos_y, scale_x, scale_y);
                pos_x += scale_x;
            }    
            if(row[j] == 1) 
            {
                ctx.fillStyle = 'black';
                ctx.strokeStyle = '#393ff1';
                ctx.fillRect(pos_x, pos_y, scale_x, scale_y);
                ctx.strokeRect(pos_x, pos_y, scale_x, scale_y);
                pos_x += scale_x;
            }    
        }
        // a row has ended, reset the starting point
        pos_x = initial_x;
        pos_y = initial_y + (scale_y * i);
    }


})();