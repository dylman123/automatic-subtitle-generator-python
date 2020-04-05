from scripts import render

# Import static text from assets
TEXT = render.static_text["user_inputs"]
file_types = TEXT["file_types"]
button_texts = TEXT["button"]
instruction_texts = TEXT["instructions"]
verify_errors = TEXT["verify_errors"]

file_paths = []  # A list of strings which contains the input file paths
num_speakers = 0  # An integer to represent how many speakers are in the clip

def get_callback(fn):
    '''To pass the program_ctrl() function into this module.'''
    global callback
    callback = fn

def get_video_name(path):
    '''
    Extracts the name of the video from it's file path.
    Output: string which contains the video name.
    '''
    name = path.split("/")[-1].split(".")[0]
    return name

def get_value(ctrl):
    '''
    Reads the string which is inputted in the textbox.
    Output: num_speakers is updated (an int containing the number of speakers
    in the video clip, which is a global variable).
    '''
    global num_speakers, callback
    try:
        num_speakers = int(render.string_in.get())
        callback()
    except:
        error = verify_errors[ctrl]
        render.draw_error(error, x=0.5, y=0.9)

def select_num_speakers(ctrl):
    '''
    Draws a button for the user to click.
    It also draws a textbox and instruction for the user.
    Output: triggers a lambda function get_value.
    '''
    text = instruction_texts[ctrl]
    render.draw_info(text=text, x=0.5, y=0.3)
    render.draw_textbox(x=0.5, y=0.5)
    render.draw_button(text="Enter", x=0.5, y=0.7, command=lambda:get_value(ctrl))

def verify_file(ctrl, file_path):
    '''
    Ensures that the file selected is valid.
    Output: file_paths is updated (a list containing all the imported files, which is a global variable).
    '''
    chosen_ext = file_path.split(".")[-1]
    for i in range(len(file_types[ctrl])):
        valid_ext = file_types[ctrl][i][1].split(".")[-1]
        if chosen_ext == valid_ext:   
            file_paths.append(file_path)
            callback()
        else: pass

def select_file(ctrl):
    '''
    Opens a dialog box for the user to select a file from disk.
    Output: file_path (a string which contains the path of the selected file)
    '''
    text = instruction_texts[ctrl]
    exts = []
    for ext in file_types[ctrl]:
        exts.append(tuple(ext))
    file_path = render.ask_open_file(text, tuple(exts))
    verify_file(ctrl, file_path)

def import_file(ctrl):
    '''
    Draws a button for the user to click.
    Output: triggers a lambda function select_file.
    '''
    text = button_texts[ctrl]
    render.draw_button(text=text, x=0.5, y=0.5, command=lambda:select_file(ctrl))
