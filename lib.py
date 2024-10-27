import os
import subprocess
from time import strftime, time
from typing import Any

import googletrans

MAX_TEXT_LENGTH = 2000

last_used = time()


def log(text: str):
    global last_used
    print(f"[{strftime('%H:%M:%S')} {time()-last_used:0.1f}s] {text}")
    last_used = time()


def to_srt_time_format(time: float) -> str:
    hours = int(time // 3600)
    time -= hours * 3600
    minutes = int(time // 60)
    time -= minutes * 60
    seconds = int(time // 1)
    milliseconds = int((time - seconds) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def dump_srt_segments(segments: dict) -> str:
    srt = ""
    for idx, line in enumerate(segments):
        srt += f"{idx+1}\n"
        srt += f"{to_srt_time_format(line['start'])} --> {to_srt_time_format(line['end'])}\n"
        srt += f"{line['text'].strip()}\n\n"
    return srt


def translate_subtitles(subtitle: dict[str, Any], dest: str = "pt"):
    idx, separator = 0, "\n\n\n"
    translated = subtitle.copy()
    translated["text"] = ""
    segments = subtitle.get("segments")
    if not segments:
        return subtitle
    while idx < len("segments"):
        start_idx, text = idx, ""
        while len(text) < MAX_TEXT_LENGTH and idx < len(segments):
            text += segments[idx]["text"] + separator
            idx += 1
        text = text.rstrip()
        translated_text = translate_text(text, dest, subtitle.get("language"))
        for piece_idx, text in enumerate(translated_text.split(separator)):
            translated["segments"][start_idx + piece_idx]["text"] = text
            translated["text"] += text
    translated["language"] = dest
    return translated


def translate_text(text: str, dest: str, src: str = "auto") -> str:
    translator = googletrans.Translator()
    translated = translator.translate(text, dest, src)
    return translated.text


def add_subtitles(
    movie: str,
    subtitles: str,
    output: str,
    font="Roboto Medium",
    font_size=11,
    text_color="0000FFFF",
    shadow_color="00000000",
    shadow_size=1,
    margin_bottom=35,
):
    video_filter = f"subtitles={subtitles}:force_style='FontName={font},FontSize={font_size},PrimaryColour=&H{text_color},OutlineColour=&H{shadow_color},BorderStyle=1,Shadow={shadow_size},MarginV={margin_bottom}'"
    threads = os.cpu_count()
    cmd = [
        "ffmpeg",
        "-threads",
        str(threads),
        "-i",
        movie,
        "-vf",
        video_filter,
        "-y",
        output,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(
            f"Failed to add subtitles directly to movie:\n\n{result.stderr}"
        )
