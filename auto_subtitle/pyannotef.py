import os
import re
import dotenv
dotenv.load_dotenv()

current_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(current_dir)

speakers = []
subtitles = []

from pyannote.audio import Pipeline

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token=os.getenv("HUGGINGFACE_TOKEN")
)

def cut_file_speakers(string):
    print("Cutting file into speakers")
    string = str(pipeline(string)).split("\n")
    file = open("./temp/speakers.txt", "w",encoding="utf-8")
    for line in string:
        file.write(line + "\n")
    file.close()

def return_speaker(starter,speakers):
    treshold = 1000
    for i in speakers:
        if i == "": break
        timer = re.findall(r'\b\d{2}:\d{2}:\d{2}\.\d{3}\b',i)
        start = timer[0]
        if convert_ms(starter)>=convert_ms(start)-treshold:
            return int(re.search(r'\[.*\] A SPEAKER_(\d+)',i).group(1))
        else :
            print("not found")
        
def merge_srt_speaker(srt_path):
    srt = open(srt_path, "r",encoding="utf-8")
    srt = srt.read()
    srt = srt.split("\n\n")
    speakers = open("./temp/speakers.txt", "r",encoding="utf-8")
    speakers = speakers.read()
    speakers = speakers.split("\n")
    for s in srt :
        if s == "": break
        s = s.split("\n")
        duration = s[1]
        start = duration.split(" --> ")[0]
        end = duration.split(" --> ")[1]
        text = s[2]
        speaker = return_speaker(start,speakers)
        
        while len(subtitles) <= speaker:
            subtitles.append([])

        subtitles[speaker].append([start,end,text])

    for i in range(len(subtitles)):
        srt = open(f"./temp/speaker_{i}.srt", "w",encoding="utf-8")
        compteur = 1
        for j in subtitles[i]:
            srt.write(f"{compteur}\n{j[0]} --> {j[1]}\n{j[2]}\n\n")
            compteur += 1
        srt.close()

    return len(subtitles)

def convert_ms(time):
    parts = time.split(":")
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2].split(".")[0])
    ms = int(parts[2].split(".")[1])
    return hours * 3600000 + minutes * 60000 + seconds * 1000 + ms

def add_n_ms(time, n):
    total_ms = convert_ms(time) + n
    new_hours, remainder = divmod(total_ms, 3600000)
    new_minutes, remainder = divmod(remainder, 60000)
    new_seconds, remainder = divmod(remainder, 1000)
    new_ms = remainder
    new_time = f"{int(new_hours):02d}:{int(new_minutes):02d}:{int(new_seconds):02d}.{int(new_ms):03d}"
    return new_time