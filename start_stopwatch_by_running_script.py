#----
# install packages first
# ----
# pip install SimpleGUICS2Pygame


# import modules
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# define global variables
integer = 0
x = 0
y = 0
tenths = 0


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    min = t // 600
    secs = t // 10 - min * 60
    global tenths
    tenths = t % 10
    if secs < 10:
        return str(min) + ":" + "0" + str(secs) + "." + str(tenths)
    else:
        return str(min) + ":" + str(secs) + "." + str(tenths)


# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()


def stop():
    global x, y
    if timer.is_running():
        y += 1
        if tenths % 10 == 0:
            x += 1
    timer.stop()


def reset():
    global integer, x, y
    integer = 0
    x = 0
    y = 0


# define event handler for timer with 0.1 sec interval
def timer_handler():
    global integer
    integer += 1


# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(integer), (50, 110), 42, "white")
    canvas.draw_text(str(x) + "/" + str(y), (125, 40), 32, "green")


# create frame
frame = simplegui.create_frame("Stopwatch", 200, 200)
frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(100, timer_handler)

# register event handlers
frame.add_button("Start", start, 200)
frame.add_button("Stop", stop, 200)
frame.add_button("Reset", reset, 200)

# start frame
frame.start()

