import discord
from discord import app_commands
import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio
import time

load_dotenv()

biryani = "DISCORD_BOT_TOKEN(;( i mean application 1 ANYWAYS)"
butterchicken ="GEMINI_IS_FREE_GET_UR_KEEYYYYY"

genai.configure(api_key=butterchicken)
karahi = genai.GenerativeModel("gemini-3-flash-preview")

chai = discord.Intents.default()
chai.message_content = True

samosa = discord.Client(intents=chai)
tandoori = app_commands.CommandTree(samosa)
allowed_channels = set()
panju = time.time()
lassi_delay = 1800


def yasu(prompt):
    try:
        chicken = karahi.generate_content(prompt)
        if chicken.text:
            return chicken.text.strip()
    except Exception as biryani_error:
        print("Gemini hiccup:", biryani_error)
    return "Couldn't make a topic 😅"


def masala(category=None):
    if category:
        return yasu(f"Make ONE short {category} topic for a Discord server. Max 20 words. NO TRASH PLZZZZZZ")
    return yasu("Make ONE short fun topic for a Discord server. Max 20 words. e.g wht pokemon will be OU stable with 1 single change, or What if u are told u are in a dream? etc NO TRASH plzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")


def pakora():
    return yasu("Make a 'Would You Rather' question under 20 words, clean and ready for poll. e.g -- Would u rather choose 1$ or 2$ , or would u rather always be outside or always be etc NOO TRASH PLZZZZZZZZZZ")


def nihari():
    return yasu("Make a fun controversial hot take for a Discord chat. no trash ,, under 20 words only 1 NO TRASH PLZZZZZZZZ")


def jalebi():
    return yasu("Make a short debate topic for Discord. under 20 words, no trash just only 1,NO TRASH PLZZZZZZZZZZZZ")


@samosa.event
async def on_ready():
    await tandoori.sync()
    print(f"Online as {samosa.user}")
    samosa.loop.create_task(chai_checker())


@samosa.event
async def on_message(msg):
    global panju
    if msg.author.bot:
        return
    panju = time.time()


async def chai_checker():
    global panju
    await samosa.wait_until_ready()
    while not samosa.is_closed():
        if time.time() - panju > lassi_delay:
            for biryani_guild in samosa.guilds:
                for butter_channel in biryani_guild.text_channels:
                    if butter_channel.id not in allowed_channels:
                        continue
                    if butter_channel.permissions_for(biryani_guild.me).send_messages:
                        topic = masala()
                        embed = discord.Embed(title="💬 Chat's quiet...", description=topic, color=0x5865F2)
                        await butter_channel.send(embed=embed)
                        panju = time.time()
                        break
        await asyncio.sleep(60)


@tandoori.command(name="randtopic", description="Make a random topic")
@app_commands.describe(category="Optional category: gaming, programming, funny")
async def randtopic(interaction: discord.Interaction, category: str = None):
    if interaction.channel_id not in allowed_channels:
        interaction.response.send_message('❌ This Channel Is Not Allowed To do this!',ephemeral=True)
        return
    await interaction.response.defer()
    topic = masala(category)
    embed = discord.Embed(title="💬 Random Topic", description=topic, color=0x5865F2)
    await interaction.followup.send(embed=embed)


@tandoori.command(name="wouldyourather", description="Make a would-you-rather question")
async def wouldyourather(interaction: discord.Interaction):
    if interaction.channel_id not in allowed_channels:
        interaction.response.send_message('❌ This Channel Is Not Allowed To do this!',ephemeral=True)
        return
    await interaction.response.defer()
    text = pakora()
    embed = discord.Embed(title="🤔 Would You Rather", description=text, color=0x00b894)
    await interaction.followup.send(embed=embed)


@tandoori.command(name="hottake", description="Make a hot take")
async def hottake(interaction: discord.Interaction):
    if interaction.channel_id not in allowed_channels:
        interaction.response.send_message('❌ This Channel Is Not Allowed To do this!',ephemeral=True)
        return
    await interaction.response.defer()
    text = nihari()
    embed = discord.Embed(title="🔥 Hot Take", description=text, color=0xff7675)
    await interaction.followup.send(embed=embed)


@tandoori.command(name="debate", description="Make a debate topic")
async def debate(interaction: discord.Interaction):
    if interaction.channel_id not in allowed_channels:
        interaction.response.send_message('❌ This Channel Is Not Allowed To do this!',ephemeral=True)
        return
    await interaction.response.defer()
    text = jalebi()
    embed = discord.Embed(title="⚔ Debate Topic", description=text, color=0xfdcb6e)
    await interaction.followup.send(embed=embed)

@tandoori.command(name="settopicchannel", description="Allow this channel for bot topics")
async def settopicchannel(interaction: discord.Interaction):
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Admins only.", ephemeral=True)
        return

    allowed_channels.add(interaction.channel.id)

    await interaction.response.send_message(
        "✅ This channel is now allowed for topics."
    )
samosa.run(biryani)
