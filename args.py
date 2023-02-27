#pylint:disable=E1123
#pylint:disable=E0237
from __future__ import absolute_import
from reddittracker import parser
from discord.ext import commands
import discord
import praw
import datetime
import requests
from bs4 import BeautifulSoup


intents = discord.Intents().all()
intents.members = True
intents.messages = True
intents.message_content = True

prefix = '!' 
bot = commands.Bot(command_prefix=prefix, intents=intents)

reddit = praw.Reddit(
client_id='client_id',
client_secret='client_secret',
user_agent='user_agent',
username='username',
password='password'
)

reddit.read_only = False

            

        
@bot.command()
async def searchgsi(ctx, *, device):
    SEARCH_URLS = [
        "https://github.com/phhusson/treble_experimentations/wiki",
        "https://forum.xda-developers.com/c/treble-roms-and-development.8511/",
        "https://forum.xda-developers.com/c/android-general/generic-system-image-gsi-list-t3832615",
        "https://forum.xda-developers.com/t/android-10-q-generic-system-image.3952019/",
        "https://gitlab.com/shagbag913/vendor-gsis/-/wikis/home",
        "https://github.com/solutionfixxxer/Project-Treble-Experience/wiki",
        "https://magiskzip.com/gsi-list-phhusson/",
        "https://www.lineageos.org/",
        "https://download.lineageos.org/",
        "https://gerrit.pixelexperience.org/",
        "https://forum.xda-developers.com/t/gsis-and-treble-roms-index-for-all-devices.3824063/"
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }

    results = []
    for url in SEARCH_URLS:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all("a", href=True)
            for link in links:
                if device.lower() in link.text.lower():
                    results.append((link.text, link["href"]))

    if not results:
        await ctx.send(f"No GSIs found for '{device}'.")
    else:
        embed = discord.Embed(title=f"Search Results for '{device}':", color=0x00ff00)
        for index, result in enumerate(results[:10], start=1):
            embed.add_field(name=f"Result {index}:", value=f"[{result[0]}]({result[1]})", inline=False)
        await ctx.send(embed=embed)
        
            
                       
                                             
@bot.command()
async def search(ctx, *, query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    url = f'https://duckduckgo.com/html/?q={query}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('.result__url')
    if not links:
        await ctx.send('No results found.')
    else:
        x_embed = discord.Embed(title=f"Search Results for '{query}':", color=0x00ff00)
        for index, link in enumerate(links[0:20], start=1):
            x_embed.add_field(name=f"Result {index}:", value=link.get('href'), inline=False)
        await ctx.send(embed=x_embed)            


@bot.command()
async def searchfirmware(ctx, *, model):
    SEARCH_URLS = [
        ("https://www.sammobile.com/firmwares/search", {"q": model}),
        ("https://updato.com/firmware-archive-select-model", {"model_name": model}),
        ("https://www.firmware.science/", {"s": model}),
        ("https://www.officialroms.com/", {"s": model}),
        ("https://www.androidfilehost.com/", {"w=search&s=": model}),
        ("https://firmwarefile.com/", {"q": model}),
        ("https://www.mobilesfirmware.com/", {"s": model}),
        ("https://androidmtk.com/category/firmware", {"s": model}),
        ("https://firmwarex.net/", {"s": model})
    ]
    
    firmware_found = False
    for url, params in SEARCH_URLS:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all("a", href=True)
            for link in links:
                if model.lower() in link.text.lower() and "download" in link.text.lower():
                    await ctx.send(link["href"])
                    firmware_found = True
                    break
        if firmware_found:
            break
    
    if not firmware_found:
        await ctx.send(f"No firmware found for {model}.")



@bot.command()
async def info(ctx):
    help_embed = discord.Embed(title="Command Information", color=discord.Color.blue())
    help_embed.add_field(name="!searchgsi", value="Search for GSI for an Android device.", inline=False)
    help_embed.add_field(name="!searchfirmware", value="Search for firmware versions for an Android device.", inline=False)
    help_embed.add_field(name="!search", value="Search the internet for information.", inline=False)
    help_embed.add_field(name="!root", value="Shows last post from subreddit r/androidroot")
    await ctx.send(embed=help_embed)
    
@bot.command()
async def root(ctx):
    subreddit = reddit.subreddit('androidroot')
    latest_post = subreddit.new(limit=1).__next__()
    post_embed = discord.Embed(title=latest_post.title, url=latest_post.shortlink, description=latest_post.selftext,
                               color=discord.Color.blue())

    post_comments = []
    for comment in latest_post.comments:
        if len(post_comments) < 4:
            post_comments.append(f"{comment.author.name}: {comment.body}")
        else:
            break
    post_embed.add_field(name="Comments", value="\n".join(post_comments), inline=False)
    await ctx.send(embed=post_embed)    


@bot.event
async def on_ready():
            now = datetime.datetime.now()
            channel = discord.utils.get(bot.get_all_channels(), name='bot-status')
            embed = discord.Embed(title="The bot is now online!")
            embed.add_field(name="Online: ", value=":green_circle:")
            embed.add_field(name=f"The date is: ", value=str(now))
            embed.add_field(name=":information_source:", value="Type !info for the commands!")
            await channel.send(embed=embed)
           
    
                                 
              
if __name__ == "__main__":
    TOKEN = "TOKEN"
    bot.run(TOKEN)                   
