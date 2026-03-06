import subprocess
import re
from googletrans import Translator
from gtts import gTTS
import pygame
import io
import asyncio
import tempfile

translator = Translator()
pygame.mixer.init()

def play_audio_stream(audio_stream):
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_file:
        temp_file.write(audio_stream.read())
        temp_file.flush()
        pygame.mixer.music.load(temp_file.name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

def translate_to_tamil_and_speak(english_text):
    translated = translator.translate(english_text, src="en", dest="ta")
    print(f"Translated to Tamil: {translated.text}")
    tts = gTTS(text=translated.text, lang="ta")
    audio_stream = io.BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    play_audio_stream(audio_stream)

async def run_yolo_and_speak():
    last_label = None
    process = subprocess.Popen(
        ["python", "run.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:
        print(f"Output from run.py: {line.strip()}")
        detected = re.search(r'1 (\w+)', line)
        if detected:
            label = detected.group(1)
            print(f"Detected sign: {label}")
            if label != last_label:
                translate_to_tamil_and_speak(label)
                last_label = label

    process.stdout.close()
    await asyncio.to_thread(process.wait)

if __name__ == "__main__":
    try:
        asyncio.run(run_yolo_and_speak())
    except KeyboardInterrupt:
        print("Program terminated by user.")
