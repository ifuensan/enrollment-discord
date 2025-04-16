🚀 Paso 4: Conectar a Google Sheets
1. Crea una hoja de cálculo nueva en Google Sheets

    Llama el documento Inscripciones Cursos

    Cambia el nombre de la primera pestaña a Respuestas

    Agrega encabezados: Nombre de usuario | Curso | Correo

2. Configura las credenciales

    Ve a Google Cloud Console

    Crea un nuevo proyecto

    Activa la API de Google Sheets y Google Drive

    Crea una Service Account

        Luego: “Manage keys” > “Add key” > JSON

        Guarda el archivo como credentials.json en el mismo directorio de tu bot

3. Comparte la hoja con el email del bot

    En el Google Sheet: Compartir > Añade el email del bot (acabado en @gserviceaccount.com) y dale acceso de editor

También podemos empacarlo para que lo puedas subir a un VPS o a Replit, como tú prefieras.
