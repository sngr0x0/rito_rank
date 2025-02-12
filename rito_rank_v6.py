import requests
import discord
import json
from discord.ext import commands
from discord import app_commands


with open("config.json", 'r') as config:
    data = json.load(config)

#Finding puuid:
def get_puuid(gameName:str, tagLine:str) -> str | None:
    response = requests.get(f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}\
    /{tagLine}?api_key={data['rito_token']}")
    #make sure we got a non-empty resopnse
    if response and response.status_code == 200:
        return response.json()['puuid']
    else:
        return None


#Finding Summoner's ID:
def get_summonerId(puuid:str, region:str) -> str | None:
    response = requests.get(f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={data['rito_token']}")
    if response and response.status_code == 200:
        return response.json()['id']
    else:
        return None

#Finding summoner's ranks stats:
def get_summoner_rank_stats(summonerId:str, region:str) -> dict | None:
    response = requests.get(f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerId}?api_key={data['rito_token']}")
    rank_stats = {}
    for item in response.json():
        if item['queueType'] == 'RANKED_SOLO_5x5':
            solo_stats = item
            rank_stats['tier'] = solo_stats['tier']
            rank_stats['rank'] = solo_stats['rank']
            #winrate = wins / total games
            winrate = solo_stats['wins'] / (solo_stats['wins'] + solo_stats['losses'])
            winrate_percent = round(winrate * 100, 2)
            rank_stats['winrate']= str(winrate_percent)+'%'
            return rank_stats
    return None


#all() enables all intents == CHANGE IT IN PRODUCTION!!!!
intents = discord.Intents.all()
status = discord.Status.idle
activity = discord.Game("League of Legends")

bot = commands.Bot(
    intents = intents,
    status = status,
    activity = activity,
    command_prefix= '$'
)

#A simple command to resend anything I tell it to say in uppercase.
@bot.command()
async def say(ctx, *, text):
    await ctx.send(text.upper())
#Greet new homies
@bot.event
async def on_member_join(member):
    guild = member.guild
    mention = member.mention
    channel = guild.system_channel  # system_channel is where automated messages like "welcome" messages are sent to.
    await channel.send(mention + "Welcome to the loli gang, homie ╰(*°▽°*)╯")


#Creating a slash command ,using "tree.command", which consists of 3 parts
#First part => region (which is a dropdown menu because its value is being used in the api call to the riot api; so it must be accurate
#and typically not freely entered by a user)
#Second => summoner_name; i.e. gameName in the riot api
#Third => tag; i.e. tagLine in the riot api
@bot.tree.command(name="get_rank_stats", description="Summoner's solo ranked stats.")
@app_commands.choices(
    region=[
        app_commands.Choice(name="North America", value="na1"),
        app_commands.Choice(name="Middle East", value="me1"),
        app_commands.Choice(name="Europe West", value="euw1"),
        app_commands.Choice(name="Europe Nordic & East", value="eun1"),
        app_commands.Choice(name="Oceania", value="oc1"),
        app_commands.Choice(name="Korea", value="kr"),
        app_commands.Choice(name="Japan", value="jp1"),
        app_commands.Choice(name="Brazil", value="br1"),
        app_commands.Choice(name="LAS", value="la2"),
        app_commands.Choice(name="LAN", value="la1"),
        app_commands.Choice(name="Russia", value="ru1"),
        app_commands.Choice(name="Turkey", value="tr1"),
        app_commands.Choice(name="Taiwan", value="tw2"),
        app_commands.Choice(name="Vietnam", value="vn2"),
        app_commands.Choice(name="Singapore", value="SG2")
    ]
)
async def get_rank_stats(interaction: discord.Interaction, region:app_commands.Choice[str], summoner_name:str, tag:str) -> bool:
    #Making sure the summoner_name and the tag are valid values
    if  len(summoner_name) < 3 or len(summoner_name) > 16:
        await interaction.response.send_message("Invalid summoner's name. Make sure it 3-character min and 16-character max.")
        return False
    if len(tag) < 3 or len(tag) > 5:
        await interaction.response.send_message("Invalid tag. Make sure it's 3-character min and 5-character max.")
        return False
    puuid = get_puuid(summoner_name, tag)
    region = region.value
    summonerId = get_summonerId(puuid, region)
    rank_stats = get_summoner_rank_stats(summonerId, region)
    if rank_stats:
        await interaction.response.send_message(
        f"{summoner_name}#{tag} ranked stats:\n\
        Rank: {rank_stats['tier']} {rank_stats['rank']}\n\
        Winrate: {rank_stats['winrate']}"
        )
    elif not rank_stats and summonerId:
        await interaction.response.send_message(f"There's no rank stats for this summoner :/")
    else:
        await interaction.response.send_message(f"No summoner is found :/")
    return True
#NOTE
#This code is bad cuz a follow up means a different message.
#Using itneraction.response.send_message() in a loop causes an error cuz you can only response once.

#sync the slash commands
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)!")
    except:
        print("Nothing is synced!")

if __name__ == '__main__':
    #running the bog with reconnect=True to make it try to reconnect if it ever disconnected. 
    bot.run(data['disco_token'],
               reconnect= True,
               )