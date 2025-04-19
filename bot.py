import discord
from discord.ext import commands
from discord import app_commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv
from datetime import datetime
from discord.ui import Button, View
from functions import obtener_cursos_abiertos, obtener_todos_cursos, es_correo_valido

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CANAL_PERMITIDO_ID = int(os.getenv("CANAL_PERMITIDO_ID"))

print(f"GUILD_ID: {GUILD_ID} ({type(GUILD_ID)})")
print(f"CANAL_PERMITIDO_ID: {CANAL_PERMITIDO_ID} ({type(CANAL_PERMITIDO_ID)})")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

#Hoja de inscripciones
sheet = client.open("Inscripciones Cursos").worksheet("Respuestas")

#Hoja de cursos
sheet_cursos = client.open("Master Calendar Courses 2025 ").worksheet("Courses ready")

# Vista de botones de valoración
class ValoracionView(View):
    def __init__(self):
        super().__init__(timeout=30)
        self.valor_seleccionada = None

        for i in range(1, 6):
            self.add_item(ValorButton(str(i)))

class ValorButton(Button):
    def __init__(self, valor):
        super().__init__(label=valor, style=discord.ButtonStyle.primary)
        self.valor = valor

    async def callback(self, interaction: discord.Interaction):
        self.view.valor_seleccionada = self.valor
        await interaction.response.send_message(f"✅ ¡Gracias por valorar con un {self.valor}!", ephemeral=True)
        self.view.stop()


@bot.tree.command(name="myping", description="Test del bot")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def myping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!", ephemeral=True)
    
# Comando principal de inscripción
@bot.tree.command(name="inscribirme", description="Inscribirte a un curso")
@app_commands.guilds(discord.Object(id=GUILD_ID))
#@app_commands.guilds(discord.Object(id=1360683780104392916))
async def inscribirme(interaction: discord.Interaction):
    
    if interaction.channel_id != CANAL_PERMITIDO_ID:
        await interaction.response.send_message(
            f"❌ Este comando solo se puede usar en <#{CANAL_PERMITIDO_ID}>.",
            ephemeral=True
        )
        return    
    
    # Primera y única respuesta inicial
    await interaction.response.send_message("🔄 Obteniendo lista de cursos...", ephemeral=True)
    
    cursos = obtener_todos_cursos(client)  # o cursos_abiertos
    lista_cursos = "\n".join([f"• {curso}" for curso in cursos])
    mensaje = f"📚 ¿A qué curso te quieres inscribir?\n\n{lista_cursos}"
    
    # Respuesta posterior (seguimiento)
    await interaction.followup.send(mensaje, ephemeral=True)         

    def check(m):
        return m.author.id == interaction.user.id and m.channel.id == interaction.channel_id

    curso = await bot.wait_for("message", check=check)
    
    await interaction.followup.send("✉️ ¿Cuál es tu correo electrónico?", ephemeral=True)
    #correo = await bot.wait_for("message", check=check)
    while True:
        correo = await bot.wait_for("message", check=check)
        if es_correo_valido(correo.content):
            break
        else:
            await interaction.followup.send("❌ Ese correo no parece válido. Intenta de nuevo (ej. nombre@dominio.com)", ephemeral=True)

    sheet.append_row([interaction.user.name, curso.content, correo.content])
    await interaction.followup.send("✅ ¡Gracias! Te hemos inscrito correctamente.", ephemeral=True)
    await mostrar_valoracion(interaction, sheet)


# Comando para valorar el proceso
@bot.tree.command(name="muestra_valoracion", description="Valora el proceso de inscripción (1-5)")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def muestra_valoracion(interaction: discord.Interaction):
    await interaction.response.send_message("🔄 Muestra Valoracion", ephemeral=True)



@bot.tree.command(name="valorar", description="Valora el proceso de inscripción (1-5)")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def valorar(interaction: discord.Interaction):
    #await interaction.response.send_message("🔄 Valorar 12345", ephemeral=True)
    view = ValoracionView()
    await interaction.response.send_message(
        "📝 ¿Cómo valorarías el proceso de inscripción?", view=view, ephemeral=True
    )
    await view.wait()

    if view.valor_seleccionada:
        nombre = interaction.user.name
        valor = view.valor_seleccionada

        # Buscar la fila del usuario por nombre
        filas = sheet.get_all_values()
        for i, fila in enumerate(filas):
            if fila[0] == nombre:
                columna_valoracion = len(fila) + 1 if len(fila) < 4 else 4  # por si ya existe
                sheet.update_cell(i + 1, columna_valoracion, valor)
                break 

async def mostrar_valoracion(interaction, sheet):
    view = ValoracionView()
    await interaction.followup.send(
        "📝 ¿Cómo valorarías el proceso de inscripción?", view=view, ephemeral=True
    )
    await view.wait()

    if view.valor_seleccionada:
        nombre = interaction.user.name
        valor = view.valor_seleccionada

        filas = sheet.get_all_values()
        for i, fila in enumerate(filas):
            if fila[0] == nombre:
                columna_valoracion = len(fila) + 1 if len(fila) < 4 else 4
                sheet.update_cell(i + 1, columna_valoracion, valor)
                break   

@bot.event
async def on_ready():
    synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"✅ Bot listo como {bot.user}")
    print(f"🧾 Slash commands registrados solo en este servidor: {[c.name for c in synced]}")

bot.run(DISCORD_TOKEN)