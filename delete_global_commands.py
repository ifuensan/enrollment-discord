
import discord
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

    print("🧹 Eliminando todos los comandos globales...")
    
    tree.clear_commands(guild=None)     # ← Esto borra comandos globales
    await tree.sync()                   # ← Esto sincroniza la eliminación

    print("✅ Comandos globales eliminados.")
    await bot.close()

bot.run(DISCORD_TOKEN)
