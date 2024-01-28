// game.js
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    scene: {
        preload: preload,
        create: create,
        update: update
    },
    physics: {
        default: 'arcade',
        arcade: {
            debug: false, // Set to true for debugging physics bodies
        }
    }
};

const game = new Phaser.Game(config);

let snake;
let food;
let cursors;
let score = 0;
let scoreText;
let snakeBody = [];
let scene; // Add a variable to store the scene reference
let touchStartX = 0;
let touchStartY = 0;

function preload() {
    this.load.image('snake', 'snake.png');
    this.load.image('food', 'food.png');
}

function create() {
    scene = this; // Store the scene reference in the variable

    cursors = this.input.keyboard.createCursorKeys();
    this.input.addPointer(1); // Enable touch input

    snake = this.physics.add.image(400, 300, 'snake').setScale(0.5);
    snake.setCollideWorldBounds(true);

    food = this.physics.add.image(Phaser.Math.Between(100, 700), Phaser.Math.Between(100, 500), 'food').setScale(0.5);

    scoreText = this.add.text(16, 16, 'Score: 0', { fontSize: '32px', fill: '#fff' });

    this.physics.add.overlap(snake, food, eatFood, null, this);

    // Listen for touch start event
    this.input.on('pointerdown', function (pointer) {
        touchStartX = pointer.x;
        touchStartY = pointer.y;
    }, this);

    // Listen for touch end event
    this.input.on('pointerup', function (pointer) {
        let touchEndX = pointer.x;
        let touchEndY = pointer.y;

        // Calculate the swipe distance in both X and Y axes
        let deltaX = touchEndX - touchStartX;
        let deltaY = touchEndY - touchStartY;

        // Determine the predominant direction of the swipe
        if (Math.abs(deltaX) > Math.abs(deltaY)) {
            // Horizontal swipe
            if (deltaX > 0) {
                snake.setVelocityX(200);
                snake.setVelocityY(0);
            } else if (deltaX < 0) {
                snake.setVelocityX(-200);
                snake.setVelocityY(0);
            }
        } else {
            // Vertical swipe
            if (deltaY > 0) {
                snake.setVelocityY(200);
                snake.setVelocityX(0);
            } else if (deltaY < 0) {
                snake.setVelocityY(-200);
                snake.setVelocityX(0);
            }
        }
    }, this);
}

function update() {
    if (cursors.left.isDown || this.input.pointer1.isDown) {
        snake.setVelocityX(-200);
        snake.setVelocityY(0);
    } else if (cursors.right.isDown) {
        snake.setVelocityX(200);
        snake.setVelocityY(0);
    } else if (cursors.up.isDown) {
        snake.setVelocityY(-200);
        snake.setVelocityX(0);
    } else if (cursors.down.isDown) {
        snake.setVelocityY(200);
        snake.setVelocityX(0);
    }

    if (snake.x < 0 || snake.x > 800 || snake.y < 0 || snake.y > 600) {
        this.scene.restart();
    }

    // Move the body segments in the update function
    moveBody();
}

function eatFood(snake, food) {
    food.setPosition(Phaser.Math.Between(100, 700), Phaser.Math.Between(100, 500));
    score += 10;
    scoreText.setText('Score: ' + score);

    // Create a new body segment at the tail
    if (snakeBody.length === 0) {
        let newBody = scene.physics.add.image(snake.x, snake.y, 'snake').setScale(0.5);
        snakeBody.push(newBody);
    } else {
        let newBody = scene.physics.add.image(snakeBody[snakeBody.length - 1].x, snakeBody[snakeBody.length - 1].y, 'snake').setScale(0.5);
        snakeBody.push(newBody);
    }
}

function moveBody() {
    if (snakeBody.length > 0) {
        // Move each body segment to the position of the previous segment
        for (let i = snakeBody.length - 1; i > 0; i--) {
            snakeBody[i].x = snakeBody[i - 1].x;
            snakeBody[i].y = snakeBody[i - 1].y;
        }

        // Move the first segment (head) to the position of the snake
        snakeBody[0].x = snake.x;
        snakeBody[0].y = snake.y;
    }
}
