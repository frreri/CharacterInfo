document.addEventListener('DOMContentLoaded', () => {

    // Setting up the grid and it's child elements etc
    const grid = document.querySelector('.grid');
    const gridWidth = 10;
    let squares = [];
    for (let i = 0; i < 210; i++) {
        let squareDiv = document.createElement('div');
        if (i >= 200) {
            squareDiv.classList.add('taken');
        }
        grid.appendChild(squareDiv);
        squares.push(squareDiv);
    }

    // Tetris shapes
    const lShape = [
        [1, gridWidth + 1, gridWidth * 2 + 1, 2],
        [gridWidth, gridWidth + 1, gridWidth + 2, gridWidth * 2 + 2],
        [1, gridWidth + 1, gridWidth * 2 + 1, gridWidth * 2],
        [gridWidth, gridWidth * 2, gridWidth * 2 + 1, gridWidth * 2 + 2]
    ];
    const zShape = [
        [0, gridWidth, gridWidth + 1, gridWidth * 2 + 1],
        [gridWidth + 1, gridWidth + 2, gridWidth * 2, gridWidth * 2 + 1],
        [0, gridWidth, gridWidth + 1, gridWidth * 2 + 1],
        [gridWidth + 1, gridWidth + 2, gridWidth * 2, gridWidth * 2 + 1]
    ];
    const tShape = [
        [1, gridWidth, gridWidth + 1, gridWidth + 2],
        [1, gridWidth + 1, gridWidth + 2, gridWidth * 2 + 1],
        [gridWidth, gridWidth + 1, gridWidth + 2, gridWidth * 2 + 1],
        [1, gridWidth, gridWidth + 1, gridWidth * 2 + 1]
    ];
    const oShape = [
        [0, 1, gridWidth, gridWidth + 1],
        [0, 1, gridWidth, gridWidth + 1],
        [0, 1, gridWidth, gridWidth + 1],
        [0, 1, gridWidth, gridWidth + 1]
    ];
    const iShape = [
        [1, gridWidth + 1, gridWidth * 2 + 1, gridWidth * 3 + 1],
        [gridWidth, gridWidth + 1, gridWidth + 2, gridWidth + 3],
        [1, gridWidth + 1, gridWidth * 2 + 1, gridWidth * 3 + 1],
        [gridWidth, gridWidth + 1, gridWidth + 2, gridWidth + 3]
    ];
    const allShapes = [lShape, zShape, tShape, oShape, iShape];

    // Setting random start shape and position
    let currentPosition = 4;
    let currentRotation = 0;
    let random = Math.floor(Math.random() * allShapes.length);
    let nextRandom = 0;
    let current = allShapes[random][currentRotation];
    let timerId;

    // Draw shape, and undraw shape
    function draw() {
        current.forEach(index => {
            squares[currentPosition + index].classList.add('shape');
        });
    }
    function undraw() {
        current.forEach(index => {
            squares[currentPosition + index].classList.remove('shape');
        });
    }

    // Check if next to grid element is taken and if so, freeze shape and create new one
    function freeze() {
        if (current.some(index => squares[currentPosition + index + gridWidth].classList.contains('taken'))) {
            current.forEach(index => squares[currentPosition + index].classList.add('taken'));
            // new shape
            random = nextRandom;
            nextRandom = Math.floor(Math.random() * allShapes.length);
            current = allShapes[random][currentRotation];
            currentPosition = 4;
            draw();
            displayNextShape();
            addScore();
            gameOver();
        }
    }

    // Keybindings
    function control(e) {
        if (e.keyCode === 37 && timerId) {
            moveLeft();
        } else if (e.keyCode === 38 && timerId) {
            rotate();
        } else if (e.keyCode === 39 && timerId) {
            moveRight();
        } else if (e.keyCode === 40 && timerId) {
            moveDown();
        }
    }
    document.addEventListener('keyup', control);

    // Shape movement functions
    function moveDown() {
        undraw();
        currentPosition += gridWidth;
        draw();
        freeze();
    }
    function moveLeft() {
        undraw();
        const isMaxLeft = current.some(index => (currentPosition + index) % gridWidth === 0);

        if (!isMaxLeft) currentPosition -= 1;

        if (current.some(index => squares[currentPosition + index].classList.contains('taken'))) {
            currentPosition += 1;
        }
        draw();
    }
    function moveRight() {
        undraw();
        const isMaxRight = current.some(index => (currentPosition + index) % gridWidth === gridWidth - 1);

        if (!isMaxRight) currentPosition += 1;

        if (current.some(index => squares[currentPosition + index].classList.contains('taken'))) {
            currentPosition -= 1;
        }
        draw();
    }
    function rotate() {
        undraw();
        currentRotation++;
        if (currentRotation === current.length) {
            currentRotation = 0;
        }
        current = allShapes[random][currentRotation];
        draw();
    }

    // Displaying upcoming shapes

    // Setting up minigrid for displaying next shape
    const nextGrid = document.querySelector('.next-grid');
    const nextGridWidth = 4;
    let nextSquares = [];
    for (let i = 0; i < 16; i++) {
        let nextDiv = document.createElement('div');
        nextGrid.appendChild(nextDiv);
        nextSquares.push(nextDiv);
    }
    let nextGridIndex = 0;

    // Next shapes
    const nextShapes = [
        [1, nextGridWidth + 1, nextGridWidth * 2 + 1, 2],
        [0, nextGridWidth, nextGridWidth + 1, nextGridWidth * 2 + 1],
        [1, nextGridWidth, nextGridWidth + 1, nextGridWidth + 2],
        [0, 1, nextGridWidth, nextGridWidth + 1],
        [1, nextGridWidth + 1, nextGridWidth * 2 + 1, nextGridWidth * 3 + 1]
    ];

    // Display the next shape
    function displayNextShape() {
        nextSquares.forEach(square => {
            square.classList.remove('shape');
        });
        nextShapes[nextRandom].forEach(index => {
            nextSquares[nextGridIndex + index].classList.add('shape');
        });
    }

    // Start/Pause button
    const startButton = document.querySelector('#start-button');
    startButton.addEventListener('click', () => {
        if (timerId) {
            clearInterval(timerId);
            timerId = null;
        } else {
            if (!squares.some(square => square.classList.contains('shape'))) {
                nextRandom = Math.floor(Math.random() * allShapes.length);
                displayNextShape();
            }
            draw();
            timerId = setInterval(moveDown, 500);

        }
    });

    // Add score
    const scoreDisplay = document.querySelector('#score');
    let score = 0;
    function addScore() {
        for (let i = 0; i < 199; i += gridWidth) {
            const row = [i, i + 1, i + 2, i + 3, i + 4, i + 5, i + 6, i + 7, i + 8, i + 9];

            if (row.every(index => squares[index].classList.contains('taken'))) {
                score += 10;
                scoreDisplay.innerHTML = score;
                row.forEach(index => {
                    squares[index].classList.remove('taken', 'shape');
                });
                const squaresRemoved = squares.splice(i, gridWidth);
                squares = squaresRemoved.concat(squares);
                squares.forEach(cell => grid.appendChild(cell));
            }
        }
    }

    // Game over
    let gameOverText = document.createElement('div');
    gameOverText.innerHTML = 'Game Over!';
    gameOverText.classList.add('game-over');
    gameOverText.style.top = window.innerHeight / 2 - 41 + 'px';
    gameOverText.style.left = window.innerWidth / 2 - 180 + 'px';
    gameOverText.style.display = 'none';
    document.body.appendChild(gameOverText);

    function gameOver() {
        if (current.some(index => squares[currentPosition + index].classList.contains('taken'))) {
            gameOverText.style.display = 'block';
            clearInterval(timerId);
            timerId = null;
        }
    }
})