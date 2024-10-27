import shutil
from argparse import ArgumentParser, Namespace
from tempfile import mktemp

import whisper

import lib


def write_subtitles(file: str, segments: list[dict]):
    out = open(file, "w")
    out.write(lib.dump_srt_segments(segments))
    out.close()


def transcribe(
    whisper_model: str, audio_file: str, src_language: str | None = None
) -> dict:
    lib.log(f"Loading whisper {whisper_model} model...")
    model = whisper.load_model(whisper_model)
    lib.log("Model loaded! Loading audio...")
    audio = whisper.load_audio(audio_file)
    lib.log("Audio loaded! Transcribing...")
    result = model.transcribe(audio, language=src_language)
    lib.log("Transcribed!")
    return result


def parse_args() -> Namespace:
    argparser = ArgumentParser()
    argparser.add_argument("--input", "-i", required=True, help="Input video file")
    argparser.add_argument("--output", "-o", required=True, help="Output file")
    argparser.add_argument(
        "--target-language",
        "-t",
        default="en",
        help="Output target language",
    )
    argparser.add_argument(
        "--input-language", help="Set original movie language", default=None
    )
    argparser.add_argument(
        "--whisper-model",
        default="small",
        help="Whisper model used to transcribe movies",
    )
    argparser.add_argument(
        "--save-srt",
        help="Save subtitles to <output>.<language>.srt file",
        action="store_true",
    )

    args = argparser.parse_args()
    return args


def main():
    args = parse_args()

    subtitles = transcribe(args.whisper_model, args.input, args.input_language)
    temp_subtitles = mktemp()
    write_subtitles(temp_subtitles, subtitles["segments"])
    subtitles_basename = args.output.replace(args.output.split(".")[-1], "")[:-1]
    if args.save_srt:
        lib.log("Saving original subtitles...")
        shutil.copy(temp_subtitles, f"{subtitles_basename}.{subtitles['language']}.srt")
        lib.log("Saved!")

    if subtitles["language"] != args.target_language:
        lib.log(
            f"Translating from {subtitles['language']} to {args.target_language}..."
        )
        subtitles = lib.translate_subtitles(subtitles, args.target_language)
        write_subtitles(temp_subtitles, subtitles["segments"])

    if args.save_srt:
        lib.log(f"Saving {subtitles['language']} subtitles...")
        shutil.copy(temp_subtitles, f"{subtitles_basename}.{subtitles['language']}.srt")
        lib.log("Saved!")

    lib.log("Adding subtitles to movie...")
    lib.add_subtitles(args.input, temp_subtitles, args.output)
    lib.log("Done!")


if __name__ == "__main__":
    main()
