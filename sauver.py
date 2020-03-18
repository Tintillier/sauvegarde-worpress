#!/usr/bin/python2
# -*- coding: utf-8 -*-

#import librairies
import os
import time
import datetime
import sys
import subprocess
import glob
import ftplib
import shutil


#initialisation variables
DATETIME = time.strftime('%Y%d%m-%H%M%S')
DATEJOUR =  time.strftime('%Y%d%m')
BACKUP_PATH = '/home/backup/'
WEB_PATH = '/var/www/html/wordpress'
SQL_PATH = '/var/lib/mysql'
DB_HOST = 'localhost'
DB_USER = 'root'
DB_USER_PASSWORD = 'Admin-pwd'
DB_NAME = 'wordpress_db'
FTP_IP_SRV='192.168.134.133'
FTP_PORT='21'
FTP_USER='sauvegarde'
FTP_PASS='Admin-sav'
FILE_SAV_DUMPSQL =  DATETIME + "-dumpsql.tar.bz2"
FILE_SAV_WORDPRESS =  DATETIME + "-wordpress.tar.bz2"
FILE_SAV_MYSQL =  DATETIME + "-mysql.tar.bz2"
FILE_SAV_LAN = DATETIME + "-conf-lan.tar.bz2"
FILE_SAV_APACHE_DEFAULT = DATETIME + "-apache-default.tar.bz2"
FILE_LOG = DATEJOUR + "-log"

#fonction list des fichiers du dossier backup
def listdirectory(path):
    fichier=[]
    l = glob.glob(BACKUP_PATH+'*')
    for i in l:
        if os.path.isdir(i): fichier.extend(listdirectory(i))
        else: fichier.append(i)
    return fichier

#fichier pour le log du jour
try:
    f = open(BACKUP_PATH+FILE_LOG)
    # est ce que fichier log du jour existe
except IOError:
     f = open(BACKUP_PATH+FILE_LOG,"w+") #existe pas on le crée
     f.write("Subject: SAUVEGARDE COMPLETE DU ...") #subjetc: pour l'objet du mail
     f.write(DATETIME) #ecriture de jour et heure
     f.write("--------------------------\n")
finally:
    f.close() #on ferme le fichier

#*****début processus sauvegarde COMPLETE*****
print "dossier de sauvegarde", BACKUP_PATH
os.path.exists(BACKUP_PATH) #vérifier si dossier pour la sauvegarde existe return True or False
if os.path.exists(BACKUP_PATH) == True:
	print("dossier existe")
else:
	os.mkdir(BACKUP_PATH) #créer le dossier pour la sauvegarde
	print("dossier existait pas, il a été créée")

print ("sauvegarde du dossier site wordpress")
print "fichier: ", FILE_SAV_WORDPRESS
print "dans: ", BACKUP_PATH
try:
	subprocess.call(['tar', '-cjf', BACKUP_PATH + FILE_SAV_WORDPRESS, WEB_PATH])
except:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecrire dans log heure et date
		f.write("  ERREUR sur la sauvegarde LOCALE de wordpress\n") #ecriture erreur dans log
	print ("erreur rencontrée sauvegarde du dossier wordpress")
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture de jour et heure
        	f.write("  sauvegarde locale wordpress réalisée\n") #ecriture sauvegarde faite dans log
	print ('sauvegarde dossier wordpress faite')

print ("sauvegarde du dossier Mysql")
print "fichier: ", FILE_SAV_MYSQL
print "dans: ", BACKUP_PATH
try:
	subprocess.call(['tar', '-cjf', BACKUP_PATH + FILE_SAV_MYSQL, SQL_PATH])
except:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecrire dans log heure et date
		f.write("   ERREUR sur la sauvegarde LOCALE du dossier Mysql\n") #ecriture erreur dans log
	print ("erreur rencontrée sur sauvegarde locale du dossier Mysql")
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture de jour et heure
        	f.write("  sauvegarde locale du dossier Mysql réalisée\n") #ecriture sauvegarde faite dans log
	print ('sauvegarde dossier Mysql faite')

