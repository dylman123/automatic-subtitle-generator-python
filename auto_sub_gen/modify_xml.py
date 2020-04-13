import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import re
import os
import copy
import fileinput
import subprocess
import pandas as pd

def create_resource(root):
    '''
    Creates a new resource for a Basic Title.
    Returns the id of the new resource.
    '''
    resources = root.find('resources')
    new_id = str(len(resources)+1)
    title = ET.Element('effect')
    title.attrib = {'id': f'r{new_id}',
                     'name': 'Basic Title',
                     'uid': '.../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti'}
    resources.append(title)
    return new_id

def create_title(idx, captions, asset_idx, asset_offset, asset_start, coords, rsc_id):
    '''
    Generates a <title></title> section of the .fcpxml file, based on the
    captions which were generated previously.
    '''
    global title_template

    start = round(captions.iloc[idx, 1], 1)  # Round to 1dp to keep to 30fps edit boundary (100/3000s)
    duration = round(captions.iloc[idx, 3], 1)  # Round to 1dp to keep to 30fps edit boundary (100/3000s)
    caption = captions.iloc[idx, 4]
    speaker = captions.iloc[idx, 5]

    # Assign the title template to a local root 
    branch = title_template.getroot()

    # Find the clip's frame duration
    frame_duration = "1001/30000s"  #FIXME: frame_duration = find_fd()

    # Modify the template for the specific caption and associated FCP parameters
    rate = 3000  # Set to 3000 to keep to 30fps edit boundary (100/3000s)
    duration = int(duration * rate)
    offset = start - asset_offset + asset_start  # Offset time of title relative to overall clip
    offset = format_timestamp(time=offset, fd=frame_duration)
    #start = int(? * rate)  # Might not need to add to <title></title>
    x_pos, y_pos = coords[speaker-1]

    # Set parameter values in XML template
    branch.attrib['name'] = f'{caption} - Basic Title'
    branch.attrib['duration'] = f'{duration}/{rate}s'
    branch.attrib['offset'] = offset
    branch.attrib['ref'] = f'r{rsc_id}'
    #branch.attrib['start'] = f'{start}/{rate}s'  # Might not need to add to <title></title>
    branch[0].attrib['value'] = f'{x_pos} {y_pos}'
    branch[3][0].attrib['ref'] = f'ts{idx+1}'
    branch[3][0].text = f'{caption}'
    branch[4].attrib['id'] = f'ts{idx+1}'

    return copy.deepcopy(branch)

def find_asset_idx(captions, idx, clip_offsets):
    '''
    Returns an index (integer) which represents the appropriate asset-clip for 
    any given title. The index will be used on the list named clip_offsets.
    Also returns a float which represents the indexed clip's asset offset.
    '''
    asset_idx = 0
    audio_offset = captions.iloc[idx, 0]
    for clip_offset in clip_offsets:
        if audio_offset >= clip_offset:       
            asset_idx = clip_offsets.index(clip_offset)
            asset_offset = clip_offset
    return asset_idx, asset_offset

def is_int32(number):
    '''Checks if an integer is 32-bit.'''
    if type(number) != int: return False
    min32, max32 = -2**31, 2**31-1
    if number >= min32 and number <= max32:
        return True
    else: return False
    
def is_int64(number):
    '''Checks if an integer is 64-bit.'''
    if type(number) != int: return False
    min64, max64 = -2**63, 2**63-1
    if number >= min64 and number <= max64:
        return True
    else: return False

def fit2frame(time, frame_durs):
    '''
    Converts a time (int in seconds) into a string which FCPX expects.
    Output is a dict of strings. Each dict key is a frame duration.
    '''
    _locals = locals()
    time_vals = {}
    for fd in frame_durs.keys():
        num = frame_durs[fd][0]
        den = frame_durs[fd][1]
        exec(f'{fd} = {num} / {den}')
        exec(f'quotient = time / {fd}', globals(), _locals)
        rounded = int(round(_locals['quotient']))
        new_num = int(round(rounded*num))
        check = new_num/num
        if not check.is_integer():
            print(f'Warning, {check} is not an integer!')
        while(is_int64(new_num) == False):
            print(f'Warning, {new_num} is not a 64-bit integer!')
            new_num = int(new_num / 2)
            den = int(den / 2)
        if(is_int32(den) == False):
            print(f'Warning, {den} is not a 32-bit integer!')
        if den == 1:
            string = f'{new_num}s'
        else: string = f'{new_num}/{den}s'
        try: new_time = new_num / den
        except: pass
        time_vals[fd] = string
    return time_vals

