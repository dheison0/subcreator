from googletrans import Translator

MAX_TEXT_LENGTH = 2000

def translate(sub: list[dict], dest:str="pt") -> list[dict]:
    idx = 0
    separator =  "\n\n\n"
    tra = sub.copy()
    tra['text'] = ''
    while idx < len(sub["segments"]):
        text = ""
        start_idx = idx
        while len(text) < MAX_TEXT_LENGTH and idx < len(sub["segments"]):
            text += sub["segments"][idx]['text'] +separator
            idx += 1
        text = text.rstrip()
        translated = translate_segment(text, dest, sub['language'])
        for pIDX, piece in enumerate(translated.split(separator)):
            tra['segments'][start_idx+pIDX]['text'] = piece
            tra['text'] += piece
    tra['language'] = dest
    return tra
    
def translate_segment(text: str, dest: str, src: str = "en") -> str:
    translator = Translator()
    translated = translator.translate(text, dest=dest)
    return translated.text
