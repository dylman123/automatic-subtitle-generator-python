import render
import subprocess
from PIL import ImageTk, Image
import __init__

TEXT = render.static_text["select_speaker"]
INSTRUCTION = TEXT["instructions"]
NUM_SPEAKERS = 0
click = 1
coords = []

def create_title():
    '''Draws a title to instruct the user.'''
    global INSTRUCTION, click
    instruction = INSTRUCTION.replace("{speaker}", str(click))
    render.draw_large_text(text=instruction, x=20, y=10, click=click)

def on_click(eventorigin):
    '''On a mouse click, a dot is rendered and the speaker selection is incremented.'''
    global NUM_SPEAKERS, x, y, click, coords
    # Get the cursor coordinates
    x = eventorigin.x
    y = eventorigin.y
    r = 10
    # FCP requires coords to be relative to centre of frame.
    coords.append((x-render.WIDTH/2, render.HEIGHT/2-y))
    # Render a coloured dot and titles
    render.draw_circle(x, y, r, click)
    render.clear_canvas_text()
    if click < NUM_SPEAKERS:
        click += 1
        create_title()
    elif click >= NUM_SPEAKERS:
        render.draw_button(text="Next", x=0.98, y=0.02, command=__init__.program_ctrl)

def position_subs(num_speakers):
    '''Creates a clickable/interactive area to position subtitles.'''
    global NUM_SPEAKERS, click
    click = 1
    NUM_SPEAKERS = num_speakers
    create_title()
    # Bind the canvas to a mouse click
    render.canvas.bind("<Button 1>", on_click)

def screengrab(video_path, image_path):
    '''Grabs an image from the first frame of the video.'''
    command = f'ffmpeg -i {video_path} -ss 00:00:00.000 -vframes 1 {image_path}'
    subprocess.call(command, shell=True)

    # Open image from path
    img = Image.open(image_path)
    # Set geometry
    WIDTH, HEIGHT = img.size
    scale = 1
    WIDTH = int(WIDTH * scale)
    HEIGHT = int(HEIGHT * scale)
    render.set_size(WIDTH, HEIGHT)
    # Creates a Tkinter-compatible photo image
    photo_img = ImageTk.PhotoImage(img)
    # The Canvas widget is a standard Tkinter widget used to display graphical items
    render.draw_canvas(WIDTH, HEIGHT)
    # Insert the image onto the canvas
    render.draw_image(photo_img)

def get_examples_for_speaker(df_captions, speaker_tag, q=7):
    '''
    Returns a speaker's first "q" captions in the clip as a list. 
    Default value of "q" = 7.
    Used to capture examples of a speaker's captions.
    '''
    
    captions_list = []
    count = 0
    
    for idx in range(len(df_captions)):
        if df_captions.iloc[idx, 4] == speaker_tag and count < q:
            captions_list.append(df_captions.iloc[idx, 3])
            count += 1
        if count >= q:
            break
            
    return captions_list