def format_timestamp(time, fd):
    '''
    Selects the appropriate timestamp based on the clip's frame duration.
    Output is a string of format "{numerator}/{denomenator}s" for FCPX timing attributes requirements. For details on FCPX timing attributes, see:
    https://developer.apple.com/library/archive/documentation/FinalCutProX/Reference/FinalCutProXXMLFormat/StoryElements/StoryElements.html#//apple_ref/doc/uid/TP40011227-CH13-SW2
    '''
    fd_refs = {
    "1001/30000s": "fd_2997",
    "1001/60000s": "fd_5994",
    "100/3000s": "fd_30"
    }
    frame_durs = {
    "fd_2997": [1001, 30000],
    "fd_5994": [1001, 60000],
    "fd_30": [100, 3000]
    }
    timestamp = fit2frame(time, frame_durs)[fd_refs[fd]]
    return timestamp

def find_timings(spine):
    '''
    Finds the offsets and starts (timestamps) of each of the "asset-clip"s in the
    .fcpxml file. This is needed in order to match each of the captions into the appropriate
    asset-clip in the .fcpxml file. This function returns 2 lists of floats.
    '''

    clip_offsets = []
    for asset_clip in spine.findall('asset-clip'):
        num = int(re.split('/|s', asset_clip.attrib['offset'])[0])
        try: den = int(re.split('/|s', asset_clip.attrib['offset'])[1])  # May be an empty string
        except: den = 1
        clip_offsets.append(num / den)
    
    clip_starts = []
    for asset_clip in spine.findall('asset-clip'):
        num = int(re.split('/|s', asset_clip.attrib['start'])[0])
        try: den = int(re.split('/|s', asset_clip.attrib['start'])[1])  # May be an empty string
        except: den = 1
        clip_starts.append(num / den)
        
    return clip_offsets, clip_starts

def add_title(spine, asset_idx, new_title):
    '''Adds a title element into the appropriate location, whilst maintaining DTD validation.'''
    spine[asset_idx].append(new_title)
    trailing_elements = ['audio-channel-source']  # A list of subelements to exist at the end of the parent element
    for string in trailing_elements:
        element = spine[asset_idx].find(string)
        try:
            spine[asset_idx].remove(element)
            spine[asset_idx].append(element)  # Move subelement to end of the element list
        except: pass

def modify_xml(xml_path, template_path, csv_path, coords):
    '''Reads in the title template XML file and modifies it.'''
    global title_template, root

    # Parse saved csv as a pandas dataframe
    captions = pd.read_csv(csv_path)

    # Parse in the title template XML file
    title_template = ET.parse(template_path)

    # Open imported .fcpxml file
    file_in = ET.parse(xml_path)  # FIXME: Sometimes throws a parse error
    root = file_in.getroot()

    # Create a new resource for a Basic Title
    rsc_id = create_resource(root)

    # Create a spine variable (assumes only 1 spine exists in the video file)
    for element in root.iter('spine'):
        spine = element

    # Find offset and start timestamps (in seconds)
    clip_offsets, clip_starts = find_timings(spine)

    # Iterate through all the captions and place them in the appropriate xml locations
    for idx in range(len(captions)):
        asset_idx, asset_offset = find_asset_idx(captions, idx, clip_offsets)
        asset_start = clip_starts[asset_idx]
        new_title = create_title(idx, captions, asset_idx, asset_offset, asset_start, coords, rsc_id)
        add_title(spine, asset_idx, new_title)

def new_prettify(xml_tree):
    '''Does a pretty print for XML file'''
    reparsed = parseString(xml_tree)
    return('\n'.join([line for line in reparsed.toprettyxml(indent=' '*4).split('\n') if line.strip()]))

def add_header(out_path):
    '''Adds an appropriate XML header in order to pass DTD validation.'''
    header = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n'

    for n, line in enumerate(fileinput.input(out_path, inplace=True), start=1):
        if n == 1:
            print(header, end='\n')
        else:
            print(line, end='')

def dtd_validator(out_path, dtd_path):
    '''Runs a XML DTD validator. If validation fails, result is written to terminal.'''
    if ('\ ' in out_path) == False:
            out_path = out_path.replace(' ', '\ ')  # Escapes any spaces in file_path for POSIX
    command = f'xmllint --noout --dtdvalid {dtd_path} {out_path}'
    result = subprocess.call(command, shell=True)
    if(result == 1):
        print('DTD Validation Failed!')

def save_xml(video_name, output_dir, dtd_path):
    '''Writes the new .fcpxml file to disk.'''
    global root

    data = ET.tostring(root)  # Convert XML data to string
    xml_bytes = new_prettify(data).encode('utf-8')  # Prettify and covert to bytes

    out_path = f"{output_dir}/{video_name}.fcpxml"  # Set output path
    if os.path.exists(out_path): os.remove(out_path)  # Overwrite if exists

    with open(out_path, "wb") as file_out:
        file_out.write(xml_bytes)  # Write XML section to the file

    add_header(out_path)  # Write XML header to the file
    dtd_validator(out_path, dtd_path)  # Validate the outputted file against the FCPXML schema

    return out_path