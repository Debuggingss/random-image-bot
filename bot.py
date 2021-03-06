import aiohttp
import discord
from discord.ext import commands

# Client secret token
TOKEN = "<YOUR_TOKEN_HERE>"

# Sets prefix and removes the default help command so we can overwrite it
client = commands.Bot(command_prefix='.')
client.remove_command('help')


@client.event
async def on_ready():
    # Set game activity to a custom message
    activity = discord.Game(name="with da images!")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print('[IMGBOT] Bot started up..."')


@client.command()
async def help(ctx, arg: str = ''):
    """
    :param ctx: Message object
    :param arg: Argument for setting language
    :return: None
    """
    if arg == 'hu':
        embed = discord.Embed(title="**Random Kép Bot Segítség**")
        embed.add_field(name='.rndimg <size>', value='Küld egy véletlenszerű négyzet alakú képet a megadott mérettel.')
        embed.add_field(name='.rndimg <size1> <size2>', value='Küld egy véletlenszerű képet a megadott 2 mérettel.')
        embed.add_field(name=':flag_gb:', value='For english help simply use the command `.help`!')
    else:
        embed = discord.Embed(title="**Random Image Bot Help**")
        embed.add_field(name='.rndimg <size>', value='Returns a random square image with the given size.')
        embed.add_field(name='.rndimg <size1> <size2>', value='Returns a random image with the 2 given dimensions.')
        embed.add_field(name=':flag_hu:', value='Magyar segítségért használd a `.help hu` parancsot!')
    await ctx.send(embed=embed)


@client.command()
async def rndimg(ctx, width: str, height: str = ''):
    """
    :param ctx: Message Object
    :param width: Image width used for the image (required)
    :param height: Image height used for the image (optional)
    :return: A random image
    """
    if width != '' and width.isnumeric() and height == '':
        async with aiohttp.ClientSession() as session:
            image = await session.get(f"https://picsum.photos/{width}")
            embed = discord.Embed(title='Random Image', description=f'Size: {width}\n'
                                                                    f'Link: {image.url}')
            embed.set_image(url=str(image.url))
        await ctx.send(embed=embed)
    if width != '' and width.isnumeric() and height != '' and height.isnumeric():
        async with aiohttp.ClientSession() as session:
            image = await session.get(f"https://picsum.photos/{width}/{height}")
            embed = discord.Embed(title='Random Image', description=f'Width: {width}\n'
                                                                    f'Height: {height}\n'
                                                                    f'Link: {image.url}')
            embed.set_image(url=str(image.url))
        await ctx.send(embed=embed)


# Log the client in with the set token
client.run(TOKEN)
