import os
import time
import subprocess
from langdetect import detect
from dotenv import load_dotenv, dotenv_values 
from PyDeepLX import PyDeepLX
from twitchio.ext import commands
from espeakng import ESpeakNG
from playsound import playsound

# Loading Variables
load_dotenv()

class Bot(commands.Bot):
    
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token = os.getenv("BOT_KEY"), prefix = os.getenv("PREFIX"), initial_channels = [os.getenv("CONNECT_CHANNEL")])

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    
    # Translator
    # Note: This function translates messages from one language to another based on the specified settings in the environment variables.
    # TwitchIO API without prefix
    async def event_message(self, message):
        orginal_message = message.content
        language_detection = detect(message.content)
        language_translate_back = os.getenv("LANG_DETECT")
        language_fallback = os.getenv("LANG_TO")
        voice_model = os.getenv("TTS-MODEL")
        print(f"Detected Language = {language_detection}")
        if language_detection == language_translate_back:
            if message.echo:
                return
            print(f"Orginal Message - {orginal_message} by {message.author.name}")
            time.sleep(2) 
            translate_message = PyDeepLX.translate(orginal_message, language_detection, language_fallback)
            print(f"Translated to - {translate_message}")
            await message.channel.send(f"{message.author.name} - {translate_message}")
            subprocess.run(["edge-tts", "--text",  f"{translate_message}", "--write-media", "audio.mp3", "-v", f"{voice_model}"])
            playsound("audio.mp3")
            return
        else:
            if message.echo:
                return
            print(f"Orginal Message - {orginal_message} by {message.author.name}")
            time.sleep(2)
            translate_message = PyDeepLX.translate(orginal_message)
            print(f"Translated to - {translate_message}")
            await message.channel.send(f"{message.author.name} - {translate_message}")
            subprocess.run(["edge-tts", "--text",  f"{translate_message}", "--write-media", "audio.mp3", "-v", f"{voice_model}"])
            playsound("audio.mp3")
            return

bot = Bot()
bot.run()
