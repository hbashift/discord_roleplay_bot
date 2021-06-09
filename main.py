from datetime import datetime
import discord
from discord.ext import commands
import random
import requests
import json
import aiohttp
import io

TOKEN = 'ODUxOTA1NjE5MTYyMDM4Mjgy.YL_E7w.aGhm68sU-jadgTK10CH0wNMfozY'

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='()', description=description, intents=intents)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('```Format has to be in NdN!```')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))


@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


@bot.command()
async def fuck(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.trigger_typing()
    await ctx.send(f'Иди нахуй, {member.mention}!')


@bot.command()
async def horny(ctx, member: discord.Member = None):
        '''Horny license just for u'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://some-random-api.ml/canvas/horny?avatar={member.avatar_url_as(format="png")}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "horny.png")
                    em = discord.Embed(
                        title="bonk",
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://horny.png")
                    await ctx.send(embed=em, file=file)
                else:
                    await ctx.send('No horny :(')
                await session.close()


@bot.command(aliases=['lyrc'])  # adding a aliase to the command so we can use !lyrc or !lyrics
async def lyrics(ctx, *, search=None):
    """A command to find lyrics easily!"""

    if not search:  # if user hasnt typed anything, throw a error
        embed = discord.Embed(title="No search argument!",
                              description="You havent entered anything, so i couldnt find lyrics!")
        await ctx.reply(embed=embed)

        # ctx.reply is available only on discord.py 1.6.0!

    song = search.replace(' ', '%20')  # replace spaces with "%20"

    async with aiohttp.ClientSession() as lyricsSession:  # define session
        async with lyricsSession.get(f'https://some-random-api.ml/lyrics?title={song}') as jsondata:  # define json data
            if not (300 > jsondata.status >= 200):
                await ctx.send(f'Recieved Poor Status code of {jsondata.status}.')
            else:
                lyricsData = await jsondata.json()  # load json data
        songLyrics = lyricsData['lyrics']  # the lyrics
        songArtist = lyricsData['author']  # the authors name
        songTitle = lyricsData['title']  # the songs title

        try:
            for chunk in [songLyrics[i:i + 2000] for i in range(0, len(songLyrics),
                                                                2000)]:  # if the lyrics extend the discord character limit (2000): split the embed
                embed = discord.Embed(title=f'{songTitle} by {songArtist}', description=chunk,
                                      color=discord.Color.blurple())
                embed.timestamp = datetime.utcnow()

                await lyricsSession.close()  # closing the session

                await ctx.reply(embed=embed)

        except discord.HTTPException:
            embed = discord.Embed(title=f'{songTitle} by {songArtist}', description=chunk,
                                  color=discord.Color.blurple())
            embed.timestamp = datetime.utcnow()

            await lyricsSession.close()  # closing the session

            await ctx.reply(embed=embed)


@bot.command
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
    print(response)
    json_data = json.loads(response.text) # Извлекаем JSON
    print(json_data)

    embed = discord.Embed(color = 0xff9900, title = 'Random Fox') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed


@bot.command(aliases=['s'])
async def suck(ctx, member: discord.Member):
    await ctx.trigger_typing()
    await ctx.send(f'{member.mention} опять сосет :))))!')

bot.run(TOKEN)
