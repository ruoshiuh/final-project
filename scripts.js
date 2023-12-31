(() => {
    const canvas = document.querySelector('#main');

    // get the 2D context, and then I am able to draw somnething on it 
    let ctx = canvas.getContext('2d');


    // map
    // 0: road      1: wall      2: roads with points
    const map = [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1],
                    [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],                                    
                ];

    let block = 40;
    let padding = block * 0.2;

    // default walls and roads
    for(let i = 0; i < map.length; i++) 
    {
        let row = map[i];
        for(let j = 0; j < map[i].length; j++) 
        {
            // the roads
            if(row[j] == 0) 
            {
                ctx.fillStyle = 'black';
                ctx.fillRect(block * j, block * i, block, block);
            }    
            // the walls
            if(row[j] == 1) 
            {
                ctx.fillStyle = '#393ff1';
                ctx.fillRect(block * j, block * i, block, block);
            } 
        }
    }
    // painting the inner box for walls
    for(let i = 0; i < map.length; i++) 
    {
        let row = map[i];
        for(let j = 0; j < map[i].length; j++) 
        {
            pos_x = block * j;
            pos_y = block * i;
            // 1. adjacent left and right
            if(row[j] == 1 && row[j + 1] == 1) 
            {
                ctx.fillStyle = 'black';
                ctx.fillRect(pos_x + padding, pos_y + padding, block * 2 - padding * 2, block - padding * 2);
            } 
        }
    }
   


})();