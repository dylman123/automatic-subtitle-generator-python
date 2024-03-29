from auto_sub_gen import render
import subprocess

def convert_to_wav(video_path, audio_path):
    '''
    Extracts the audio from a video file.
    Output is a .wav file which is written to disk.
    '''
    if ('\ ' in video_path) == False:
        video_path = video_path.replace(' ', '\ ')  # Escapes any spaces in file_path for POSIX
    command = f'ffmpeg -i {video_path} -ab 160k -ac 2 -ar 44100 -vn {audio_path}'
    subprocess.call(command, shell=True)

def convert_to_mono(stereo_path, mono_path):
    '''
    Converts an audio file in stereo to an audio file in mono format.
    Output is a .wav file which is written to disk.
    '''
    command = f'ffmpeg -i {stereo_path} -ac 1 {mono_path}'
    subprocess.call(command, shell=True)
    