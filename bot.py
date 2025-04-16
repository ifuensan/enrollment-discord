import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Configurar acceso a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Inscripciones Cursos").worksheet("Respuestas")

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

@bot.command(name="inscribirme")
async def inscribirme(ctx):
    await ctx.send("¿A qué curso te quieres inscribir?")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    curso = await bot.wait_for("message", check=check)
    await ctx.send("¿Cuál es tu correo electrónico?")
    correo = await bot.wait_for("message", check=check)

    # Guardar en la hoja
    sheet.append_row([ctx.author.name, curso.content, correo.content])
    await ctx.send("✅ ¡Inscripción completada!")

bot.run("AQUÍ_TU_TOKEN")
