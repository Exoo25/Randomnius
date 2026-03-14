import discord
from discord import app_commands
import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio
import time

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API = os.getenv("GEMINI_API")

# Configure Gemini
genai.configure(api_key=GEMINI_API)

model = genai.GenerativeModel("gemini-3-flash-preview")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

last_message_time = time.time()
AUTO_TOPIC_DELAY = 1800  # 30 minutes


# ---------- AI GENERATION ----------

def generate_text(prompt):
    try:
        response = model.generate_content(prompt)
        if response.text:
            return response.text.strip()
    except Exception as e:
        print("Gemini error:", e)

    return "AI failed to generate a topic."


def generate_topic(category=None):
    if category:
        prompt = f"Generate ONE short {category} discussion topic for a Discord server. Under 20 words."
    else:
        prompt = "Generate ONE short fun discussion topic for a Discord server. Under 20 words."

    return generate_text(prompt)


def generate_wyr():
    prompt = "Create a 'Would You Rather' question for a Discord server. under 20m words no trash at last just poll like"
    return generate_text(prompt)


def generate_hot_take():
    prompt = "Generate a controversial but fun hot take for a Discord server discussion."
    return generate_text(prompt)


def generate_debate():
    prompt = "Generate a short debate topic for people in a Discord server."
    return generate_text(prompt)


# ---------- BOT EVENTS ----------

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")
    client.loop.create_task(dead_chat_checker())


@client.event
async def on_message(message):
    global last_message_time

    if message.author.bot:
        return

    last_message_time = time.time()


# ---------- DEAD CHAT REVIVER ----------

async def dead_chat_checker():
    global last_message_time

    await client.wait_until_ready()

    while not client.is_closed():

        if time.time() - last_message_time > AUTO_TOPIC_DELAY:

            for guild in client.guilds:
                for channel in guild.text_channels:

                    if channel.permissions_for(guild.me).send_messages:
                        topic = generate_topic()

                        embed = discord.Embed(
                            title="💬 Chat seems quiet...",
                            description=topic,
                            color=0x5865F2
                        )

                        await channel.send(embed=embed)
                        last_message_time = time.time()
                        break

        await asyncio.sleep(60)


# ---------- COMMANDS ----------

@tree.command(name="randtopic", description="Generate a random discussion topic")
@app_commands.describe(category="Optional topic category (gaming, programming, funny)")
async def randtopic(interaction: discord.Interaction, category: str = None):

    await interaction.response.defer()

    topic = generate_topic(category)

    embed = discord.Embed(
        title="💬 Random Discussion Topic",
        description=topic,
        color=0x5865F2
    )

    await interaction.followup.send(embed=embed)


@tree.command(name="wouldyourather", description="Generate a would-you-rather question")
async def wouldyourather(interaction: discord.Interaction):

    await interaction.response.defer()

    text = generate_wyr()

    embed = discord.Embed(
        title="🤔 Would You Rather",
        description=text,
        color=0x00b894
    )

    await interaction.followup.send(embed=embed)


@tree.command(name="hottake", description="Generate a hot take")
async def hottake(interaction: discord.Interaction):

    await interaction.response.defer()

    text = generate_hot_take()

    embed = discord.Embed(
        title="🔥 Hot Take",
        description=text,
        color=0xff7675
    )

    await interaction.followup.send(embed=embed)


@tree.command(name="debate", description="Generate a debate topic")
async def debate(interaction: discord.Interaction):

    await interaction.response.defer()

    text = generate_debate()

    embed = discord.Embed(
        title="⚔ Debate Topic",
        description=text,
        color=0xfdcb6e
    )

    await interaction.followup.send(embed=embed)


client.run(DISCORD_TOKEN)
