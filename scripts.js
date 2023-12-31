(() => {
    const canvas = document.querySelector('#main');

    // get the 2D context, and then I am able to draw somnething on it 
    let ctx = canvas.getContext('2d');


    // map
    // 0: road      1: wall      2: roads with points
    const map = [
                    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                    
                ];

    block = 30;
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
                ctx.fillRect(block * j, block * i, block, block);
            }    
            if(row[j] == 1) 
            {
                ctx.fillStyle = 'black';
                ctx.strokeStyle = '#393ff1';
                ctx.fillRect(block * j, block * i, block, block);
                ctx.strokeRect(block * j, block * i, block, block);
            }    
        }
    }


})();