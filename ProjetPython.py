#####################################
#   Jérôme ROUGET & Yoann BAUMERT   #
#   17/02/2017                      #
#   Projet Python                   #
#####################################

# Import

import sqlite3
import csv

# Utilisation des fichiers

groupesDB=sqlite3.connect('groupes.db')
personnelsDB=sqlite3.connect('personnels.db')

# Création des tables

connect=groupesDB.cursor()
connexion=personnelsDB.cursor()

connect.execute("""
CREATE TABLE IF NOT EXISTS Groupes(
    id INTEGER PRIMARY KEY,
    DEPARTEMENT TEXT
)
""")

connexion.execute("""
CREATE TABLE IF NOT EXISTS Personnels(
    id INTEGER PRIMARY KEY,
    NOM TEXT,
    FIFILLE TEXT,
    PRENOM TEXT,
    NAISSANCE TEXT,
    FONCTION TEXT,
    DEPARTEMENT TEXT,
    COURRIEL TEXT,
    TEL INT,
    MOBILE INT,
    FOREIGN KEY(DEPARTEMENT) REFERENCES Groupes(DEPARTEMENT)
)
""")

# Lecture et parsing

with open ("personnels.csv",newline="\n") as csvfile:
    reader=csv.reader(csvfile,delimiter=',',quotechar='"')
    lecteur=csv.DictReader(csvfile)

    for row in lecteur:
        connect.execute('INSERT INTO Groupes(DEPARTEMENT) VALUES("'+row['Departement']+'")')
        connexion.execute('INSERT INTO Personnels(NOM,FIFILLE,PRENOM,NAISSANCE,FONCTION,DEPARTEMENT,COURRIEL,TEL,MOBILE) VALUES("'+row['NOM']+'","'+row['NOM de jeune fille']+'","'+row['Prenom']+'","'+row['Date de naissance']+'","'+row['Fonction']+'","'+row['Departement']+'","'+row['Courriel']+'","'+row['Telephone']+'","'+row['Mobile']+'")')

# Select

connexion.execute("SELECT NOM,DEPARTEMENT FROM Personnels")

osef=connexion.fetchall()
print(osef)

groupesDB.commit()
personnelsDB.commit()
