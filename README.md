# server-handler

Gestionnaire du serveur personnel de **Bugz-gg**.

Il se compose d'un bot Telegram, et d'un bot Discord.

## Bot Telegram
Bot de gestion universel du serveur.  
Il contient un fichier de variables d'environnement `.env`  
qui se structure ainsi :
```md
TOKEN=TELEGRAM-TOKEN
ADMINS=ADMIN1, ADMIN2, ADMIN3
```
- Gestion de Factorio:
- - Lancer le serveur avec une certaine sauvegarde avec `/start $SAUVEGARDE`
- - Arrêter le serveur avec `/down`
- - Pour avoir la liste des saves factorio sur le server `/list`
- - Upload une save facorio avec `/upload`
- - Avoir la liste des commandes `/help`


## Bot Discord
Ce bot a pour seul vocation de gérer le container Factorio:
- Lancer le serveur avec `/startserver $SAUVEGARDE`
- Arrêter le serveur avec `/stopserver`

