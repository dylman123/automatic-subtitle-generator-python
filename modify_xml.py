import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import re
import os
import copy

def create_title(idx, captions, asset_idx, asset_offset, asset_start, coords):
    '''
    Generates a <title></title> section of the .fcpxml file, based on the
    captions which were generated previously.
    '''
    global title_template

    start = captions.iloc[idx, 0]
    duration = captions.iloc[idx, 2]
    caption = captions.iloc[idx, 3]
    speaker = captions.iloc[idx, 4]

    # Assign the title template to a local root 
    branch = title_template.getroot()

    # Modify the template for the specific caption and associated FCP parameters
    rate_1 = 6000
    rate_2 = 3000
    #rate_3 = 3000  # Probably don't need to add to <title></title>
    relstart = start - asset_offset  # Start time of title relative to clip
    offset = int((asset_start + relstart) * rate_1)
    duration = int(duration * rate_2)
    #start = int(3363 * rate_3)  # Probably don't need to add to <title></title>
    x_pos, y_pos = coords[speaker-1]

    # Set parameter values in XML template
    branch.attrib['name'] = f'{caption} - Basic Title'
    branch.attrib['offset'] = f'{offset}/{rate_1}s'
    branch.attrib['duration'] = f'{duration}/{rate_2}s'
    #branch.attrib['start'] = f'{start}/{rate_3}s'  # Probably don't need to add to <title></title>
    branch[0].attrib['value'] = f'{x_pos} {y_pos}'
    branch[3][0].attrib['ref'] = f'ts{idx}'
    branch[3][0].text = f'{caption}'
    branch[4].attrib['id'] = f'ts{idx}'

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

def find_timings(root):
    '''
    Finds the offsets and starts (timestamps) of each of the "asset-clip"s in the
    .fcpxml file. This is needed in order to match each of the captions into the appropriate
    asset-clip in the .fcpxml file. This function returns 2 lists of floats.
    '''
    clip_offsets = []
    for asset_clip in root[1][0][0][0][0].findall('asset-clip'):
        num = int(re.split('/|s', asset_clip.attrib['offset'])[0])
        try: den = int(re.split('/|s', asset_clip.attrib['offset'])[1])  # May be an empty string
        except: den = 1
        clip_offsets.append(num / den)
    
    clip_starts = []
    for asset_clip in root[1][0][0][0][0].findall('asset-clip'):
        num = int(re.split('/|s', asset_clip.attrib['start'])[0])
        try: den = int(re.split('/|s', asset_clip.attrib['start'])[1])  # May be an empty string
        except: den = 1
        clip_starts.append(num / den)
        
    return clip_offsets, clip_starts

def modify_xml(xml_path, template_path, captions, coords):
    '''Reads in the title template XML file and modifies it.'''
    global title_template, ROOT

    # Parse in the title template XML file
    title_template = ET.parse(template_path)

    # Open imported .fcpxml file
    file_in = ET.parse(xml_path)
    root = file_in.getroot()

    # Find offset and start timestamps (in seconds)
    clip_offsets, clip_starts = find_timings(root)

    # Iterate through all the captions and place them in the appropriate xml locations
    for idx in range(len(captions)):
        asset_idx, asset_offset = find_asset_idx(captions, idx, clip_offsets)
        asset_start = clip_starts[asset_idx]
        new_title = create_title(idx, captions, asset_idx, asset_offset, asset_start, coords)
        root[1][0][0][0][0][asset_idx].append(new_title)

    # Update ROOT (global variable)
    ROOT = root

def new_prettify(xml_tree):
    '''Does a pretty print for XML file'''
    reparsed = parseString(xml_tree)
    return('\n'.join([line for line in reparsed.toprettyxml(indent=' '*4).split('\n') if line.strip()]))

def save_xml(video_name, output_dir):
    '''Writes the new .fcpxml file to disk.'''
    global ROOT

    xml_header = [  # Add XML header
        b'<?xml version="1.0" encoding="UTF-8"?>\n',
        b'<!DOCTYPE fcpxml>\n',
        b'\n'
        ]

    data = ET.tostring(ROOT)  # Convert XML data to string
    xml_bytes = new_prettify(data).encode('utf-8')  # Prettify and covert to bytes

    out_path = f"{output_dir}/{video_name}.fcpxml"  # Set output path
    if os.path.exists(out_path): os.remove(out_path)  # Overwrite if exists
    
    with open(out_path, "wb") as file_out:
        file_out.writelines(xml_header)  # Write XML header to the file
        file_out.write(xml_bytes)  # Write XML section to the file