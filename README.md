# sauvegarde-worpress
Script python avec sauvegarde déportée en ftp et rapport par email (msmtp)
Les tests on été fait sur Pyhton 2.7.17 et Debian 10

LE SCRIPT FAIT UNE SAUVEGARDE DE TYPE "COMPLETE" EN VUE D'UNE SAUVEGARDE D'UN SITE WORDPRESS
L'envoi du mail fait appel à msmtp (adapter selon votre infrastricture) via un script bash.
Le script sauvegarde également les fichiers hosts, hostname, interfaces, resolv.conf et 000-default.conf
"Un dump" de la base Mysql est réalisée afin de pouvoir éventuellement faire une intervention manuelle sur la base de donnée

Variables à adapter :

ATTENTION: dans ce script j'efface les anciennes sauvegardes (2mn soit 120 secondes), CHANGER CETTE VALEUR EN SECONDES pour le nombre de jours pendant lesquels vous voulez conserver vos sauvegardes
LIGNE avec la variable deux_minutes_ago = time.time() - 120

BACKUP_PATH = '/home/backup/' >> dossier pour la sauvegarde en local sur le serveur web
WEB_PATH = '/var/www/html/wordpress' >> dossier du site wordpress sur le serveur web
DB_USER = 'root' >> Compte administrateur de la base de données 
DB_USER_PASSWORD = 'Admin-pwd' >> Mode de passe du compte administrateur de la base de données
DB_NAME = 'wordpress_db' >> Nom de la base de données Wordpress
FTP_IP_SRV='192.168.134.133' >> Adresse IP sur serveur FTP distant
FTP_PORT='21'>> Port du serveur FTP
FTP_USER='sauvegarde' >> Compte utilisateur autorisé sur le FTP
FTP_PASS='Admin-sav' >> Mot de passe du compte FTP
FILE_SAV_DUMPSQL =  DATETIME + "-dumpsql.tar.bz2" >> vous pouvez personnaliser le nom de fichier
FILE_SAV_WORDPRESS =  DATETIME + "-wordpress.tar.bz2" >> vous pouvez personnaliser le nom de fichier
FILE_SAV_MYSQL =  DATETIME + "-mysql.tar.bz2" >> vous pouvez personnaliser le nom de fichier
FILE_SAV_LAN = DATETIME + "-conf-lan.tar.bz2" >> vous pouvez personnaliser le nom de fichier
FILE_SAV_APACHE_DEFAULT = DATETIME + "-apache-default.tar.bz2" >> vous pouvez personnaliser le nom de fichier
FILE_LOG = DATEJOUR + "-log">> vous pouvez personnaliser le nom de fichier



