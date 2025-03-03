from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy.exc import OperationalError
import geopandas as gpd


app = Flask(__name__)

engine = None

@app.route('/')
def load_map_page():
    return render_template('index.html')


# Fonction pour se connecter à la base de données avec des paramètres
@app.route('/connect_db', methods=['POST'])
def connect_db_route():
    data = request.get_json()
    db_user = data.get('user')
    db_password = data.get('password')
    db_host = data.get('host')
    db_name = data.get('db_name')
    try:
        # Créer la chaîne de connexion dynamique avec les paramètres passés
        connection_string = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'

        # Créer une connexion à la base de données PostgreSQL
        engine = create_engine(connection_string, echo=True)

        # Tester la connexion en exécutant une requête simple
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))  # Requête simple pour tester la connexion
            if result:
                logging.info("Connexion réussie")
                print("Connexion réussie")
                return jsonify(success=True)  # Retourne la session pour l'utilisation

    except OperationalError as e:
        logging.error(f"Erreur de connexion à la base de données: {e}")
        print(f"Erreur de connexion: {e}")
        return jsonify(success=False, error=str(e)) 
    
def connect_db():
    try:
        connection_string = "postgresql://justin:Jesus-2016@localhost/spatialbot_db"
        engine = create_engine(connection_string)
        connection = engine.connect()
        print("Database connection successful")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise



@app.route('/get_layers_name', methods=['GET'])
def get_layers_names():
   
    query = "SELECT f_table_name FROM geometry_columns WHERE f_table_schema = 'public';"
    result = gpd.read_postgis(query, connect_db())
    
    # Extract table names into a list
    layers = result['table_name'].tolist()  # `table_name` is the column name from the result
    print(layers)
    return jsonify(success=True, layers=layers)
  
   
    # try: 
    #     metadata = MetaData(bind=connect_db())
    #     metadata.reflect()
    #     layers = [layers.append(table) for table in metadata.tables]
    #     print("layers : ", layers)
    #     return jsonify(success=True, layers=layers)
    # except Exception as e:
    #     return jsonify(success=False, error=str(e))


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    # Réponse de test simple
    response_text = f"Bot : {user_message}"
    
    return jsonify({"response": response_text})


if __name__ == "__main__":
    app.run(debug=True)