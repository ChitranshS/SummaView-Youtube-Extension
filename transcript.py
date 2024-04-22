import yt_dlp
import datetime
import os
import whisper
import random
def download_ytvid_as_mp3(url):
    video_url = url
    number =random.randint(1, 100)
    filename = f"name{number}.webm"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_url])
    print(f"Download complete... {filename}")
    return filename
def seconds_to_srt_time(seconds):
    time_format = "%H:%M:%S"
    timedelta_obj = datetime.timedelta(seconds=seconds)
    hours, remainder = divmod(timedelta_obj.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    return formatted_time

def get_srt(result):
    segments = result['segments']
    srt = ""
    for segment in segments:
        start_time = seconds_to_srt_time(segment['start'])
        end_time = seconds_to_srt_time(segment['end'])
        text = segment['text']
        srt += f"<a href=\"\" class=\"injectedLink\">{ start_time.replace('.', ',')}</a> --> <a href=\"\" class=\"injectedLink\">{end_time.replace('.', ',')}</a>:<br>{text}<br>"
    return srt
def main(url):

    filepath = download_ytvid_as_mp3(url)

    model = whisper.load_model("tiny")

        # Load audio and process
    audio = whisper.load_audio(filepath)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)

    result = model.transcribe(filepath)
    if result:
            os.remove(filepath)

    print("transcribed")

    srt = get_srt(result)
    sending_result = {"text": result['text'], "srt": srt}
    return sending_result
