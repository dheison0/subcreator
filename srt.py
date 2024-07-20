def _time_to_src_format(time: float) -> str:
    hours = int(time // 3600)
    time -= hours * 3600
    minutes = int(time // 60)
    time -= minutes * 60
    seconds = int(time // 1)
    milliseconds = int((time - seconds) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def dump(segments: dict) -> str:
    result = ""
    for idx, line in enumerate(segments):
        result += f"{idx+1}\n"
        result += f"{_time_to_src_format(line['start'])} --> {_time_to_src_format(line['end'])}\n"
        result += f"{line['text'].strip()}\n\n"
    return result
