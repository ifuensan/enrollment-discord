# 🤖 Bot de Inscripciones en Discord

Este bot de Discord permite a los usuarios inscribirse en cursos a través de una conversación sencilla. Recoge los datos y los guarda automáticamente en una hoja de cálculo de Google Sheets.

## 🚀 Funcionalidades

- Comando `/inscribirme`
- Interacción por mensaje privado o canal
- Guarda: nombre de usuario, curso, y correo electrónico
- Integra con Google Sheets

## ⚙️ Requisitos

- Python 3.9 o superior
- Una cuenta de Google con acceso a Google Sheets
- Un servidor de Discord donde tengas permisos de administrador

## 🧰 Instalación

### 1. **Clona este repositorio**

```bash
git clone https://github.com/tuusuario/discord-inscripciones-bot.git
cd enrollment-bot-discord
```

### 2. **Instala dependencias**

```bash
pip install -r requirements.txt
```

### 4. **Prepara la variables de entorno**

```bash
cp .env.sample .env
```

### 5. **Configura Google Sheets**

- Ve a [Google Cloud Console](https://console.cloud.google.com/)
- Crea un nuevo proyecto
- Activa:
  - Google Sheets API
  - Google Drive API
- Crea una cuenta de servicio:
  - Desde "IAM & Admin" > "Service Accounts" > Crear
  - Luego: “Keys” > “Add key” > JSON
- Renombra el archivo descargado como `credentials.json` y colócalo en el directorio raíz del proyecto.
- Crea una hoja de cálculo en Google Sheets llamada `Inscripciones Cursos`
  - Comparte el documento con el email de la cuenta de servicio
  - Añade una hoja llamada `Respuestas`
  - Encabezados: `Nombre de usuario | Curso | Correo`

### 6. **Configura Discord Bot**

- Ve a [Discord Developer Portal](https://discord.com/developers/applications)
- Crea una nueva aplicación y añade un bot
- Activa `Message Content Intent`
- Copia el Token y pégalo en tu archivo `.env`

```bash
DISCORD_TOKEN="TU_TOKEN_AQUÍ"
```

### 7. **Ejecuta el bot**

```bash
python bot.py
```

### 8. **Invita al bot a tu servidor**

En la misma app, ve a "OAuth2" > URL Generator
Selecciona:
- bot y applications.commands
- En “Bot Permissions” marca:
  - Send Messages
  - Read Message History
Copia el URL generado abajo, pégalo en el navegador y añádelo a tu servidor.


## ✨ Cómo usar

En un canal donde el bot tenga acceso:

```bash
/inscribirme
```

El bot preguntará por:
- Curso
- Correo electrónico

Y guardará la información en la hoja de cálculo configurada.

## 📂 Estructura del proyecto

```
📁 discord-inscripciones-bot
├── bot.py
├── credentials.json
├── README.md
└── requirements.txt
```

## 🧪 Dependencias

Inclúyelas en un archivo `requirements.txt`:

```txt
discord.py
gspread
oauth2client
```

## 📌 Próximas mejoras (sugerencias)

- Interfaz con botones (`discord.ui`)
- Validación de correos
- Notificación por DM
- Panel de administración en web

## 🛡️ Licencia

MIT License
