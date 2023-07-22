// Define the game constants
const canvasWidth = 400;
const canvasHeight = 400;
const gridSize = 20;
const initialSnakeLength = 10;
const snakeSpeed = 200; // milliseconds between each snake movement
const foodSize = gridSize;

// Wait for the document to finish loading
document.addEventListener("DOMContentLoaded", () => {
    // Create the canvas element
    const canvas = document.createElement("canvas");
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;
    document.body.appendChild(canvas);
    const context = canvas.getContext("2d");

    // Define the snake class
    class Snake {
        x: number;
        y: number;
        dx: number;
        dy: number;
        cells: Array<{ x: number; y: number }>;

        constructor() {
            this.x = 0;
            this.y = 0;
            this.dx = gridSize;
            this.dy = 0;
            this.cells = [];
        }

        update() {
            this.x += this.dx;
            this.y += this.dy;

            // Wrap the snake around the canvas
            if (this.x >= canvasWidth) {
                this.x = 0;
            } else if (this.x < 0) {
                this.x = canvasWidth - gridSize;
            }

            if (this.y >= canvasHeight) {
                this.y = 0;
            } else if (this.y < 0) {
                this.y = canvasHeight - gridSize;
            }

            // Create a new head cell
            const head = { x: this.x, y: this.y };
            this.cells.unshift(head);

            // Remove tail cells if the snake is longer than the required length
            if (this.cells.length > initialSnakeLength) {
                this.cells.pop();
            }
        }

        draw() {
            context.fillStyle = "green";
            this.cells.forEach((cell) => {
                context.fillRect(cell.x, cell.y, gridSize, gridSize);
            });
        }

        setDirection(direction: string) {
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
        }
    }

    // Define the food class
    class Food {
        x: number;
        y: number;

        constructor() {
            this.x = getRandomPosition(canvasWidth);
            this.y = getRandomPosition(canvasHeight);
        }

        draw() {
            context.fillStyle = "red";
            context.fillRect(this.x, this.y, foodSize, foodSize);
        }
    }

    // Utility function to generate random positions for the food
    function getRandomPosition(max: number) {
        return Math.floor(Math.random() * max / gridSize) * gridSize;
    }

    // Create the snake object
    const snake = new Snake();

    let food = new Food();

    // Handle keyboard input
    document.addEventListener("keydown", (event) => {
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
            const tail = { x: snake.cells[0].x, y: snake.cells[0].y };
            snake.cells.push(tail);

            // Create new food
            food = new Food();
        }

        setTimeout(gameLoop, snakeSpeed);
    }

    // Start the game loop
    gameLoop();
});