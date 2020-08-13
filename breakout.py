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
VELOCITY_X_MIN = 2.0
VELOCITY_X_MAX = 6.0

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

    bricks = setup(c) # Bricks is list of all bricks on the screen

    c.mainloop()

def setup(c):
    """
    Initializes whole playground with all columns in correct position and color
    Inside: Builds all bricks on the screen and sets their color
    Input: canvas
    Output: returns list of bricks
    """
    bricks = []
    for i in range(NBRICK_ROWS):
        y = BRICK_Y_OFFSET + i * (BRICK_HEIGHT + BRICK_SEP)
        for j in range(NBRICK_COLUMNS):
            x = int(j * (BRICK_WIDTH + BRICK_SEP) + (c.get_canvas_width()/2 - (NBRICK_COLUMNS*BRICK_WIDTH + (NBRICK_COLUMNS-1)*BRICK_SEP)/2))
            brick = c.create_rectangle(x, y, x+BRICK_WIDTH, y+BRICK_HEIGHT)
            if i < 0.2 * NBRICK_ROWS:
                color = "red"
            elif i < 0.4 * NBRICK_ROWS:
                color = "orange"
            elif i < 0.6 * NBRICK_ROWS:
                color = "yellow"
            elif i < 0.8 * NBRICK_ROWS:
                color = "green"
            else:
                color = "cyan"
            c.set_color(brick, color)
            bricks.append(brick)
    return bricks




if __name__ == '__main__':
    main()
