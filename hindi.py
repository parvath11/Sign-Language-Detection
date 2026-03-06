import subprocess
import re
from googletrans import Translator
from gtts import gTTS
import pygame
import io
import asyncio  # Import the asyncio library

# Initialize the Translator
translator = Translator()

# Initialize pygame for playing audio
pygame.mixer.init()

# Function to play the audio directly from memory using pygame
def play_audio_stream(audio_stream):
    pygame.mixer.music.load(audio_stream, "mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10) # Wait a short while to prevent hogging CPU

# Function to translate detected sign to Hindi and speak it
async def translate_to_hindi_and_speak(english_text):
    # Use 'await' to get the result from the asynchronous function
    translated = await translator.translate(english_text, src='en', dest='hi')
    print(f"Translated to Hindi: {translated.text}")

    # Convert the translated text to speech using gTTS
    tts = gTTS(text=translated.text, lang='hi')
    
    # Save the speech to an in-memory file
    audio_stream = io.BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)

    # Play the audio stream
    play_audio_stream(audio_stream)

# Run the YOLOv5-based hand sign detection script
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
    await asyncio.to_thread(process.wait) # Wait for process completion in a thread to avoid blocking

if __name__ == "__main__":
    # Use asyncio.run() to execute the main async function
    try:
        asyncio.run(run_yolo_and_speak())
    except KeyboardInterrupt:
        print("Program terminated by user.")