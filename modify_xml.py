import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import re
import os
import copy
import fileinput
import subprocess

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

    start = round(captions.iloc[idx, 0], 1)  # Round to 1dp to keep to 30fps edit boundary (100/3000s)
    duration = round(captions.iloc[idx, 2], 1)  # Round to 1dp to keep to 30fps edit boundary (100/3000s)
    caption = captions.iloc[idx, 3]
    speaker = captions.iloc[idx, 4]

    # Assign the title template to a local root 
    branch = title_template.getroot()

    # Modify the template for the specific caption and associated FCP parameters
    rate_1 = 3000  # Set to 3000 to keep to 30fps edit boundary (100/3000s)
    rate_2 = 3000  # Set to 3000 to keep to 30fps edit boundary (100/3000s)
    rate_3 = 3000  # Set to 3000 to keep to 30fps edit boundary (100/3000s)
    relstart = start - asset_offset  # Start time of title relative to clip
    offset = int((asset_start + relstart) * rate_1)
    duration = int(duration * rate_2)
    #start = int(? * rate_3)  # Probably don't need to add to <title></title> for now
    x_pos, y_pos = coords[speaker-1]

    # Set parameter values in XML template
    branch.attrib['name'] = f'{caption} - Basic Title'
    branch.attrib['offset'] = f'{offset}/{rate_1}s'
    branch.attrib['duration'] = f'{duration}/{rate_2}s'
    branch.attrib['ref'] = f'r{rsc_id}'
    #branch.attrib['start'] = f'{start}/{rate_3}s'  # Probably don't need to add to <title></title>
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

def modify_xml(xml_path, template_path, captions, coords):
    '''Reads in the title template XML file and modifies it.'''
    global title_template, root

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