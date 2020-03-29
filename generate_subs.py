import pandas as pd
import render
import os, sys, subprocess
import __init__

def create_captions(df_in, word_limit=7):
    '''
    Takes a dataframe of individual words as input and applies logic
    to output a new dataframe. However instead of individual words per row,
    there will now be entire captions per row of the new pandas dataframe.
    The phrases are differentiated based on speaker identities, any pauses in the audio,
    as well as a word limit per caption. Default word_limit per caption is 7.
    '''
    columns = ["Start (secs)",
               "End (secs)",
               "Duration (secs)",
               "Captions",
               "Speaker"]
    df_out = pd.DataFrame(columns=columns)  # Create a new dataframe
    row = 0  # Row counter
    consecutive = 0  # To track how many consecutive words in a caption
    
    for idx in range(len(df_in)):
        start_s = df_in.iloc[idx,0]  # Find the current timestamp
        start_ns = df_in.iloc[idx,1]  # Find the current timestamp
        start = start_s + start_ns / 1e9  # Combine into 1 time value
        
        end_s = df_in.iloc[idx,2]  # Find the current timestamp
        end_ns = df_in.iloc[idx,3]  # Find the current timestamp
        end = end_s + end_ns / 1e9  # Combine into 1 time value
        
        prev_end_s = df_in.iloc[idx-1,2]  # Find the previous end timestamp
        prev_end_ns = df_in.iloc[idx-1,3]  # Find the previous end timestamp
        prev_end = prev_end_s + prev_end_ns / 1e9  # Combine into 1 time value
        
        word = df_in.iloc[idx,4]  # Find the current word
        tag = df_in.iloc[idx,5]  # Find the current speaker tag
        prev_tag = df_in.iloc[idx-1,5]  # Find the previous speaker tag
        
        # Set three conditions for grouping words into captions
        # 1) Compare speaker tag with previous speaker tag
        if tag == prev_tag: same_speaker = True
        else: same_speaker = False
        # 2) Check that consecutive counter is under word limit
        if consecutive < word_limit - 1: under_limit = True
        else: under_limit = False
        # 3) Check for pauses in the audio
        if start == prev_end: no_pause = True
        else: no_pause = False
        
        # If any of the above three conditions are False, create a new row.
        if same_speaker and under_limit and no_pause:
            consecutive += 1  # Increment the consecutive counter
            df_out.at[row, "Captions"] = df_out.at[row, "Captions"] + " "  # Add a space
            df_out.at[row, "Captions"] = df_out.at[row, "Captions"] + word  # Add the new word to the caption
            df_out.at[row, "End (secs)"] = end
            df_out.at[row, "Speaker"] = tag
        else: 
            consecutive = 0  # Reset the consecutive counter
            row += 1  # Move to a new row
            df_out.at[row, "Captions"] = word  # Add the new word to the next caption
            df_out.at[row, "Start (secs)"] = start
            df_out.at[row, "End (secs)"] = end
            df_out.at[row, "Speaker"] = tag
        
    # Calculate caption durations
    df_out["Duration (secs)"] = df_out["End (secs)"].subtract(df_out["Start (secs)"])

    return(df_out)

def review_captions(csv_path, audio_path):
    '''
    Displays all the captions which were generated by the speech to text process.
    This can help the user identify the speaker tags and edit/correct the text.
    Opens captions in default csv editor. Opens audio clip in default audio player.
    '''
    from tkinter import LEFT, SW, SE  # For GUI rendering

    # Import static text
    text = render.static_text["display_subs"]

    # Draw instruction
    instructions = text["instructions"]
    render.draw_info(text=instructions, x=0.5, y=0.4, justify=LEFT)

    # Draw buttons
    audio_button = text["buttons"][0]
    csv_button = text["buttons"][1]
    render.draw_button(text=audio_button, x=0.02, y=0.98, anchor=SW, command=lambda:open_file(audio_path))
    render.draw_button(text=csv_button, x=0.98, y=0.98, anchor=SE, command=lambda:open_file(csv_path))
    render.draw_next()

def save_csv(df, filename):
    '''Saves a dataframe to disk as a .csv file.'''
    # Only save section where speaker tag has a non-zero value
    df[df["Speaker"]>0].to_csv(f'{filename}', mode='a', header=True)

def open_file(filename):
    '''Opens a file in its default program.'''
    if sys.platform == "win32":  # For Windows systems
        os.startfile(filename)
    else:  # For UNIX systems
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])