#----
# install packages first
# ----
# pip install SimpleGUICS2Pygame


import random
import time
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


#----
# initialize globals - encode positional info for paddles
#----
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 17
PAD_WIDTH = 8
PAD_HEIGHT = 90
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True


#----
# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
#----
def spawn_ball(direction):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    x1 = random.randrange(130, 250)
    x2 = random.randrange(80, 190)
    if direction == RIGHT:
        ball_vel = [x1 / 60, - x2 / 60]
    elif direction == LEFT:
        ball_vel = [- x1 / 60, - x2 / 60]


#----
# define event handlers
#----
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    global score1, score2  # these are integers
    score1 = 0
    score2 = 0
    direction = random.choice([True, False])
    spawn_ball(direction)


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "white")

    ball_acc = 0.1  ## SPECIFY acceleration factor

    # update ball
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]

    # determine whether paddle and ball collide
    if (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH
            and paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] + BALL_RADIUS
            and ball_pos[1] - BALL_RADIUS <= paddle1_pos + HALF_PAD_HEIGHT):
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] = ball_vel[0] * (1 + ball_acc)
        ball_vel[1] = ball_vel[1] * (1 + ball_acc)
    elif ball_pos[0] <= 0:
        score2 += 1
        spawn_ball(RIGHT)
    if (ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH
            and paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] + BALL_RADIUS
            and ball_pos[1] - BALL_RADIUS <= paddle2_pos + HALF_PAD_HEIGHT):
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] = ball_vel[0] * (1 + ball_acc)
        ball_vel[1] = ball_vel[1] * (1 + ball_acc)
    elif ball_pos[0] >= WIDTH:
        score1 += 1
        spawn_ball(LEFT)

    # draw ball
    time.sleep(0.01)
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "white", "white")

    # update paddle's vertical position, keep paddle on the screen
    if (HALF_PAD_HEIGHT <= paddle2_pos + paddle2_vel
            <= HEIGHT - HALF_PAD_HEIGHT):
        paddle2_pos += paddle2_vel
    if (HALF_PAD_HEIGHT <= paddle1_pos + paddle1_vel
            <= HEIGHT - HALF_PAD_HEIGHT):
        paddle1_pos += paddle1_vel

    # draw paddles
    canvas.draw_line((HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT), \
                     (HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT), \
                     PAD_WIDTH, 'white')
    canvas.draw_line((WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), \
                     (WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT), \
                     PAD_WIDTH, 'white')

    # draw scores
    canvas.draw_text(str(score1), [200, 100], 60, "White")
    canvas.draw_text(str(score2), [360, 100], 60, "White")


def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 7
    if key == simplegui.KEY_MAP["up"] and paddle1_pos > 0:
        paddle2_vel -= acc
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += acc


def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0


def button_handler():
    new_game()


#----
# create frame
#----
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", button_handler, 200)


#----
# start frame
#----
new_game()
frame.start()

