####################################
# Jérôme ROUGET & Yoann BAUMERT    #
# 17/02/2017                       #
# Projet Python                    #
####################################

# Import

import sqlite3
import re
import csv
import random

# Fonctions

def mot_de_passe():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-_*/~$%&.:?!"
    MDP = ""

    for i in range(12):
        MDP = MDP + alphabet[random.randint(0, len(alphabet) - 1)]
    return MDP
    

# Utilisation des fichiers

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
    MOBILE INT
)
""")


# Lecture et parsing

with open ("personnels.csv",newline="\n") as csvfile:
    reader=csv.reader(csvfile,delimiter=',',quotechar='"')
    lecteur=csv.DictReader(csvfile)

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
        
        connexion.execute("SELECT IDENTIFIANT FROM Personnels WHERE IDENTIFIANT=:csv_identifiant_lower", {"csv_identifiant_lower":csv_identifiant_lower})
        data=connexion.fetchone()
        #print(data)
        if data is None:
            connexion.execute('INSERT INTO Personnels(NOM,JEUNEFILLE,PRENOM,IDENTIFIANT,PASSWORD,NAISSANCE,FONCTION,DEPARTEMENT,COURRIEL,TEL,MOBILE) VALUES("'+csv_nom+'","'+csv_jeune_fille+'","'+csv_prenom+'","'+csv_identifiant_lower+'","'+csv_password+'","'+csv_birthday+'","'+csv_fonction+'","'+csv_departement+'","'+csv_courriel+'","'+csv_tel+'","'+csv_mobile+'")')
            print("L'utilisateur %s a été créé."%csv_identifiant_lower)
        else:
            connexion.execute('UPDATE Personnels SET NOM="'+csv_nom+'", JEUNEFILLE="'+csv_jeune_fille+'", PRENOM="'+csv_prenom+'", IDENTIFIANT="'+csv_identifiant_lower+'", NAISSANCE="'+csv_birthday+'", FONCTION="'+csv_fonction+'", DEPARTEMENT="'+csv_departement+'", COURRIEL="'+csv_courriel+'", TEL="'+csv_tel+'", MOBILE="'+csv_mobile+'" WHERE IDENTIFIANT="'+csv_identifiant_lower+'"')
            print("L'utilisateur %s a été mis à jour."%csv_identifiant_lower)

            
                
# TEST SELECT

##connexion.execute("SELECT * FROM Personnels")
##data=connexion.fetchall()
##print(data)

# input("\nAppuyez sur ENTREE pour fermer...") # Permet de ne pas fermer la console automatiquement

BDD.commit()
