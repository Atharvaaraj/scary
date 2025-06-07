const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const ground = canvas.height - 20;

let player = {
    x: 50,
    y: ground,
    vy: 0,
    width: 20,
    height: 30,
    jumping: false
};

let obstacles = [];
let obstacleTimer = 0;
let gameOver = false;

function jump() {
    if (!player.jumping) {
        player.vy = -10;
        player.jumping = true;
    }
}

function createObstacle() {
    const height = 20 + Math.random() * 30;
    obstacles.push({
        x: canvas.width,
        y: ground,
        width: 20,
        height: height
    });
}

function update() {
    if (gameOver) return;

    // gravity
    player.vy += 0.5;
    player.y += player.vy;
    if (player.y >= ground) {
        player.y = ground;
        player.vy = 0;
        player.jumping = false;
    }

    obstacleTimer += 1;
    if (obstacleTimer > 90) {
        createObstacle();
        obstacleTimer = 0;
    }

    for (let i = 0; i < obstacles.length; i++) {
        obstacles[i].x -= 3;
        if (
            player.x < obstacles[i].x + obstacles[i].width &&
            player.x + player.width > obstacles[i].x &&
            player.y < obstacles[i].y &&
            player.y + player.height > obstacles[i].y - obstacles[i].height
        ) {
            gameOver = true;
        }
    }

    obstacles = obstacles.filter(ob => ob.x + ob.width > 0);
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#0f0';
    ctx.fillRect(player.x, player.y - player.height, player.width, player.height);

    ctx.fillStyle = '#f00';
    obstacles.forEach(ob => {
        ctx.fillRect(ob.x, ob.y - ob.height, ob.width, ob.height);
    });

    ctx.fillStyle = '#fff';
    ctx.fillText('Click or press space to jump', 10, 20);

    if (gameOver) {
        ctx.fillStyle = '#fff';
        ctx.fillText('Game Over! Refresh to try again.', 200, 100);
    }
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

canvas.addEventListener('click', jump);
window.addEventListener('keydown', (e) => {
    if (e.code === 'Space') jump();
});

loop();
