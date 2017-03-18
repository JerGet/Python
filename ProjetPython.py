#+----------------------------------+
#|   Jérôme ROUGET & Yoann BAUMERT  |
#|   17/02/2017                     |
#|   Projet Python                  |
#+----------------------------------+

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import

import sqlite3
import re
import csv
import random
import string
import time
import hashlib

# Fonctions

def mot_de_passe():
    length = 14 # longueur du mot de passe
    chars = string.ascii_letters + string.digits + '!@#$%^&*()' # caractères possibles pour le mot de passe
    hashed_pwd = hashlib.md5("".join(random.sample(chars,length)).encode('utf-8')).hexdigest() # hashage du mot de passe avec la library hashlib
    return hashed_pwd

now = time.strftime('%Y%m%d%H%M%S') # date et heure actuelle sous le format YYYYmmddHHMMSS

# Connexion à la base SQLite

BDD=sqlite3.connect('ma_base.db')

# Création de la table

connexion=BDD.cursor()

connexion.execute("""
CREATE TABLE IF NOT EXISTS Personnels(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    NOM TEXT,
    JEUNEFILLE TEXT,
    PRENOM TEXT,
    IDENTIFIANT TEXT,
    PASSWORD TEXT,
    NAISSANCE TEXT,
    FONCTION TEXT,
    DEPARTEMENT TEXT,
    COURRIEL TEXT,
    TEL INT,
    MOBILE INT,
    CHECKUPDATE INT
)
""")


# Lecture et parsing

# on ouvre le fichier csv
with open ("personnels.csv",newline="\n") as csvfile:
    reader=csv.reader(csvfile,delimiter=',',quotechar='"')
    lecteur=csv.DictReader(csvfile)

    # et on attribue chaque colonne à une variable
    for row in lecteur:
        csv_nom=row['NOM']
        csv_jeune_fille=row['NOM de jeune fille']
        csv_prenom=row['Prénom']
        csv_birthday=row['Date de naissance']
        csv_fonction=row['Fonction']
        csv_departement=row['Département']
        csv_courriel=row['Courriel']
        csv_tel=row['Téléphone']
        csv_mobile=row['Mobile']
        csv_identifiant=re.sub(" ",r"",csv_prenom[0]+csv_nom+csv_birthday[-2:])
        csv_identifiant_lower=csv_identifiant.lower()
        csv_password=mot_de_passe()
        csv_check_update=now

        # on compare les identifiants de la base de donnée avec ceux du fichier csv
        connexion.execute("SELECT IDENTIFIANT FROM Personnels WHERE IDENTIFIANT=:csv_identifiant_lower", {"csv_identifiant_lower":csv_identifiant_lower})
        data=connexion.fetchone()

        # si l'identifant n'existe pas dans la base de donnée, alors l'utilisateur est créé
        if data is None:
            connexion.execute('INSERT INTO Personnels(NOM,JEUNEFILLE,PRENOM,IDENTIFIANT,PASSWORD,NAISSANCE,FONCTION,DEPARTEMENT,COURRIEL,TEL,MOBILE,CHECKUPDATE) VALUES("'+csv_nom+'","'+csv_jeune_fille+'","'+csv_prenom+'","'+csv_identifiant_lower+'","'+csv_password+'","'+csv_birthday+'","'+csv_fonction+'","'+csv_departement+'","'+csv_courriel+'","'+csv_tel+'","'+csv_mobile+'","'+csv_check_update+'")')
            print("L'utilisateur %s a été créé."%csv_identifiant_lower)

        # et si il existe, tous les champs sont mis à jour sauf le mot de passe
        else:
            connexion.execute('UPDATE Personnels SET NOM="'+csv_nom+'", JEUNEFILLE="'+csv_jeune_fille+'", PRENOM="'+csv_prenom+'", IDENTIFIANT="'+csv_identifiant_lower+'", NAISSANCE="'+csv_birthday+'", FONCTION="'+csv_fonction+'", DEPARTEMENT="'+csv_departement+'", COURRIEL="'+csv_courriel+'", TEL="'+csv_tel+'", MOBILE="'+csv_mobile+'", CHECKUPDATE="'+csv_check_update+'" WHERE IDENTIFIANT="'+csv_identifiant_lower+'"')
            print("L'utilisateur %s a été mis à jour."%csv_identifiant_lower)


# Suppression des utilisateurs n'étant plus dans l'entreprise
# on compare si la date de 'checkupdate' avec la date actuelle (now), et si c'est différent, on supprime l'utilisateur

connexion.execute('DELETE FROM Personnels WHERE CHECKUPDATE !='+now)

# Permet de ne pas fermer la console automatiquement
input("\nAppuyez sur ENTREE pour fermer...")

BDD.commit()
