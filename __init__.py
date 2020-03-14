# Import Python modules
import render
import os
import glob
import pathlib
from tkinter import Button, CENTER, NW

# Import modules in this project
import automatic_subtitle_generator.user_inputs as ui
import automatic_subtitle_generator.signal_processing as sp
import automatic_subtitle_generator.speech_to_text as s2t
import automatic_subtitle_generator.generate_subs as gs
import automatic_subtitle_generator.select_speaker as ss
import automatic_subtitle_generator.modify_xml as mx

# Initialise global variables
CTRL = -1  # Program control counter
temp_dir = "temp"  # Path to temp directory
output_dir = "output"  # Path to output directory
video_path = ""  # Path to imported video file
video_name = ""  # Name of imported video file
xml_path = ""  # Path to imported xml file
audio_path = f'{temp_dir}/audio_raw.wav'  # Path to extracted raw audio file
mono_path = f'{temp_dir}/audio_mono.wav'  # Path to extracted mono audio file
wd = str(pathlib.Path().absolute())  # Current working directory
google_creds = wd + "/assets/google_creds.json"  # Path to GCP creds
df_words = None  # Dataframe to store response of GCP API
df_subs = None  # Dataframe to store individual subtitles
image_path = f'{temp_dir}/screenshot.png'  # Path to screenshot image file
template_path = "assets/title_template.fcpxml"  # Path to XML template for a title

def restart():
    '''User to restart program once the end has been reached.'''
    global CTRL
    CTRL = -1
    render.bar_step = 0
    ui.file_paths = []
    program_ctrl()

def decrement_ctrl(steps):
    '''CTRL is decremented when user clicks "Back".'''
    global CTRL
    CTRL -= (steps+1)
    render.bar_step = 0
    program_ctrl()

def back_button(steps, x=30, y=20):
    '''Draws a back button.'''
    render.back = Button(render.root, text="Back", anchor=CENTER, command=lambda:decrement_ctrl(steps))
    render.back.place(x=x, y=y, anchor=CENTER)

def program_ctrl():
    '''Controls the program flow.'''
    global CTRL, video_path, video_name, xml_path, df_words, df_subs, image_path
    render.clear_window()
    CTRL += 1
    if CTRL == 0:  # Import video file
        ui.import_file(CTRL)
    elif CTRL == 1:  # Import XML file
        back_button(1)
        video_path = ui.file_paths[0]
        video_name = ui.get_video_name(path=video_path)
        ui.import_file(CTRL)  
    elif CTRL == 2:  # Select number of speakers
        back_button(1)
        render.set_size(render.initial_width, render.initial_height)
        xml_path = ui.file_paths[1]
        ui.select_num_speakers(CTRL)  
    elif CTRL == 3:  # Signal processing
        make_temp_dir()
        render.draw_progress_bar()
        sp.convert_to_wav(video_path=video_path, audio_path=audio_path)
        sp.convert_to_mono(stereo_path=audio_path, mono_path=mono_path)
        program_ctrl()
    elif CTRL == 4:  # Speech to text Google API
        render.draw_progress_bar()
        s2t.set_env_variable(path=google_creds)
        response = s2t.sample_long_running_recognize(path=mono_path, num_speakers=ui.num_speakers)
        df_words = s2t.create_dataframe(response=response)
        program_ctrl()
    elif CTRL == 5:  # Generate subtitles
        render.draw_progress_bar()
        df_subs = gs.create_captions(df_words,  word_limit=7)
        program_ctrl()
    elif CTRL == 6:  # Continue button
        back_button(4)
        render.draw_progress_bar()
        render.draw_button(text="Next",x=0.5,y=0.8,command=program_ctrl)
    elif CTRL == 7:  # Display subtitles
        gs.display_captions(df_subs)
        back_button(5, x=render.WIDTH-85, y=21)
    elif CTRL == 8:  # Select speaker
        make_temp_dir()
        ss.screengrab(video_path=video_path, image_path=image_path)
        ss.position_subs(num_speakers=ui.num_speakers)
        back_button(1, x=render.WIDTH-100, y=22)
    elif CTRL == 9:  # Modify and save XML file
        render.set_size(render.initial_width, render.initial_height)
        render.draw_progress_bar()
        mx.modify_xml(xml_path=xml_path, template_path=template_path, captions=df_subs, coords=ss.coords)
        mx.save_xml(video_name=video_name, output_dir=output_dir)
        program_ctrl()
    elif CTRL == 10:  # Save XML file
        render.draw_button(text=render.static_text["newclip"],x=0.5, y=0.5, command=restart)

def make_temp_dir():
    '''Makes a directory named "temp".'''
    global temp_dir
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    else:
        files = glob.glob(f"{temp_dir}/*")
        for f in files:
            os.remove(f)

def make_output_dir():
    '''Makes a directory named "output". The outputted XML files will be saved here.'''
    global output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
