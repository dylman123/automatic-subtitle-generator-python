from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog
import json
import time

def get_callback(next_fn, back_fn):
    '''To pass the program_ctrl() and decrement_ctrl() functions into this module.'''
    global next_callback, back_callback
    next_callback = next_fn
    back_callback = back_fn

def read_static_text():
    '''Returns dict of the static text file'''
    global static_text
    with open("assets/static_text.json") as f:
        static_text = json.load(f)

def ask_open_file(title, filetypes):
    return filedialog.askopenfilename(initialdir=".", title=title, filetypes=filetypes)

def draw_scrollable(text, x, y, width, height, anchor=SW):
    global root, scroll, scrollable
    barwidth = draw_scrollbar()
    scrollable = Text(root, wrap=WORD, yscrollcommand=scroll.set)
    scrollable.place(relx=x,rely=y,anchor=anchor,width=width-barwidth,height=height)
    scrollable.insert(END, text)
    scrollable.config(yscrollcommand=scroll.set)  # attach scrollbar to text
    scroll.config(command=scrollable.yview)

def draw_scrollbar():
    global root, scroll
    scroll = Scrollbar(root)
    scroll.pack(side=RIGHT, fill=Y)
    barwidth = 15
    return barwidth

def draw_button(text, x, y, command, anchor=CENTER, wraplength=0):
    global root, buttons
    button = Button(root, text=text, wraplength=wraplength, anchor=CENTER, command=command)
    button.place(relx=x, rely=y, anchor=anchor)
    buttons.append(button)

def draw_back(steps):
    draw_button(text="Back", x=0.02, y=0.02, anchor=NW, command=lambda:back_callback(steps))

def draw_next():
    draw_button(text="Next", x=0.98, y=0.02, anchor=NE, command=next_callback)

def draw_info(text, x, y, font="Default", anchor=CENTER, justify=CENTER):
    global root, info
    info = Label(root, text=text, font=font, justify=justify)
    info.place(relx=x, rely=y, anchor=anchor)

def draw_error(text, x, y, anchor=CENTER):
    global root, error
    try: error.destroy()
    except: pass
    error = Label(root, text=text)
    error.place(relx=x, rely=y, anchor=anchor)

def draw_textbox(x, y, width=5, anchor=CENTER):
    global root, string_in, textbox
    string_in = StringVar()
    textbox = Entry(root, width=width, textvariable=string_in)
    textbox.place(relx=x, rely=y, anchor=anchor)

def draw_progress_bar(x=0.5, y=0.6, anchor=CENTER):
    global root, progress, step_size, new_bar, bar_offset, bar_step
    text = static_text["progress_bar"]  # Import static text from assets
    draw_info(text[bar_step], x=x, y=y-0.3)
    progress = Progressbar(root, orient = HORIZONTAL, length = WIDTH/2, mode = 'determinate') 
    progress.place(relx=x, rely=y, anchor=anchor)
    progress.step(bar_step * step_size)
    bar_step += 1
    progress.update()
    time.sleep(0.5)

def draw_canvas(width, height):
    global root, canvas
    canvas = Canvas(root, width=width, height=height)
    canvas.pack(side="bottom", fill="both", expand="no")

def draw_image(image):
    '''Draws image onto the canvas.'''
    global root, canvas
    root.image = image  # Prevent image garbage collection
    canvas.create_image(0, 0, anchor=NW, image=image)

def draw_circle(x, y, r, click):
    global canvas, colours
    canvas.create_oval(x-r,y-r,x+r,y+r, fill=colours[click-1])

def draw_large_text(text, x, y, click, anchor=NW):
    '''Draws large text onto the canvas.'''
    global canvas, large_text, colours
    large_text = canvas.create_text(x, y, anchor=anchor, width=WIDTH-100, text=text, font=("Purisa", 20, "bold"), fill=colours[click-1])

def draw_small_text(text):
    '''Draws small text onto the canvas.'''
    global canvas, small_text
    pass

def clear_canvas_text():
    global canvas, large_text, small_text
    for item in large_text, small_text:
        try: 
            canvas.delete(item)
        except: pass

def clear_window():
    global buttons, back, info, textbox, error, string_in, progress, scroll, scrollable, canvas
    for item in buttons, back, info, textbox, error, progress, scroll, scrollable, canvas:
        try:  # If item is a tkinter element
            item.destroy()
        except: pass
        try:  # If item is a list
            for element in item:
                element.destroy()
        except: pass
        string_in = ""

def set_size(width, height):
    global root, WIDTH, HEIGHT
    WIDTH = width
    HEIGHT = height
    root.geometry(f"{width}x{height}")
    root.resizable(width=False, height=False)

def start():
    global root, WIDTH, HEIGHT
    root = Tk()
    root.title(static_text["title"])
    set_size(WIDTH, HEIGHT)

def reset_size():
    global initial_width, initial_height
    set_size(initial_width, initial_height)

# Set initial window geometry
initial_width = 500
initial_height = 200
WIDTH = initial_width
HEIGHT = initial_height

# Initialisation functions and variables
'''Variables can be tkinter elements or a list of tkinter elements.'''
read_static_text()
buttons = []
back = None
info = None
textbox = None
string_in = ""
error = None
progress = None
new_bar = True  # Flag to indicate a new progress bar
bar_offset = 0  # To control where progress bar begins in the program
step_size = 99.99 / (len(static_text["progress_bar"])-1)  # As a %
bar_step = 0  # To count progress bar steps
scroll = None
scrollable = None
canvas = None
colours = ["red", "blue", "yellow", "green", "purple", "pink", "white", "orange"] 
large_text = None
small_text = None
start()