# Imports
import discord # Interactions avec l'API Discord
from dotenv import load_dotenv # Chargement des variables d'environnement
import requests # requêtes HTTP
import os # Manipulation des fichiers et dossiers

# On charge le fichier .env
load_dotenv()

# Récupération des variables d'environnement
discord_token = os.getenv('DISCORD_TOKEN') # token du bot
save_folder = os.getenv('SAVE_FOLDER') # dossier où sont téléchargées les images
target_channel_id = os.getenv('TARGET_CHANNEL_ID') # ID du canal où est le bot

# On crée une instance du client discord avec tous les droits
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Fonction qui télécharge l'image - rajout de "message" en paramètre pour pouvoir envoyer le message de confirmation dans le canal
async def download_image(url, filename, message):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(save_folder, filename), 'wb') as f:
            f.write(response.content)
            print("Image téléchargée: {0}".format(filename))
        await message.channel.send("Mission accomplie, formation du lézard !")


# Quand le bot est prêt à être utilisé
@client.event
async def on_ready():
    print("Bot connecté en tant que {0.user}".format(client))
    # Le bot envoie un message dans le canal "général"
    await client.get_channel(1087111766384853104).send("Vous m'avez d'mandé Sir ?") # TODO: à modifier par la variable d'environnement target_channel_id (ne fonctionne pas)


# Quand un message est envoyé dans le canal
@client.event
async def on_message(message):
    # Si le message est envoyé par le bot, on ne fait rien
    if message.author == client.user:
        return

    # Si le message contient bien une image Upscaled, on l'enregistre
    if "Image #" in message.content:
        attachment= message.attachments[0] # on stocke les informations de l'image
        print('Image détectée', attachment.url, attachment.filename)
        await download_image(attachment.url, attachment.filename, message) # on télécharge l'image

    # Commande pour arrêter le bot
    # if message.content == '!stop':
    #     await message.channel.send("Ca d'vient n'importe quoi, j'me barre !")
    #     await client.close()

    # Commande pour lancer le bot
    # if message.content == '!start':
    #     await client.start(discord_token)
    #     await message.channel.send("Vous m'avez d'mandé Sir ?")

# On lance le bot
client.run(discord_token)