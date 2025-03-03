# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "folium",
#     "sqlalchemy",
#     "streamlit",
#     "streamlit-folium",
#     "yfinance",
# ]
# ///
import folium
from streamlit_folium import st_folium
import yfinance as yf
import streamlit as st
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging


msft = yf.Ticker("MSFT")


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
    

# 1. Fonction pour le chatbot
def chatbot(user_input):
    responses = {
        "bonjour": "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
        "carte": "Vous pouvez interagir avec la carte principale ci-dessous.",
        "aide": "Posez-moi des questions sur la carte ou sur les analyses spatiales.",
    }
    
    return responses.get(user_input.lower(), "Désolé, je n'ai pas compris votre demande.")

# 2. Créer la carte interactive avec Folium
def create_map():
    m = folium.Map(location=(48.8566, 2.3522))  # Coordonnées de Paris (exemple)
    folium.Marker([48.8566, 2.3522], popup="Paris").add_to(m)  # Ajouter un marqueur
    return m

def create_chat_message():
    st.title("Spatial Bot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # React to user input
    prompt = st.chat_input("What is up ?")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response  = f"Echo: {prompt}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    

# 3. Fonction pour afficher la sidebar et le chatbot
def sidebar():
    with st.sidebar.title("Chatbot"):
        # Afficher le chat
        create_chat_message()

    # user_input = st.sidebar.text_input("Posez une question :", "")
    # response = ""
    
    # if user_input:
    #     if "connexion" in user_input.lower():
    #         st.write("Je vais vous aider à vous connecter à la base de données.")
    #         host = st.text_input("Nom d'hôte de la base de données :")
    #         dbname = st.text_input("Nom de la base de données :")
    #         user = st.text_input("Nom d'utilisateur :")
    #         password = st.text_input("Mot de passe :", type="password")

    #         if connect_db(user, password, host, dbname):
    #             logging.log("Succes 2")

    #             response = chatbot("Successfuly connected !")
    #     st.sidebar.write(f"**Réponse du chatbot** : {response}")
    # else:
    #     st.sidebar.write("**Bienvenue dans le chatbot**. Posez-moi une question !")

# 4. Main application
def main():
    st.title("Application Streamlit avec Chatbot et Carte Interactive")
    
    # Afficher la sidebar avec le chatbot
    sidebar()
    
    # Afficher la carte interactive dans la page principale
    # st.subheader("Carte Interactive")
    # map_obj = create_map()
    # st_folium(map_obj, width=700, height=500)

# Exécution de l'application Streamlit
if __name__ == "__main__":
    main()

# Hacky stuff required to be added to make it work without `streamlit run`:
if "__streamlitmagic__" not in locals():
    import streamlit.web.bootstrap

    streamlit.web.bootstrap.run(__file__, False, [], {})
