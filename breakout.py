import math
from graphics import Canvas
import random
import time

CANVAS_WIDTH = 420
CANVAS_HEIGHT = 600

# Stage 1: Set up the Bricks

# Number of bricks in each row
NBRICK_COLUMNS = 10

# Number of rows of bricks
NBRICK_ROWS = 10

# Separation between neighboring bricks, in pixels
BRICK_SEP = 4

# Width of each brick, in pixels
BRICK_WIDTH = math.floor((CANVAS_WIDTH - (NBRICK_COLUMNS + 1.0) * BRICK_SEP) / NBRICK_COLUMNS)

# Height of each brick, in pixels
BRICK_HEIGHT = 8

# Offset of the top brick row from the top, in pixels
BRICK_Y_OFFSET = 70

# Stage 2: Create the Bouncing Ball

# Radius of the ball in pixels
BALL_RADIUS = 10

# The ball's vertical velocity.
VELOCITY_Y = 6.0

# The ball's minimum and maximum horizontal velocity; the bounds of the
# initial random velocity that you should choose (randomly +/-).
VELOCITY_X_MIN = 2
VELOCITY_X_MAX = 6

# Animation delay or pause time between ball moves (in seconds)
DELAY = 1 / 60

# Stage 3: Create the Paddle

# Dimensions of the paddle
PADDLE_WIDTH = 60
PADDLE_HEIGHT = 10

# Offset of the paddle up from the bottom
PADDLE_Y_OFFSET = 30

# Stage 5: Polish and Finishing Up

# Number of turns
NTURNS = 3

BOUNCE_SOUND = "bounce.au"


def main():
    c = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    c.set_canvas_title("Breakout")

    velocity_y = VELOCITY_Y
    miss = 0
    ball_x = random.randint(VELOCITY_X_MIN, VELOCITY_X_MAX) * random.choice([-1, 1])
    hit = 0

    bricks = setup(c)  # Bricks is list of all bricks on the screen
    paddle, paddle_y = setup_paddle(c)  # Paddle is object for paddle
    ball = setup_ball(c, miss)  # Ball is object for ball

    while miss < NTURNS and hit < NBRICK_ROWS*NBRICK_COLUMNS:
        move_ball(c, ball, ball_x, velocity_y)
        objects = c.find_overlapping(c.get_left_x(ball), c.get_top_y(ball), c.get_left_x(ball) + BALL_RADIUS, c.get_top_y(ball) + BALL_RADIUS)
        for crashed in objects:
            for brick in bricks:
                if crashed == brick:
                    c.delete(brick)
                    hit += 1
                    velocity_y = - velocity_y
            if crashed == paddle:
                if (c.get_top_y(ball) + BALL_RADIUS/2) < (c.get_top_y(paddle) + PADDLE_HEIGHT/2):
                    velocity_y = -velocity_y

        ball_x = check_walls(c, ball, ball_x)
        velocity_y = check_ceiling(c, ball, velocity_y)

        if c.get_top_y(ball)+BALL_RADIUS >= c.get_canvas_height()-velocity_y:
            miss += 1
            c.delete(ball)
            ball = setup_ball(c, miss)

        c.update()
        time.sleep(DELAY)
        mouse_x = c.get_mouse_x()
        c.moveto(paddle, mouse_x - PADDLE_WIDTH//2, paddle_y)

    c.mainloop()


def setup(c):
    """
    Initializes whole playground with all columns in correct position and color
    Inside: Builds all bricks on the screen and sets their color
    Input: canvas
    Output: returns list of bricks
    """
    bricks = []
    color = ["red", "orange", "yellow", "lime green", "cyan"]
    for i in range(NBRICK_ROWS):
        y = BRICK_Y_OFFSET + i * (BRICK_HEIGHT + BRICK_SEP)
        for j in range(NBRICK_COLUMNS):
            x = int(j * (BRICK_WIDTH + BRICK_SEP) + (c.get_canvas_width() / 2 - (
                        NBRICK_COLUMNS * BRICK_WIDTH + (NBRICK_COLUMNS - 1) * BRICK_SEP) / 2))
            brick = c.create_rectangle(x, y, x + BRICK_WIDTH, y + BRICK_HEIGHT)
            c.set_color(brick, color[i // 2])
            bricks.append(brick)
    return bricks


def setup_ball(c, miss):
    """
    Creates ball and sets his color
    Inside: Puts ball in the middle of the screen, sets black. Waits till user clicks.
    Input: canvas
    Output: Returns ball as an object
    """
    x = c.get_canvas_width() / 2 - BALL_RADIUS / 2
    y = c.get_canvas_height() / 2
    ball = c.create_oval(x, y, x + BALL_RADIUS, y + BALL_RADIUS)
    c.set_color(ball, "black")
    if miss < 3:
        c.wait_for_click()
    return ball


def setup_paddle(c):
    """
    Creates paddle in the middle
    Inside: Sets paddle
    Input: canvas
    Output: Returns paddle as an object, his y coordinate as int
    """
    x = c.get_canvas_width() / 2 - PADDLE_WIDTH / 2
    y = c.get_canvas_height() - PADDLE_Y_OFFSET - PADDLE_HEIGHT
    paddle = c.create_rectangle(x, y, x + PADDLE_WIDTH, y + PADDLE_HEIGHT)
    c.set_color(paddle, "black")
    return paddle, y


def move_ball(c, ball, ball_x, velocity_y):
    c.move(ball, ball_x, velocity_y)
    c.update()


def check_walls(c, ball, ball_x):
    if c.get_left_x(ball) < VELOCITY_X_MAX or c.get_left_x(ball) + BALL_RADIUS > c.get_canvas_width() - VELOCITY_X_MAX:
        unit = ball_x // abs(ball_x)
        ball_x = random.randint(VELOCITY_X_MIN, VELOCITY_X_MAX) * -unit
        c.move(ball, VELOCITY_X_MAX*-unit, 0)
    return ball_x


def check_ceiling(c, ball, velocity_y):
    if c.get_top_y(ball) <= velocity_y and velocity_y//abs(velocity_y) < 0:
        return -velocity_y
    return velocity_y


if __name__ == '__main__':
    main()
