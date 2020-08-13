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
# If you don't want to break the game, don't set velocity higher than ball radius
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

    velocity_y = VELOCITY_Y # Makes life sooooo easier
    velocity_x = random.randint(VELOCITY_X_MIN, VELOCITY_X_MAX) * random.choice([-1, 1])
    miss = 0 # Better keep it that way
    hit = 0

    bricks = setup(c)  # Bricks is list of all bricks on the screen
    paddle, paddle_y = setup_paddle(c)  # Paddle is object for paddle, paddle_y to keep him on same y when moving
    ball = setup_ball(c, miss)  # Ball is object for ball

    while miss < NTURNS and hit < NBRICK_ROWS*NBRICK_COLUMNS:
        move_ball(c, ball, velocity_x, velocity_y)
        objects = c.find_overlapping(c.get_left_x(ball),c.get_top_y(ball),c.get_left_x(ball)+BALL_RADIUS,c.get_top_y(ball)+BALL_RADIUS)

        for crashed in objects:
            for brick in bricks:
                if crashed == brick:
                    hit += 1
                    velocity_x, velocity_y = complex_collision_calculator(c, ball, brick, velocity_x, velocity_y)
            if crashed == paddle:
                if (c.get_top_y(ball) + BALL_RADIUS/2) < (c.get_top_y(paddle) + PADDLE_HEIGHT/2):
                    velocity_y = -velocity_y

        velocity_x = check_walls(c, ball, velocity_x)
        velocity_y = check_ceiling(c, ball, velocity_y)
        if c.get_top_y(ball)+BALL_RADIUS >= c.get_canvas_height()-velocity_y:
            # Checks for contact with floor
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
    Inside: Puts ball in the middle of the screen, sets black. Waits till user clicks, unless user made third mistake
    Input: canvas, mistakes
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
    """
    animation of moving ball
    Inside: moves ball by its delta x and y
    Input: canvas, object ball, ball x velocity, ball y velocity
    """
    c.move(ball, ball_x, velocity_y)
    c.update()


def check_walls(c, ball, ball_x):
    """
    Checks for walls on the side. Trying to avoid ball touching side, so it prevents collision before it happens
    Inside: Checks if the ball is going to hit any of the side walls in the next animation.
            If yes, it inverts ball's x_velocity and moves him VELOCITY_MAX pixels away from wall, preventing loop.
    Input: canvas, object ball, ball x velocity
    Output: Returns new/old ball velocity
    """
    if c.get_left_x(ball) < VELOCITY_X_MAX or c.get_left_x(ball) + BALL_RADIUS > c.get_canvas_width() - VELOCITY_X_MAX:
        unit = ball_x // abs(ball_x)
        ball_x = random.randint(VELOCITY_X_MIN, VELOCITY_X_MAX) * -unit
        c.move(ball, VELOCITY_X_MAX*-unit, 0)
    return ball_x


def check_ceiling(c, ball, velocity_y):
    """
    Does the same as check_walls, but for ceiling
    Inside: Check if the ball hits the ceiling in the next move. If yes, it inverts its y velocity
    Input: canvas, object ball, ball y velocity
    Output: Ball's new/old y velocity
    """
    if c.get_top_y(ball) <= velocity_y and velocity_y//abs(velocity_y) < 0:
        return -velocity_y
    return velocity_y


def complex_collision_calculator(c, ball, brick, velocity_x, velocity_y):
    """
    Makes ball bounce feel more natural. When ball hits corner or side of brick, it inverts just some velocity vectors
    Inside: Calculates brick corner and ball middle, checks for position of ball relative to brick to invert just some
            vectors. Also deletes visual representation of brick on canvas.
    Input: canvas, object ball, object brick, ball velocity x, ball velocity y
    Output: new/old x and y vectors
    """
    ball_middle_x = c.get_left_x(ball) + BALL_RADIUS/2
    ball_middle_y = c.get_top_y(ball) + BALL_RADIUS/2

    brick_x1 = c.get_left_x(brick)
    brick_x2 = c.get_left_x(brick) + BRICK_WIDTH
    brick_y1 = c.get_top_y(brick)
    brick_y2 = c.get_top_y(brick) + BRICK_WIDTH

    c.delete(brick)

    if ball_middle_x > brick_x2:
        if ball_middle_y > brick_y2:
            return random.randint(VELOCITY_X_MIN, VELOCITY_X_MAX), VELOCITY_Y
        elif ball_middle_y > brick_y1:
            return -velocity_x, velocity_y
        else:
            return random.randint(VELOCITY_X_MIN, VELOCITY_X_MAX), -VELOCITY_Y
    elif ball_middle_x > brick_x1:
        return velocity_x, -velocity_y
    else:
        if ball_middle_y > brick_y2:
            return -random.randint(VELOCITY_X_MIN, VELOCITY_X_MAX), VELOCITY_Y
        elif ball_middle_y > brick_y1:
            return -velocity_x, velocity_y
        else:
            return -random.randint(VELOCITY_X_MIN, VELOCITY_X_MAX), -VELOCITY_Y


if __name__ == '__main__':
    main()
