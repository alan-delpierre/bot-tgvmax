import logging, os
from dotenv import load_dotenv
from api import test_connect, pull_datas
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)



bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name='del')
async def delete(ctx, number_of_messages: int):
    messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()

    for each_message in messages :
        await each_message.delete()


@bot.command(name='get')
async def get(ctx, message):
    infos = message.split('/')
    if len(infos) != 3 :
        await ctx.send("Le format de la demande doit être '!get VILLE1/VILLE2/YYYY-MM-DD'")
    origine_city = infos[0]
    destination_city = infos[1]
    date = infos[2]
    trains_list = pull_datas(origine_city, destination_city, date)
    if len(trains_list) == 0 :
        message = "Il y a n'y a pas de train disponible à cette date."
    else :
        message = "Il y a {0} trains disponibles \n".format(len(trains_list))
        for i in range(len(trains_list)):
            message2 = "Train numéro {0} : \nHeure de départ : {1}\n Heure d'arrivée : {2}\n\n".format(trains_list[i]['train'], trains_list[i]['depart'], trains_list[i]['arrive'])
            message += message2

    await ctx.send(message)

bot.run(TOKEN)