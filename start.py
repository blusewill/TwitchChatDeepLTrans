import os
import time
from langdetect import detect
from dotenv import load_dotenv, dotenv_values 
from PyDeepLX import PyDeepLX
from twitchio.ext import commands

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
        print(f"Detected Language = {language_detection}")
        if language_detection == language_translate_back:
            if message.echo:
                return
            print(f"Orginal Message - {orginal_message} by {message.author.name}")
            time.sleep(2) 
            translate_message = PyDeepLX.translate(orginal_message, language_detection, language_fallback)
            print(f"Translated to - {translate_message}")
            await message.channel.send(f"{message.author.name} - {translate_message}")
            return
        else:
            if message.echo:
                return
            print(f"Orginal Message - {orginal_message} by {message.author.name}")
            time.sleep(2)
            translate_message = PyDeepLX.translate(orginal_message)
            print(f"Translated to - {translate_message}")
            await message.channel.send(f"{message.author.name} - {translate_message}")
            return
   
    # Ping Test
    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        is_moderator = 'moderator' in ctx.author.badges 
        is_broadcaster = 'broadcaster' in ctx.author.badges
        if is_moderator or is_broadcaster:
            await ctx.send(f'You Test your bot it scores 100% working. Right? {ctx.author.name}')
    
    # Message Repeater 
    
    @commands.command(name="say")
    async def say(self, ctx: commands.Context, *,phrase: "str") -> None:
        is_moderator = 'moderator' in ctx.author.badges 
        is_broadcaster = 'broadcaster' in ctx.author.badges
        if is_moderator or is_broadcaster:
           response = f"{phrase}"
           await ctx.send(response)

bot = Bot()
bot.run()