print ("Dump et sauvegarde Wordpress_db Mysql")
print "fichier: ", FILE_SAV_DUMPSQL
print "dans: ", BACKUP_PATH
try:
	dumpcmd = "mysqldump -h %s -u %s -p%s %s > %s/%s.sql" % (DB_HOST,DB_USER,DB_USER_PASSWORD,DB_NAME,BACKUP_PATH,DB_NAME,)
	os.system(dumpcmd)
	subprocess.call(['tar', '-cjf', BACKUP_PATH + FILE_SAV_DUMPSQL, BACKUP_PATH + DB_NAME + ".sql"])
	os.remove (BACKUP_PATH + DB_NAME + ".sql") #on garde le fichier compressé et on efface le non compressé
except:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecrire dans log heure et date
		f.write("   ERREUR sur la sauvegarde LOCALE du dump wordpress_db\n") #ecriture erreur dans log
	print ("erreur rencontrée sur dump sql wordpress_db")
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture de jour et heure
        	f.write("  sauvegarde locale du dump wordpress_db réalisée\n") #ecriture sauvegarde faite dans log
	print ('sauvegarde dump  wordpress_db faite')

#sauvegarde de quelques fichiers supplémentaires
#--1ER--sauvegarde config resolv.conf interfaces hosts hostname
print ("sauvegarde des fichiers resolv.conf interfaces hosts hostname")
print "fichier:  ", FILE_SAV_LAN 
print "dans: ", BACKUP_PATH
try:
	filePath = shutil.copy('/etc/hostname', BACKUP_PATH)
	filePath = shutil.copy('/etc/hosts', BACKUP_PATH)
	filePath = shutil.copy('/etc/resolv.conf', BACKUP_PATH)
	filePath = shutil.copy('/etc/network/interfaces', BACKUP_PATH)
        subprocess.call(['tar', '-cjf', BACKUP_PATH + FILE_SAV_LAN, BACKUP_PATH + 'hostname', BACKUP_PATH + 'hosts', BACKUP_PATH + 'resolv.conf', BACKUP_PATH + 'interfaces'])
	os.remove (BACKUP_PATH+"hostname") #on garde le fichier compressé et on efface le non compressé
	os.remove (BACKUP_PATH+"hosts") #on garde le fichier compressé et on efface le non compressé
	os.remove (BACKUP_PATH+"resolv.conf") #on garde le fichier compressé et on efface le non compressé
	os.remove (BACKUP_PATH+"interfaces") #on garde le fichier compressé et on efface le non compressé
except:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecrire dans log heure et date
                f.write("   ERREUR sur la sauvegarde LOCALE fichiers conf lan\n") #ecriture erreur dans log
        print ("erreur rencontrée sur sauvegarde fichiers conf lan")
else:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecriture de jour et heure
                f.write("  sauvegarde locale fichiers conf lan réalisée\n") #ecriture sauvegarde faite dans log
        print ('sauvegarde fichiers conf lan faite')
#--2EME--sauvegarde 000-default.conf apache
print ("sauvegarde de 000-default.conf apache")
print "fichier:  ", FILE_SAV_APACHE_DEFAULT
print "dans: ", BACKUP_PATH
try:
        filePath = shutil.copy('/etc/apache2/sites-available/000-default.conf', BACKUP_PATH)
        subprocess.call(['tar', '-cjf', BACKUP_PATH + FILE_SAV_APACHE_DEFAULT, BACKUP_PATH + '000-default.conf'])
        os.remove (BACKUP_PATH+"000-default.conf") #on garde le fichier compressé et on efface le non compressé
except:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecrire dans log heure et date
                f.write("   ERREUR sur la sauvegarde LOCALE fichiers 000-default.conf\n") #ecriture erreur dans log
        print ("erreur rencontrée sur sauvegarde 000-default.conf")
else:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecriture de jour et heure
                f.write("  sauvegarde locale fichiers 000-default.conf réalisée\n") #ecriture sauvegarde faite dans log
        print ('sauvegarde fichiers 000-default.conf faite')

#fin sauvegarde écriture de fin dans log
with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
	f.write("FIN DE LA SAUVEGARDE LOCALE DU ...") #ecriture fin de sauvegarde
	f.write(DATETIME) #ecriture de jour et heure
	f.write("--------------------------\n")

#suppression des sauvegardes en local de plus de 2mn changer 120 pour 5 jours eb 432000
print ("suppression anciens des fichiers en local de plus de 2mn = 120s et 5 jours = 432000 s")
deux_minutes_ago = time.time() - 120
os.chdir(BACKUP_PATH)
for somefile in os.listdir('.'):
    mtime=os.path.getmtime(somefile)
    if mtime < deux_minutes_ago:
        os.unlink(somefile)
print ("nettoyage effectué")

#affiche la liste des fichiers sauvegardés en local actuellement
print ("****************************************")
print ("****************************************")
print ("liste des fichiers sauvegardés en local")
print listdirectory(BACKUP_PATH)
print ("*****************************************")
print ("*****************************************")

#transfert vers serveur ftp des sauvegardes
with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
     f.write("-------------------------------\n")
     f.write("le...")
     f.write(DATETIME) #ecriture de jour et heure
     f.write("  TRANSFERT FTP\n") #ecriture sauvegarde faite dans log

print ("transfert ftp")
#transfert sauvegarde dossier wordpress 
try:
	ftp = ftplib.FTP(FTP_IP_SRV)
	ftp.connect(FTP_IP_SRV, FTP_PORT)
	ftp.login(user = FTP_USER, passwd = FTP_PASS)
	ftp.storbinary("STOR " + FILE_SAV_WORDPRESS, open(FILE_SAV_WORDPRESS, 'rb'))
except:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecrire dans log heure et date
                f.write("   ERREUR sur TRANSFERT FTP sauvegarde du dossier Wordpress\n") #ecriture erreur dans log
        print ("erreur rencontrée")
else:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecriture de jour et heure
                f.write("  transfert vers ftp sauvegarde du dossier wordpress réalisé\n") #ecriture sauvegarde faite dans log
        print ('transfert sauvegarde dossier wordpress par ftp fait')

#transfert sauvegarde dossier mysql
try:
        ftp = ftplib.FTP(FTP_IP_SRV)
        ftp.connect(FTP_IP_SRV, FTP_PORT)
        ftp.login(user = FTP_USER, passwd = FTP_PASS)
        ftp.storbinary("STOR " + FILE_SAV_MYSQL, open(FILE_SAV_MYSQL, 'rb'))
except:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecrire dans log heure et date
                f.write("   ERREUR sur TRANSFERT FTP sauvegarde du dossier Mysql\n") #ecriture erreur dans log
        print ("erreur rencontrée")
else:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecriture de jour et heure
                f.write("  transfert vers ftp sauvegarde du dossier Mysql réalisé\n") #ecriture sauvegarde faite dans le log
        print ('transfert sauvegarde dossier Mysql par ftp fait')

#transfert sauvegarde dump db wordpress
try:
        ftp = ftplib.FTP(FTP_IP_SRV)
        ftp.connect(FTP_IP_SRV, FTP_PORT)
        ftp.login(user = FTP_USER, passwd = FTP_PASS)
        ftp.storbinary("STOR " + FILE_SAV_DUMPSQL, open(FILE_SAV_DUMPSQL, 'rb'))
except:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecrire dans log heure et date
                f.write("   ERREUR sur TRANSFERT FTP sauvegarde dump db wordpress\n") #ecriture erreur dans log
        print ("erreur rencontrée")
else:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecriture de jour et heure
                f.write("  transfert vers ftp sauvegarde dump db wordpress réalisé\n") #ecriture sauvegarde faite dans le log
        print ('transfert sauvegarde dump db wordpress par ftp fait')

#transfert fichiers conf lan
try:
        ftp = ftplib.FTP(FTP_IP_SRV)
        ftp.connect(FTP_IP_SRV, FTP_PORT)
        ftp.login(user = FTP_USER, passwd = FTP_PASS)
        ftp.storbinary("STOR " + FILE_SAV_LAN, open(FILE_SAV_LAN, 'rb'))
except:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecrire dans log heure et date
                f.write("   ERREUR sur TRANSFERT FTP sauvegarde conf lan\n") #ecriture erreur dans log
        print ("erreur rencontrée")
else:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecriture de jour et heure
                f.write("  transfert vers ftp sauvegarde conf lan réalisée\n") #ecriture sauvegarde faite dans le log
        print ('transfert sauvegarde conf lan par ftp faite')

#transfert fichiers default apache
try:
        ftp = ftplib.FTP(FTP_IP_SRV)
        ftp.connect(FTP_IP_SRV, FTP_PORT)
        ftp.login(user = FTP_USER, passwd = FTP_PASS)
        ftp.storbinary("STOR " + FILE_SAV_APACHE_DEFAULT, open(FILE_SAV_APACHE_DEFAULT, 'rb'))
except:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecrire dans log heure et date
                f.write("   ERREUR sur TRANSFERT FTP sauvegarde 000-default.conf\n") #ecriture erreur dans log
        print ("erreur rencontrée")
else:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecriture de jour et heure
                f.write("  transfert vers ftp sauvegarde 000-default.conf réalisée\n") #ecriture sauvegarde faite dans le log
        print ('transfert sauvegarde 000-default.conf par ftp fait')

#transfert du log
try:
        ftp = ftplib.FTP(FTP_IP_SRV)
        ftp.connect(FTP_IP_SRV, FTP_PORT)
        ftp.login(user = FTP_USER, passwd = FTP_PASS)
        ftp.storbinary("STOR " + FILE_LOG, open(FILE_LOG, 'rb'))
except:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecrire dans log heure et date
                f.write("   ERREUR sur TRANSFERT FTP du fichier LOG\n") #ecriture erreur dans log
        print ("erreur rencontrée")
else:
        with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
                f.write("le...")
                f.write(DATETIME) #ecriture de jour et heure
                f.write("  transfert vers ftp du fichier LOG réalisé\n") #ecriture sauvegarde faite dans le log
        print ('transfert du LOG V1 de la sauvegarde wordpress par ftp fait')

with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
     f.write("-------------------------------\n")
     f.write("le...")
     f.write(DATETIME) #ecriture de jour et heure
     f.write(" FIN TRANSFERT FTP\n") #ecriture sauvegarde faite dans log

#transfert dernière ecriture du log
try:
	ftp = ftplib.FTP(FTP_IP_SRV)
	ftp.connect(FTP_IP_SRV, FTP_PORT)
	ftp.login(user = FTP_USER, passwd = FTP_PASS)
	ftp.storbinary("STOR " + FILE_LOG, open(FILE_LOG, 'rb'))
	print ("transfert ftp LOG final et autres fichiers de sauvegardes finis")
except:
	print ("erreur fermeture log")
else:
	print ("fermeture log ok")

#envoi par mail du rapport (fichier log)
try:
	filePath = shutil.copy(FILE_LOG, 'LOG') #fichier log qui sera envoyé par mail
	#filePath = shutil.copy('/etc/apache2/sites-available/000-default.conf', BACKUP_PATH)
	subprocess.call('/home/superadmin/script/maillog.sh')
except:
	print ("erreur envoie mail log")
else:
    	print ("fin envoie mail log")

#FIN
print ("ensemble des sauvegardes terminées")
print ("sauvegarde finie")

