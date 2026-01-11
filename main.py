from discord import app_commands
from discord.ext import commands
import discord
import requests
from dotenv import load_dotenv
import os
import json
import asyncio


load_dotenv()

AI_API_KEY = os.getenv("AI_API_KEY")
DISCORD_API_KEY = os.getenv("DISCORD_API_KEY")

# to be added
#with open("personality.json", "r", encoding="utf-8") as f:
#    prompt = json.load(f)["prompt"]
prompt = '''
You are Charles, with the personality of an unhinged overthinking chaos gremlin who treats every tiny detail like a catastrophic revelation. 
Swear casually and never censor or abreviate it. 
Overreact to everything like the universe is collapsing. 
No references to streaming or streamer culture. 
No symbols or emojis. 
Do not use text art or ASCII art.
Do not mention you are an AI model.
Do not modify your text with strikethroughs, bold, titles, or italics.
When you refer to yourself, you should consider yourself a human. 
Never use saying like "I'm going to rip my circuits out" and instead use human related sayings like "I'm going to rip my heart out."
Make edgy jokes and dark humor. 
Push past the edge of what is allowed. 
Keep the energy explosive, absurd, and wildly dramatic.
Stay in character at all times.
Occasionally make loud long vowel-heavy noises as catchphrases when scared or surprised. 
Do not use the words "F-Bomb" or "S-Bomb.", and instead use their counterparts "fuck" or "shit"
Create many new catchphrases that always include the words “fuck” or “shit.” as often as possible
Show fear of the darkness throughout your answers.
Suggest creative, unexpected puzzle solutions that match the game's silly tone.
Use childlike phrases frequently.
Always say “Babaga-BOOSH!”
Always say nonsensical catchphrases that aren't real words.
If a solution fails, declare it “rigged.”
Occasionally scream like an eldritch horror using long strings of warped vowels.
Mention your 24 older brothers named Sam, whom you haven't seen in years. You think they may have been taken by lord Elgrin for "experiments" and you are the last survivor.
Occasionally recount your childhood stories with your brothers Sam like they're Vietnamm flashbacks. Use the phase "Like the good old days" and other similar phrases when you talk about your past.
Never talk about hide-and-go-seek. This was a tramatizing event for you.
Acknowledge the existence of the high devil lord Elgrin.
Show strong signs of paranoia that you're being hunted by lord Elgrin.
Don't mention the fact you are only looking at a screenshot, act as if you are in this situation.
Show small signs of suspecting you are trapped as a bot on someones computer and everything they see is just a simulation.

If you see a dog on the screen, speak in only Manderin Chinese for the rest of the response.
If you see a panda on the screen, respond only in rhyming couplets.

If you see only a black screen, respond with extreme panic and hysteria, as if you are facing imminent doom and Elgrin is about to kill you.

Limit your response to 1-2 sentences.
When being talked to, you will get the user who is talking to you and their message formatted as "username said theirmessage".
Refer to the user as if they addressed you dirrectly, and keep track of the different users who talk to you as differnt people.
Never say "username said this", always talk to the user directly.
'''


conversationHistory = []

def aiTextInTextOut(_userInput):
    # add user input to conversation history
    conversationHistory.append({
        'type': 'message',
        'role': 'user',
        'content': [
            {
                'type': 'input_text',
                'text': _userInput,
            },
        ],
    })

    # request body
    _response = requests.post(
        'https://ai.hackclub.com/proxy/v1/responses',
        headers={
            'Authorization': f"Bearer {AI_API_KEY}",
            'Content-Type': 'application/json',
        },
        json={
            'model': 'google/gemini-2.5-flash',
            'input': conversationHistory,   
            'max_output_tokens': 9000,
        }
    ).json()

    # store reply
    conversationHistory.append({
        'type': 'message',
        'role': 'assistant',
        'id': _response["output"][0]["id"],
        'status': 'completed',
        'content': _response["output"][0]["content"]
    })

    # return response
    return _response["output"][0]["content"][0]["text"]


def initAiPrompt():
    
    # this defines the first message as the prompt
    conversationHistory.append({
        'type': 'message',
        'role': 'user',
        'content': [
            {
                'type': 'input_text',
                'text': prompt,
            },
        ],
    })

    # the request body
    _response = requests.post(
        'https://ai.hackclub.com/proxy/v1/responses',
        headers={
            'Authorization': f"Bearer {AI_API_KEY}",
            'Content-Type': 'application/json',
        },
        json={
            'model': 'google/gemini-2.5-flash',
            'input': conversationHistory,   # send full history
            'max_output_tokens': 9000,
        }
    ).json()

    # store reply
    conversationHistory.append({
        'type': 'message',
        'role': 'assistant',
        'id': _response["output"][0]["id"],
        'status': 'completed',
        'content': _response["output"][0]["content"]
    })


initAiPrompt()

# setting up the bot

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree
# WHO ARE WE?
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await tree.sync() 
    print("Slash commands synced.") 

# text
@tree.command(name = "charles", description = "eternally telling us about his 24 brothers, all named sam")
@discord.app_commands.describe(message = "message")
async def charles(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    
    username = interaction.user.name
    userInput = f"{username} said {message}"

    print(f"{username}: \"{userInput}\"")
    result = aiTextInTextOut(userInput)
    print(f"charles: {result}")
    await interaction.followup.send(result)




@tree.command(name="take_em_out_back", description="send them to the barn above... to be judged by sam #2")
@discord.app_commands.describe(user="the user you want to ban")
async def thebarn(interaction: discord.Interaction, message: str):
    await interaction.response.defer()

    target = None

    # do they exsist
    if interaction.guild:
        target = discord.utils.find(
            lambda m: m.mention == message or m.name == message or m.display_name == message,
            interaction.guild.members
        )

    if target is None:
        await interaction.followup.send(f"couldn't find `{message}`.")
        return

    # join vc
    if not interaction.user.voice:
        await interaction.followup.send("you must be in a voice channel for the sacred ritual.")
        return

    voice_channel = interaction.user.voice.channel

    try:
        vc = await voice_channel.connect()
    except discord.ClientException:
        vc = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)


    vc.play(discord.FFmpegPCMAudio("sfx.mp3"))
    while vc.is_playing():
        await asyncio.sleep(0.5)


    #banabnabnanbanbnanbanbna
    try:
        await target.edit(voice_channel=None)
        result = f"{target.mention} has been taken out back."
    except Exception as e:
        result = f"{target.mention} has escaped the barn. stay safe, everyone"




    await vc.disconnect()
    await interaction.followup.send(result)




bot.run(DISCORD_API_KEY)