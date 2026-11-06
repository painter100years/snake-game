try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, None, bg = "black", width=WINDOW_HEIGHT, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
snake_body = []
velocityX = 0
velocityY = 0
game_over = False
score = 0

special_food = None
effect_active = None
effect_timer = 0

BASE_DELAY = 100
current_delay = BASE_DELAY

def change_direction(e):

    if effect_active == "invert":
        if e.keysym == "Up":
            e.keysym = "Down"
        elif e.keysym == "Down":
            e.keysym = "Up"
        elif e.keysym == "Left":
            e.keysym = "Right"
        elif e.keysym == "Right":
            e.keysym = "Left"

    if (game_over):
        if e.keysym == "Return" or e.keysym == "space":
            reset_game()
        return

    global velocityX
    global velocityY

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

def activate_random_effect():
    global effect_active, effect_timer, current_delay

    effects = ["speed", "slow", "invert", "double"]
    effect_active = random.choice(effects)
    effect_timer = 50

    if effect_active == "speed":
        current_delay = 50
    elif effect_active == "slow":
        current_delay = 150

def reset_effect():
    global effect_active, current_delay
    effect_active = None
    current_delay = BASE_DELAY

def move():
    global snake, food, snake_body, game_over, score, special_food, effect_timer
    if (game_over):
        return
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= window_height):
        game_over = True
        return
    for tile in snake_body:
        if(snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
    
    if (snake.x == food.x and snake.y == food.y):
        if random.random() < 0.2:
            special_food = Tile(
                random.randint(0, COLS - 1) * TILE_SIZE,
                random.randint(0, ROWS - 1) * TILE_SIZE
            )
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        if effect_active == "double":
            score += 1
            snake_body.append(Tile(food.x, food.y))
        score += 1
    if special_food and snake.x == special_food.x and snake.y == special_food.y:
        activate_random_effect()
        special_food = None

    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

    if effect_active:
        effect_timer -= 1
        if effect_timer <= 0:
            reset_effect()

def draw():
    global snake, food, snake_body, game_over, score, high_score
    move()
    canvas.delete("all")
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")

    if effect_active == "invert":
        canvas.create_text(WINDOW_WIDTH / 2, 20, font = "Arial 20", text="Controls Inverted", fill="white")
    elif effect_active == "slow":
        canvas.create_text(WINDOW_WIDTH / 2, 20, font = "Arial 20", text="Slowed Down", fill="white")
    elif effect_active == "speed":
        canvas.create_text(WINDOW_WIDTH / 2, 20, font = "Arial 20", text="Sped Up", fill="white")
    elif effect_active == "double":
        canvas.create_text(WINDOW_WIDTH / 2, 20, font = "Arial 20", text="Double Points", fill="white")
    
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")
    if special_food:
        canvas.create_rectangle(special_food.x, special_food.y, special_food.x + TILE_SIZE, special_food.y + TILE_SIZE, fill="gold")
    if (game_over):
        if score > high_score:
            high_score = score
            with open("highscore.txt", "w") as f:
                f.write(str(high_score))
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font = "Arial 20", text=f"Game Over: {score}", fill="white")
        canvas.create_text(WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 1.8), font = "Arial 7", text="SPACE TO PLAY AGAIN", fill="white")
    else:
        canvas.create_text(30, 20, font="Arial 10", text = f"Score: {score}", fill="white")
        canvas.create_text(45, 40, font="Arial 10", text = f"High-score: {high_score}", fill="white")

    window.after(current_delay, draw)

def reset_game():
    global snake, food, snake_body, score, game_over, velocityX, velocityY

    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
    food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
    snake_body = []

    velocityX = 0
    velocityY = 0

    score = 0
    game_over = False

draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()