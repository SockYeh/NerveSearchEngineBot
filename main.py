from os import link
import discord, json, requests, re, urllib.parse
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from discord.ext import commands


token = ''
bot = commands.Bot(command_prefix="-", case_insensitive=True)
ua = UserAgent()
bot.remove_command("help")


@bot.event
async def on_ready():
    print("Bot is ready.")
    await bot.change_presence(
        activity=discord.Game(name=f"Searching stuff in {len(bot.guilds)} servers!")
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Please provide a search term.")
        return


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! My latency/ping is {round(bot.latency * 1000)}ms.")


@bot.command()
async def invite(ctx):
    embed = discord.Embed(
        title="Invite Me!",
        description="You can invite me [here](https://discord.com/api/oauth2/authorize?client_id=857523507709214750&permissions=8&scope=bot).",
        color=0xFFA500,
    )
    embed.set_footer(
        text=f"Command Invoked By {ctx.author} - Made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )

    await ctx.send(embed=embed)


@bot.command()
async def google(ctx, *, query):
    query = urllib.parse.quote_plus(query)

    r = requests.get(f"https://www.google.com/search?q={query}")
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("a")
    embed = discord.Embed(title="Google Search", color=0xFFA500)
    embed.set_footer(
        text=f"Command Invoked By {ctx.author} - Made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )

    looped = 0

    for result in results:
        resn = result.text
        result = result.get("href")
        if "/url?q=" in result:
            result = result.replace("/url?q=", "")
            looped += 1
            embed.add_field(
                name=str(looped),
                value=f"[{resn.strip()}]({result.strip()})",
                inline=True,
            )
        if looped == 10:
            break
    await ctx.send(embed=embed)


@bot.command()
async def yahoo(ctx, *, query):
    query = urllib.parse.quote_plus(query)

    r = requests.get(f"https://www.search.yahoo.com/search?q={query}")
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("a")
    embed = discord.Embed(title="Yahoo Search", color=0xFFA500)
    embed.set_footer(
        text=f"Command Invoked By {ctx.author} - Made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )

    looped = 0

    for result in results:
        resn = result.text
        result = result.get("href")
        if "yahoo" not in result and "http" in result:
            looped += 1
            embed.add_field(
                name=str(looped),
                value=f"[{resn.strip()}]({result.strip()})",
                inline=True,
            )
        if looped == 10:
            break
    await ctx.send(embed=embed)


@bot.command()
async def youtube(ctx, *, query):
    query = urllib.parse.quote_plus(query)

    seen = []

    r = requests.get(
        f"https://www.youtube.com/results?search_query={query}",
        headers={"User-Agent": ua.random},
    )
    embed = discord.Embed(title="Youtube Search", color=0xFFA500)
    embed.set_footer(
        text=f"Command Invoked By {ctx.author} - Made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )

    looped = 0
    soup = BeautifulSoup(r.text, "html.parser")

    for item, name in zip(
        re.findall(r"videoId\":\"(\S+)", str(soup)),
        re.findall(r"text\":\"(\S+)", str(soup)),
    ):
        try:
            name = re.findall(r"(.*?)\",", str(name))[0]
            item = re.findall(r"(.*?)\",", str(item))[0]
            if item not in seen:
                seen.append(item)
                item = f"https://youtube.com/watch?v={item}"
                looped += 1
                embed.add_field(
                    name=str(looped),
                    value=f"[{name}]({item})",
                    inline=True,
                )
            if looped == 10:
                break
        except:
            continue
    await ctx.send(embed=embed)


@bot.command()
async def bing(ctx, *, query):
    query = urllib.parse.quote_plus(query)

    r = requests.get(
        f"https://www.bing.com/search?q={query}", headers={"User-Agent": ua.chrome}
    )
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("a")
    embed = discord.Embed(title="Bing Search", color=0xFFA500)
    embed.set_footer(
        text=f"Command Invoked By {ctx.author} - Made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )

    looped = 0
    for result in results:
        try:
            resn = result.text
            result = result.get("href")
            if "bing" not in result and "http" in result:
                looped += 1
                embed.add_field(
                    name=str(looped),
                    value=f"[{resn.strip()}]({result.strip()})",
                    inline=True,
                )
            if looped == 10:
                break
        except:
            continue
    await ctx.send(embed=embed)


@bot.command()
async def brave(ctx, *, query):
    query = urllib.parse.quote_plus(query)

    r = requests.get(
        f"https://search.brave.com/search?q={query}", headers={"User-Agent": ua.chrome}
    )
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("a")
    embed = discord.Embed(title="Brave Search", color=0xFFA500)
    embed.set_footer(
        text=f"Command Invoked By {ctx.author} - Made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )
    looped = 0
    for result in results:
        try:
            resn = result.text.strip().split(" ")[0]
            result = result.get("href")
            if "brave" not in result and "http" in result:
                looped += 1
                embed.add_field(
                    name=str(looped),
                    value=f"[{resn.strip()}]({result.strip()})",
                    inline=True,
                )
            if looped == 10:
                break
        except:
            continue
    await ctx.send(embed=embed)


@bot.command(aliases=["stackoverflow"])
async def stackof(ctx, *, query):
    query = urllib.parse.quote_plus(query)

    r = requests.get(
        f"https://google.com/search?q=inurl:stackoverflow.com+python+OR+site:stackoverflow.com+{query}",
        headers={"User-Agent": ua.chrome},
    )
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("a")
    embed = discord.Embed(title="Stack Overflow Search", color=0xFFA500)
    embed.set_footer(
        text=f"Command Invoked By {ctx.author} - Made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )
    looped = 0
    for result in results:
        try:
            link = result.get("href")
            if "stackoverflow.com/questions" in link:
                link = link.replace("/url?q=", "").split("&")[0]
                name = link.split("/")[5].replace("-", " ")
                looped += 1
                embed.add_field(
                    name=str(looped),
                    value=f"[{name.strip()}]({link.strip()})",
                    inline=True,
                )
            if looped == 10:
                break
        except:
            continue
    await ctx.send(embed=embed)


@bot.command()
async def reddit(ctx, *, query):
    query = query.replace(" ", "_")
    r = requests.get(
        f"https://www.reddit.com/r/{query}", headers={"User-Agent": ua.chrome}
    )
    soup = BeautifulSoup(r.text, "html.parser")
    embed = discord.Embed(title="Reddit Search", color=0xFFA500)
    embed.set_footer(
        text=f"Command Invoked By {ctx.author} - Made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )
    looped = 0

    for post in soup.find_all("a"):
        try:
            if f"reddit.com/r/{query}/comments" in post["href"]:
                name = post["href"].split("/")[7]
                name = name.replace("_", " ")
                link = post["href"]
                looped += 1
                embed.add_field(
                    name=str(looped),
                    value=f"[{name.strip()}]({link.strip()})",
                    inline=True,
                )
            if looped == 10:
                break
        except:
            continue
    await ctx.send(embed=embed)


@bot.command()
async def github(ctx, *, query):
    query = urllib.parse.quote_plus(query)

    r = requests.get(
        f"https://github.com/search?q={query}", headers={"User-Agent": ua.chrome}
    )
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("a", class_="v-align-middle")
    embed = discord.Embed(title="Github Search", color=0xFFA500)
    embed.set_footer(
        text=f"Command Invoked By {ctx.author} - Made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )

    looped = 0
    for result in results:
        try:
            resn = result.text.split("/")[1]
            result = result.get("href")
            result = f"https://github.com{result}"
            looped += 1
            embed.add_field(
                name=str(looped),
                value=f"[{resn.strip()}]({result.strip()})",
                inline=True,
            )
            if looped == 10:
                break
        except:
            continue
    await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Commands", color=0xFFA500)
    embed.set_footer(
        text=f"Command Invoked By {ctx.author} - Made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )
    embed.add_field(
        name="google",
        value="Searches Google for your query",
        inline=False,
    )
    embed.add_field(
        name="yahoo",
        value="Searches Yahoo for your query",
        inline=False,
    )
    embed.add_field(
        name="bing",
        value="Searches Bing for your query",
        inline=False,
    )
    embed.add_field(
        name="brave",
        value="Searches Brave for your query",
        inline=False,
    )
    embed.add_field(
        name="youtube",
        value="Searches Youtube for your query",
        inline=False,
    )
    embed.add_field(
        name="stackoverflow",
        value="Searches Stack Overflow for your query",
        inline=False,
    )
    embed.add_field(
        name="reddit",
        value="Searches Reddit for your query",
        inline=False,
    )
    embed.add_field(
        name="github",
        value="Searches Github for your query",
        inline=False,
    )
    embed.add_field(
        name="ping",
        value="Shows my ping",
        inline=False,
    )
    embed.add_field(
        name="help",
        value="Shows this message",
        inline=False,
    )
    await ctx.send(embed=embed)


bot.run(token)
