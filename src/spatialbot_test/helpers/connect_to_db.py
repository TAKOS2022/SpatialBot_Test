from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

# Fonction pour se connecter à la base de données avec des paramètres
def connect_db(db_user, db_password, db_host, db_name):
    try:
        # Créer la chaîne de connexion dynamique avec les paramètres passés
        connection_string = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
        
        # Créer une connexion à la base de données PostgreSQL
        engine = create_engine(connection_string, echo=True)
        
        # Créer un objet Session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        logging.log("Connexion réussie")
        print("Connexion réussie")
        
        return session  # Retourne la session pour l'utilisation

    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        logging.log(f"Erreur de connexion à la base de données : {e}")
        return None  # Retourne None si la connexion échoue

