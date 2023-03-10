#pylint:disable=E1123
#pylint:disable=E0237
from __future__ import absolute_import
from discord.ext import commands
from bs4 import BeautifulSoup 
import random
import discord
import praw
import datetime
import requests


intents = discord.Intents().all()
intents.members = True
intents.messages = True
intents.message_content = True

TOKEN = "TOKEN"


prefix = '!'
bot = commands.Bot(command_prefix=prefix, intents=intents)

reddit = praw.Reddit(
client_id='CLIENT_ID',
client_secret='CLIENT_SECRET',
user_agent='USER_AGENT',
username='USERNAME',
password='PASSWORD'
)

reddit.read_only = False


        
        
@bot.command()
async def searchgsi(ctx, *, device):
    SEARCH_URLS = [
        "https://github.com/phhusson/treble_experimentations/wiki",
        "https://forum.xda-developers.com/c/treble-roms-and-development.8511/",
        "https://www.reddit.com/r/Android/comments/9h05x7/generic_system_image_for_project_treble_devices/",
        "https://forum.xda-developers.com/c/android-general/generic-system-image-gsi-list-t3832615",
        "https://forum.xda-developers.com/t/android-10-q-generic-system-image.3952019/",
        "https://gitlab.com/shagbag913/vendor-gsis/-/wikis/home",
        "https://github.com/solutionfixxxer/Project-Treble-Experience/wiki",
        "https://magiskzip.com/gsi-list-phhusson/",
        "https://www.lineageos.org/",
        "https://download.lineageos.org/",
        "https://forum.xda-developers.com/t/gsis-and-treble-roms-index-for-all-devices.3824063/",
        "https://forum.xda-developers.com/t/gsi-mega-thread-generic-system-image-t3861945/",
        "https://sourceforge.net/projects/ezdroid/files/Generic%20System%20Image/",
        "https://developers.google.com/android/guides/gsi",
        "https://sourceforge.net/projects/havoc-os/files/GSI/",
        "https://get.delta.chat/android/nightly/"
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
                if device.lower() in link.text.lower() and link["href"].endswith(".img") or link["href"].endswith(".zip") or link["href"].endswith(".img.xz") or link["href"].endswith(".gz") or link["href"].endswith(".xz"):
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

    search_engines = [
        {'name': 'DuckDuckGo', 'url': 'https://duckduckgo.com/html/?q={}'},
        {'name': 'Google', 'url': 'https://www.google.com/search?q={}&num=20'},
        {'name': 'Bing', 'url': 'https://www.bing.com/search?q={}&count=20'},
        {'name': 'Yahoo', 'url': 'https://search.yahoo.com/search?p={}&n=20'},
        {'name': 'Ask', 'url': 'https://www.ask.com/web?q={}&qsrc=0&o=0&l=dir&qo=homepageSearchBox'},
        {'name': 'AOL', 'url': 'https://search.aol.com/aol/search?q={}&count=20'},
        {'name': 'Dogpile', 'url': 'https://www.dogpile.com/serp?q={}&num=20'},
        {'name': 'StartPage', 'url': 'https://www.startpage.com/do/dsearch?query={}&cat=web&pl=ext-ff&language=english&lui=english'},
        {'name': 'Yandex', 'url': 'https://yandex.com/search/?text={}&lr=213'},
        {'name': 'Wolfram Alpha', 'url': 'https://www.wolframalpha.com/input/?i={}'}
    ]

    random.shuffle(search_engines)

    results = []
    for engine in search_engines:
        url = engine['url'].format(query)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('.result__url')
        titles = soup.select('.result__title')
        for index, link in enumerate(links[:20]):
            result = {'title': titles[index].text, 'url': link.get('href'), 'engine': engine['name']}
            results.append(result)

    if not results:
        await ctx.send('No results found.')
    else:
        random.shuffle(results)
        embed = discord.Embed(title=f"Search Results for '{query}':", color=0x00ff00)
        for index, result in enumerate(results[:20], start=1):
            embed.add_field(name=f"Result {index} ({result['engine']}): {result['title']}", value=result['url'], inline=False)
        await ctx.send(embed=embed)


@bot.command()
async def searchfirmware(ctx, *, model):
    SEARCH_URLS = [
        ("https://www.sammobile.com/firmwares/search", {"q": model}),
        ("https://updato.com/firmware-archive-select-model", {"model_name": model}),
        ("https://www.firmware.science/", {"s": model}),
        ("https://www.officialroms.com/", {"s": model}),
        ("https://www.androidfilehost.com/search", {"s": model}),
        ("https://firmwarefile.com/", {"q": model}),
        ("https://www.mobilesfirmware.com/", {"s": model}),
        ("https://androidmtk.com/category/firmware", {"s": model}),
        ("https://firmwarex.net/", {"s": model}),
        ("https://www.needrom.com/", {"s": model}),
        ("https://romprovider.com/search.php", {"q": model}),
        ("https://www.romkingz.net/", {"s": model}),
        ("https://www.mymobitips.com/search/label/Firmware", {"query": model}),
        ("https://romfast.com/", {"s": model}),
        ("https://androidhost.org/search/", {"q": model}),
        ("https://www.firmwarezip.com/search", {"query": model}),
        ("https://gsm-file.com/search/", {"q": model}),
        ("https://gsm-firmware.com/search", {"query": model}),
        ("https://www.romflasher.com/search?q=", {"q": model}),
        ("https://forum.xda-developers.com/search/thread", {"q": model}),
    ]

    firmware_found = False
    for url, params in SEARCH_URLS:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            for link in soup.find_all("a", href=True):
                if model.lower() in link.text.lower() and "download" in link.text.lower():
                    await ctx.send(embed=discord.Embed(title="Firmware Download Link", description=link["href"], color=0x00ff00))
                    firmware_found = True
                    break
        if firmware_found:
            break
    
    if not firmware_found:
        firmware_links = []
        search_engines = [
            ("https://www.google.com/search", {"q": f"{model} firmware download"}),
            ("https://duckduckgo.com/html/", {"q": f"{model} firmware download"}),
            ("https://www.bing.com/search", {"q": f"{model} firmware download"}),
            ("https://www.yandex.com/search/", {"text": f"{model} firmware download"}),
        ]
        for url, params in search_engines:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            }
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                for link in soup.find_all("a", href=True):
                    if "http" in link["href"] and "download" in link.text.lower():
                        firmware_links.append(link["href"])

    if not firmware_links:
        await ctx.send(f"No firmware found for {model}.")
    else:
        firmware_links = sorted(firmware_links, key=len)[:10]
        firmware_list = "\n".join(firmware_links)
        firmware_embed = discord.Embed(title="Firmware Download Links", description=firmware_list, color=0x00ff00)
        for i, link in enumerate(firmware_links, 1):
            firmware_embed.add_field(name=f"Link {i}", value=link, inline=False)
        await ctx.send(embed=discord.Embed(title="Firmware Download Links", description=firmware_list, color=0x00ff00))



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
    global TOKEN
    bot.run(TOKEN)
