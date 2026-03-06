import subprocess
import re
from googletrans import Translator
from gtts import gTTS
import pygame
import io
import asyncio  


translator = Translator()


pygame.mixer.init()


def play_audio_stream(audio_stream):
    pygame.mixer.music.load(audio_stream, "mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10) 


async def translate_to_hindi_and_speak(english_text):
    
    translated = await translator.translate(english_text, src='en', dest='ta')
    print(f"Translated to Tamil: {translated.text}")

    
    tts = gTTS(text=translated.text, lang='hi')
    
    
    audio_stream = io.BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)

   
    play_audio_stream(audio_stream)


async def run_yolo_and_speak():
    last_label = None

    process = subprocess.Popen(
        ["python", "run.py"],
        stdout=subprocess.
        PIPE,
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
                # Call the async function using 'await'
                await translate_to_hindi_and_speak(label)
                last_label = label

    process.stdout.close()
    await asyncio.to_thread(process.wait) 

if __name__ == "__main__":
    try:
        asyncio.run(run_yolo_and_speak())
    except KeyboardInterrupt:
        print("Program terminated by user.")