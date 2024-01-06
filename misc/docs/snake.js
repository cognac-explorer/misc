// Define the game constants
var canvasWidth = 800;
var canvasHeight = 1500;
var gridSize = 20;
var initialSnakeLength = 10;
var snakeSpeed = 200; // milliseconds between each snake movement
var foodSize = gridSize;
// Wait for the document to finish loading
document.addEventListener("DOMContentLoaded", function () {
    // Create the canvas element
    var canvas = document.createElement("canvas");
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;
    document.body.appendChild(canvas);
    var context = canvas.getContext("2d");
    // Define the snake class
    var Snake = /** @class */ (function () {
        function Snake() {
            this.x = 0;
            this.y = 0;
            this.dx = gridSize;
            this.dy = 0;
            this.cells = [];
        }
        Snake.prototype.update = function () {
            this.x += this.dx;
            this.y += this.dy;
            // Wrap the snake around the canvas
            if (this.x >= canvasWidth) {
                this.x = 0;
            }
            else if (this.x < 0) {
                this.x = canvasWidth - gridSize;
            }
            if (this.y >= canvasHeight) {
                this.y = 0;
            }
            else if (this.y < 0) {
                this.y = canvasHeight - gridSize;
            }
            // Create a new head cell
            var head = { x: this.x, y: this.y };
            this.cells.unshift(head);
            // Remove tail cells if the snake is longer than the required length
            if (this.cells.length > initialSnakeLength) {
                this.cells.pop();
            }
        };
        Snake.prototype.draw = function () {
            context.fillStyle = "green";
            this.cells.forEach(function (cell) {
                context.fillRect(cell.x, cell.y, gridSize, gridSize);
            });
        };
        Snake.prototype.setDirection = function (direction) {
            switch (direction) {
                case "ArrowUp":
                    this.dx = 0;
                    this.dy = -gridSize;
                    break;
                case "ArrowDown":
                    this.dx = 0;
                    this.dy = gridSize;
                    break;
                case "ArrowLeft":
                    this.dx = -gridSize;
                    this.dy = 0;
                    break;
                case "ArrowRight":
                    this.dx = gridSize;
                    this.dy = 0;
                    break;
            }
        };
        return Snake;
    }());
    // Define the food class
    var Food = /** @class */ (function () {
        function Food() {
            this.x = getRandomPosition(canvasWidth);
            this.y = getRandomPosition(canvasHeight);
        }
        Food.prototype.draw = function () {
            context.fillStyle = "red";
            context.fillRect(this.x, this.y, foodSize, foodSize);
        };
        return Food;
    }());
    // Utility function to generate random positions for the food
    function getRandomPosition(max) {
        return Math.floor(Math.random() * max / gridSize) * gridSize;
    }
    // Define touch variables
    var touchStartX = 0;
    var touchStartY = 0;
    // Handle touch start event
    canvas.addEventListener("touchstart", function (event) {
        touchStartX = event.touches[0].clientX;
        touchStartY = event.touches[0].clientY;
    });
    // Handle touch end event
    canvas.addEventListener("touchend", function (event) {
        var touchEndX = event.changedTouches[0].clientX;
        var touchEndY = event.changedTouches[0].clientY;
        var dx = touchEndX - touchStartX;
        var dy = touchEndY - touchStartY;
        if (Math.abs(dx) > Math.abs(dy)) {
            // Horizontal swipe
            if (dx > 0) {
                snake.setDirection("ArrowRight");
            }
            else {
                snake.setDirection("ArrowLeft");
            }
        }
        else {
            // Vertical swipe
            if (dy > 0) {
                snake.setDirection("ArrowDown");
            }
            else {
                snake.setDirection("ArrowUp");
            }
        }
    });
    // Create the snake object
    var snake = new Snake();
    var food = new Food();
    // Handle keyboard input
    document.addEventListener("keydown", function (event) {
        snake.setDirection(event.key);
    });
    // Update and render the game
    function gameLoop() {
        context.clearRect(0, 0, canvasWidth, canvasHeight);
        // Draw the boundary
        context.strokeStyle = "red";
        context.lineWidth = 5;
        context.strokeRect(0, 0, canvasWidth, canvasHeight);
        snake.update();
        snake.draw();
        food.draw();
        // Check if the snake eats the food
        if (snake.cells[0].x === food.x && snake.cells[0].y === food.y) {
            // Increase snake length
            var tail = { x: snake.cells[0].x, y: snake.cells[0].y };
            snake.cells.push(tail);
            // Create new food
            food = new Food();
        }
        setTimeout(gameLoop, snakeSpeed);
    }
    // Start the game loop
    gameLoop();
});
