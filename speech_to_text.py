from google.cloud import speech_v1p1beta1
import io
import pandas as pd
import os

def set_env_variable(path):
    '''
    Sets the environment variable GOOGLE_APPLICATION_CREDENTIALS,
    which is required to make API calls to GCP.
    '''
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

def sample_long_running_recognize(path, num_speakers):
    '''
    Print confidence level for individual words in a transcription of a short audio
    file
    Separating different speakers in an audio file recording

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
      num_speakers Number of speakers in the clip
    '''

    client = speech_v1p1beta1.SpeechClient()

    # local_file_path = 'resources/commercial_mono.wav'

    # If enabled, each word in the first alternative of each result will be
    # tagged with a speaker tag to identify the speaker.
    enable_speaker_diarization = True

    # Optional. Specifies the estimated number of speakers in the conversation.
    diarization_speaker_count = num_speakers

    # When enabled, the first result returned by the API will include a list
    # of words and the start and end time offsets (timestamps) for those words.
    enable_word_time_offsets = True
    
    # The language of the supplied audio
    language_code = "en-US"  # Currently, "video" model is only available on en-US.
    
    config = {
        "enable_speaker_diarization": enable_speaker_diarization,
        "diarization_speaker_count": diarization_speaker_count,
        "language_code": language_code,
        "model": "video",
        "enable_word_time_offsets": enable_word_time_offsets
    }
    
    with io.open(path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for Google Speech-to-Text operation to complete...")
    response = operation.result()
    return response

def create_dataframe(response):
    '''
    Processes the response from the Google Speech Cloud model. 
    Output: A pandas dataframe.
    '''    
    for result in response.results:
        # First alternative has words tagged with speakers
        alternative = result.alternatives[0]
        # print(u"Transcript: {}".format(alternative.transcript))
        
        # Capture data in pandas data frame
        d = []
        for w in alternative.words:
            d.append(
                {"Start (secs)": w.start_time.seconds,
                 "Start (ns)": w.start_time.nanos,
                 "End (secs)": w.end_time.seconds,
                 "End (ns)": w.end_time.nanos,
                 "Word": w.word,
                 "Speaker": w.speaker_tag})
            
        df = pd.DataFrame(d)  # Saves the last dataframe in response.results, is this desirable?
    return df