import pytube
from moviepy.editor import *
import os
import whisper
import datetime

def download_youtube_audio(video_url):
    # Download YouTube video using pytube
    youtube = pytube.YouTube(video_url)
    video = youtube.streams.get_lowest_resolution()
    video.download()

    # Get the downloaded video file path
    video_filename = video.default_filename

    # Convert video file to MP3 using moviepy
    video_clip = VideoFileClip(video_filename)
    audio_clip = video_clip.audio

    # Define the naming order for the audio files
    output_directory = "./"
    os.makedirs(output_directory, exist_ok=True)
    counter = len(os.listdir(output_directory)) + 1
    audio_filename = f"audio_{counter}.mp3"
    output_path = os.path.join(output_directory, audio_filename)

    audio_clip.write_audiofile(output_path)

    # Clean up the video file
    video_clip.close()
    audio_clip.close()
    os.remove(video_filename)

    return output_path

def seconds_to_srt_time(seconds):
    time_format = "%H:%M:%S"
    timedelta_obj = datetime.timedelta(seconds=seconds)
    hours, remainder = divmod(timedelta_obj.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    return formatted_time

def get_srt(result):
    data = []      
    segments = result['segments']
    for i in range(len(segments)):
        localObj = {}
        localObj['id']= segments[i]['id']
        localObj['seek']= segments[i]['seek']
        localObj['start']= segments[i]['start']
        localObj['end']= segments[i]['end']
        localObj['text']= segments[i]['text']
        data.append(localObj)
    srt = ""
    for idx, segment in enumerate(data, start=1):
        start_time = seconds_to_srt_time(segment['start'])
        end_time = seconds_to_srt_time(segment['end'])
        text = segment['text']
        srt += f"<a>{start_time.replace('.', ',')}</a>--> <a>{end_time.replace('.', ',')}</a>:<br>{text}<br>"

    # Write the generated SRT content to a file
    # with open('transcript.srt', 'w') as file:
    #     file.write(srt)
    return srt

# Main function
def main(url):
    video_url = url

    # Download YouTube video and convert to MP3
    audio_filename = download_youtube_audio(video_url)

    print("MP3 file downloaded:", audio_filename)
    model = whisper.load_model("tiny")



    filename = os.path.basename(audio_filename)
    filename_without_dot = os.path.splitext(filename)[0]
    new_filename = os.path.join(os.path.dirname(filename), filename_without_dot)

    print(new_filename)

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_filename)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    # print(f"Detected language: {max(probs, key=probs.get)}")

    result = model.transcribe(audio_filename)
    if result:
        os.remove(audio_filename)
    srt = get_srt(result)
    sending_result = {"text":result['text'],
                      "srt":srt}
    return sending_result
    
