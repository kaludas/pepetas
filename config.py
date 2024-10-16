import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


if TOKEN is None:
    raise ValueError("Le token du bot n'a pas été trouvé dans les variables d'environnement.")
else:
    print("Token chargé avec succès.")