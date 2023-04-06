# Imports
import discord # Interactions avec l'API Discord
from dotenv import load_dotenv # Chargement des variables d'environnement
import requests # Requêtes HTTP
import os # Manipulation des fichiers et dossiers
import datetime # Gestion des dates

# On charge le fichier .env
load_dotenv()

# Récupération des variables d'environnement
discord_token = os.getenv('DISCORD_TOKEN') # token du bot
target_channel_id = os.getenv('TARGET_CHANNEL_ID') # ID du canal où est le bot


# On crée une instance du client discord avec tous les droits
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Fonction qui télécharge l'image - rajout de "message" en paramètre pour pouvoir envoyer le message de confirmation dans le canal
async def download_image(url, filename, message):
    response = requests.get(url)
    if response.status_code == 200:
        current_date = datetime.datetime.now() # On récupère la date du jour pour formater le nom du futur répertoire de destination
        folder_name = current_date.strftime("%Y-%m-%d")
        save_folder = f"/media/guillaume/Bonus/Midjourney/Images/{folder_name}" # dossier où sont téléchargées les images
        if not os.path.exists(save_folder): # si le répertoire n'existe pas, on le crée
            os.makedirs(save_folder) 
        with open(os.path.join(save_folder, filename), 'wb') as f: # on ouvre le fichier en mode écriture binaire
            f.write(response.content) # on écrit le contenu de la réponse dans le fichier
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

    # Commande pour vérifier si le script tourne
    if message.content == '!test':
        await message.channel.send("Salut sir ! J'trouve qu'il fait beau, mais encore frais. Mais beau.")
    
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