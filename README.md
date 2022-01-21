# Automatic Subtitle Generator for Final Cut Pro X
Created by Dylan Klein

## Introduction
This prototype was built in order to automatically generate subtitles for videos (intended for editing in Final Cut Pro X). The aim is to save a significant amount of time during the editing process. The subtitles generated need to be engaging, and for this reason, YouTube closed captions are not suitable.

This demo was built in collaboration with the YouTube channel DarrenLevyOfficial (show title: "Funny Uber Rides").

This demo has the following requirements:
1. Subtitles MUST be available to be edited in Final Cut Pro X.
2. Subtitles MUST start and stop during the spoken word period to which the text belongs.
3. Subtitles MUST appear near the speaker's face in the video.
4. Process MUST save a significant amount of time and be easy for a video editor to use.

## Installation
This code was written in Python 3.7.4. Dependencies are:
* `ffmpeg` (ffmpeg needs to be installed on the OS - not a Python install, eg. `$ brew install ffmpeg`)
* `noisereduce`
* `google-cloud-speech` (May need to run: `$ pip install --upgrade google-cloud-speech`)
* `tkmessagebox`
* `pillow`
* `pandas`

#### Steps
1. Run the following command to install (most of) the above dependencies:
`$ pip install -r requirements.txt`

2. Then run the following command to install `ffmpeg`:
`$ brew install ffmpeg`

3. Create a Google Cloud Platform account, activate the Speech-to-Text API, save your API credentials as:
`.creds/google_creds.json`

4. To execute the program, simply run:
`$ python __init__.py`

## Function
#### Inputs
The program has the following inputs:
* Video file (.mp4 or .m4v formats)
* User to select number of speakers in video clip

#### Outputs
The program has the following outputs:
* A Comma Separated Values file (.csv) - displaying the generated captions
* A Final Cut Pro XML file (.fcpxml) - to be opened in Final Cut Pro X

## Architecture
The following diagram displays the overall architecture behind the prototype:
![Architecture](architecture.drawio.png)

## Example
Navigate to the `example` directory to view example input and output files.

## Prototyping
Navigate to the `prototyping` directory to view the Jupyter notebook files which helped me to prototype various components of the application.
