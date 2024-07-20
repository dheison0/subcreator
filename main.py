import  whisper
import time
from sys import argv
from translate import translate
from srt import dump as srtdump

if len(argv) == 1:
    print(f"usage: {argv[0]} audio.wav")
    exit(0)

WHISPER_MODEL = "small.en"
log = lambda text: print(f"{time.strftime('%H:%M:%S')}: {text}")
input_audio = argv[1]
srt_out = argv[1].split("/")[-1]+".srt"

log("Starting system...")
log(f"Loading whisper model {WHISPER_MODEL}...")
model = whisper.load_model(WHISPER_MODEL)
log("Whisper model loaded!")

log("Transcribing audio to text...")
audio = whisper.load_audio(input_audio)
result = model.transcribe(audio)
log("Transcribed!")

log("Translating...")
translated = translate(result)
log("Translated!")

log(f"Writing to {srt_out}...")
srt_file = open(srt_out, "w")
srt_file.write(srtdump(translated['segments']))
srt_file.close()
log("Done")