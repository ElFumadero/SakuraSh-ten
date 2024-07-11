import discord
from discord.ext import commands
import aiohttp

# Configuration du bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  
bot = commands.Bot(command_prefix='!', intents=intents)


CHEAPSHARK_API_URL = 'https://www.cheapshark.com/api/1.0/games'


DEVELOPPEUR = "El Fumadero"

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name} (Développé par {DEVELOPPEUR})')

@bot.command(name="comparer")
async def comparer(ctx, *, game_name: str):
    params = {
        'title': game_name,
        'limit': 10  # Limite de résultats à 10
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(CHEAPSHARK_API_URL, params=params) as response:
            if response.status != 200:
                await ctx.send(f"Erreur lors de la recherche du jeu {game_name}. Réessayez plus tard.")
                return
            
            data = await response.json()
            
            if not data:
                await ctx.send(f"Aucun résultat trouvé pour le jeu {game_name}.")
                return
            
            embed = discord.Embed(title=f"Résultats de la recherche pour {game_name}")
            for game in data:
                embed.add_field(name=game['external'], 
                                value=f"Prix: ${game['cheapest']}\n[Lien](https://www.cheapshark.com/redirect?dealID={game['cheapestDealID']})")
            
            embed.set_footer(text=f"Développé par {DEVELOPPEUR}")
            await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! (Développé par {DEVELOPPEUR})")

@bot.command(name="credits")
async def developpeur(ctx):
    await ctx.send(f"Ce bot a été dev par {DEVELOPPEUR}.")


@bot.command(name="aide")
async def aide(ctx):
    embed = discord.Embed(title="Commandes du Bot", description="Voici la liste des commandes disponibles:")
    embed.add_field(name="!ping", value="Vérifie si le bot est en ligne", inline=False)
    embed.add_field(name="!comparer (nom du jeux)", value="Compare les prix d'un jeu et affiche les meilleures offres disponibles ", inline=False)
    embed.add_field(name="!credits", value="Affiche le nom du développeur", inline=False)
    await ctx.send(embed=embed)


# Token Du Bot
bot.run('TOKEN_DU_BOT')
