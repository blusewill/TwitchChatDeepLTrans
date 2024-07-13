import os
import time
import asyncio
from langdetect import detect
from dotenv import load_dotenv
from deepl import DeepLCLI
from twitchio.ext import commands
import edge_tts
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
        chan = bot.get_channel(os.getenv("CONNECT_CHANNEL"))
        loop = asyncio.get_event_loop()
        loop.create_task(chan.send(f"{self.nick} is currently Online BloodTrail"))

    
    # Translator
    # Note: This function translates messages from one language to another based on the specified settings in the environment variables.
    # TwitchIO API without prefix
    async def event_message(self, message):
        orginal_message = message.content
        language_detection = detect(message.content)
        language_translate_back = os.getenv("LANG_DETECT")
        language_fallback = os.getenv("LANG_TO")
        voice_model = os.getenv("TTS_MODEL")
        print(voice_model)
        if not isinstance(voice_model, str):
            raise ValueError("The voice model must be a string.")
        print(f"Detected Language = {language_detection}")
        if language_detection == language_translate_back:
            if message.echo:
                return
            print(f"Original Message - {orginal_message} by {message.author.name}")
            time.sleep(2) 
            deepl = DeepLCLI(f"{language_detection}", f"{language_fallback}")
            translate_message = await deepl.translate_async(orginal_message)
            print(f"Translated to - {translate_message}")
            await message.channel.send(f"{message.author.name} - {translate_message}")
            communicate = edge_tts.Communicate(translate_message, voice_model)
            with open("audio.mp3", "wb") as file:
                for chunk in communicate.stream_sync():
                    if chunk["type"] == "audio":
                        file.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        print(f"WordBoundary: {chunk}")
            playsound("audio.mp3")
            os.remove("audio.mp3")
            return
        else:
            if message.echo:
                return
            if not isinstance(voice_model, str):
                raise ValueError("The voice model must be a string.")
            print(f"Original Message - {orginal_message} by {message.author.name}")
            time.sleep(2)
            deepl = DeepLCLI("auto", "en")
            translate_message = await deepl.translate_async(orginal_message)
            print(f"Translated to - {translate_message}")
            await message.channel.send(f"{message.author.name} - {translate_message}")
            communicate = edge_tts.Communicate(translate_message, voice_model)
            with open("audio.mp3", "wb") as file:
                for chunk in communicate.stream_sync():
                    if chunk["type"] == "audio":
                        file.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        print(f"WordBoundary: {chunk}")
            playsound("audio.mp3")
            os.remove("audio.mp3")


bot = Bot()
bot.run()
