import discord
from discord import app_commands
import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio
import time

load_dotenv()

abra = os.getenv("DISCORD_TOKEN")
zippy = os.getenv("GEMINI_API")

genai.configure(api_key=zippy)
fizz = genai.GenerativeModel("gemini-3-flash-preview")

spark = discord.Intents.default()
spark.message_content = True

blip = discord.Client(intents=spark)
tango = app_commands.CommandTree(blip)

ping = time.time()
loop_delay = 1800

def whizz(prompt):
    try:
        response = fizz.generate_content(prompt)
        if response.text:
            return response.text.strip()
    except Exception as e:
        print("Gemini hiccup:", e)
    return "Couldn't make a topic 😅"

def zap(category=None):
    if category:
        return whizz(f"Make ONE short {category} topic for a Discord server. Max 20 words. NO TRASH PLZZZZZZ")
    return whizz("Make ONE short fun topic for a Discord server. Max 20 words. e.g wht pokemon will be OU stable with 1 single change, or What if u are told u are in a dream? etc NO TRASH plzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")

def bop():
    return whizz("Make a 'Would You Rather' question under 20 words, clean and ready for poll. e.g -- Would u rather choose 1$ or 2$ , or would u rather always be outside or always be etc NOO TRASH PLZZZZZZZZZZ")

def boom():
    return whizz("Make a fun controversial hot take for a Discord chat. no trash ,, under 20 words only 1 NO TRASH PLZZZZZZZZ")

def buzz():
    return whizz("Make a short debate topic for Discord. under 20 words, no trash just only 1,NO TRASH PLZZZZZZZZZZZZ")

@blip.event
async def on_ready():
    await tango.sync()
    print(f"Online as {blip.user}")
    blip.loop.create_task(chatter_checker())

@blip.event
async def on_message(msg):
    global ping
    if msg.author.bot:
        return
    ping = time.time()

async def chatter_checker():
    global ping
    await blip.wait_until_ready()
    while not blip.is_closed():
        if time.time() - ping > loop_delay:
            for guild in blip.guilds:
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        topic = zap()
                        embed = discord.Embed(title="💬 Chat's quiet...", description=topic, color=0x5865F2)
                        await channel.send(embed=embed)
                        ping = time.time()
                        break
        await asyncio.sleep(60)

@tango.command(name="randtopic", description="Make a random topic")
@app_commands.describe(category="Optional category: gaming, programming, funny")
async def randtopic(interaction: discord.Interaction, category: str = None):
    await interaction.response.defer()
    topic = zap(category)
    embed = discord.Embed(title="💬 Random Topic", description=topic, color=0x5865F2)
    await interaction.followup.send(embed=embed)

@tango.command(name="wouldyourather", description="Make a would-you-rather question")
async def wouldyourather(interaction: discord.Interaction):
    await interaction.response.defer()
    text = bop()
    embed = discord.Embed(title="🤔 Would You Rather", description=text, color=0x00b894)
    await interaction.followup.send(embed=embed)

@tango.command(name="hottake", description="Make a hot take")
async def hottake(interaction: discord.Interaction):
    await interaction.response.defer()
    text = boom()
    embed = discord.Embed(title="🔥 Hot Take", description=text, color=0xff7675)
    await interaction.followup.send(embed=embed)

@tango.command(name="debate", description="Make a debate topic")
async def debate(interaction: discord.Interaction):
    await interaction.response.defer()
    text = buzz()
    embed = discord.Embed(title="⚔ Debate Topic", description=text, color=0xfdcb6e)
    await interaction.followup.send(embed=embed)

blip.run(abra)
