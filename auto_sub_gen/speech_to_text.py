from google.cloud import speech_v1p1beta1
from google.cloud import storage
import io
import pandas as pd
import os

def set_env_variable(path):
    '''
    Sets the environment variable GOOGLE_APPLICATION_CREDENTIALS,
    which is required to make API calls to GCP.
    '''
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

def upload_blob(source_file_name, bucket_name="sample-audio-clips", destination_blob_name="audio/temp-audiofile.wav"):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
    return blob

def delete_from_gcs(blob):
    blob.delete()
    print("File audio/temp-audiofile.wav removed from Google Cloud Storage bucket.")

def sample_long_running_recognize(num_speakers, storage_uri="gs://sample-audio-clips/audio/temp-audiofile.wav"):
    """
    Print confidence level for individual words in a transcription of a short audio
    file
    Separating different speakers in an audio file recording

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """

    client = speech_v1p1beta1.SpeechClient()

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
    
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
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