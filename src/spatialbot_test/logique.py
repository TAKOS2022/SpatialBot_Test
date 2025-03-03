from sqlalchemy import create_engine
import geopandas as gpd
from sqlalchemy.sql import text
import os 
from openai import OpenAI
from pydantic import BaseModel, Field
import json 
from flask import jsonify
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def connect_to_db(db_user="justin", db_password="Jesus-2016", db_host="localhost", db_name="spatialbot_db"):
    engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}")
    return engine

def get_layers_names():
    with connect_to_db().connect() as connection:
        statement = text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE' AND table_name != 'spatial_ref_sys';")
        return connection.execute(statement).fetchall()
    
def load_selected_layer(layer_input, tables_names):
    result = []
    for item in layer_input.split(','):
        if item.strip() not in tables_names:
            raise ValueError("Le layer n'existe pas !")
        else:
            result.append(item.strip())
    return result

def test_setup_openai_1():
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
        ]
    )

    print(completion.choices[0].message.content)

class ExtractedLayer(BaseModel):
    layer_1: str
    layer_2: str

def test_structure_output_2():
    completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Extract the name of the layer."},
        {"role": "user", "content": "Calcul the spatial intersection between the buildings and pipelines layers"},
    ],
    response_format=ExtractedLayer,
    )

    event = completion.choices[0].message.parsed
    print('The layer are : ', event.layer_1," & " , event.layer_2)


def get_layer_data_base_on_name(layer_name):
    query = f"SELECT * FROM {layer_name}"
    return gpd.read_postgis(query, connect_to_db())

class LoadLayer(BaseModel):
    layers : ExtractedLayer
    operation : str

# 1. Calculate intersection between layer
def get_intersection(layer1, layer2):
    """Return the intersection between two layers"""
    result = gpd.overlay(get_layer_data_base_on_name(layer1), get_layer_data_base_on_name(layer2), how='intersection')
    print("result : ", result)
    result.to_file(r"D:\vs_code_test\spatialbot_test\data.json", driver="GeoJSON")
    # with open(r"D:\vs_code_test\spatialbot_test\data.json", "w") as json_file:
    #     json.dump(result, json_file, indent=4)
    #     print("json dumps save : ", json.dump(result, json_file, indent=4))
    # return result

    
def test_intersection():

    # We can add multiple functions inside the tools
    tools = [
        {
        "type": "function",
        "function": {
            "name": "get_intersection",
            "description": "Calcul the spatial intersection between 2 layers",
            "parameters": {
            "type": "object",
            "properties": {
                "layer1" : {"type" : "string", "description": "The first layer name"},
                "layer2" : {"type" : "string", "description": "The second layer name"}
            },
            "required": ["layer1", "layer2"], 
            "additionalProperties": False
            }, 
            "strict" : True
        }
        }
    ]

    # assistant = client.beta.assistants.create(
    #     instructions="You are a spatial bot. You will calculate spatial interaction between geospatial layer. Use the provided functions to answer questions.",
    #     model="gpt-4o-2024-08-06",
    #     tools=tools
    # )

    # thread = client.beta.threads.create()
    # message = client.beta.threads.messages.create(
    # thread_id=thread.id,
    # role="user",
    # content="What is spatial intersection between buildings_911B and pipelines_911B",
    # )


    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content" :"What is spatial intersection between vcom and Emprise" }],
        tools=tools
    )
    # print(completion.model_dump())
    print(completion.choices[0].message.tool_calls)

    for tool_call in completion.choices[0].message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        messages.append(completion.choices[0].message)

        result = call_function(name, args)
        messages.append({
            "role" : "tool", "tool_call_id":tool_call.id, "content": json.dumps(result)
        })

def call_function(name, args):
    if name == "get_intersection":
        return get_intersection(**args)
    
class IntersectionResponse(BaseModel):
    layer1: str = Field(
        description="Name of the first layer"
    )
    layer2: str = Field(
        description="Name of the second layer"
    )
    operation: str = Field(
        description="The name of the operation apply to the layers. Exemple this can be intersection, buffer etc. All operations relate to spatial interaction"
    )
    response : str = Field(
        description="A natural language response to the user's question. Example : I have complete the tasks."
    )


# A modifier ()
def send_layer_to_frond_end(layer_name):
    return jsonify(json.loads(get_layer_data_base_on_name(layer_name)))

def test_function_calling_3():
    return NotImplemented




if __name__=="__main__":
    print('Debut du programme')
    # db_user = input("Entrez le nom de l'utilisateur : ")
    # db_host = input("Entrez le host : ")
    # db_name = input("Entrez le nom de la BD : ")
    # db_password = input("Entrez le mot de passe : ")

    # engine = connect_to_db()

    # table_names = [name[0] for name in get_layers_names()]
    # print(table_names)
    # layer_input = input("Entrez les layers que vous voulez charger (separé par une virgule): ")
    # selected_layer = load_selected_layer(layer_input, table_names)
    # print("Vous avez selectionner : ", selected_layer)
    
    # ------ Integrate LLM --------
    # test_setup_openai_1()
    # test_structure_output_2()

    # print(get_layer_data_base_on_name("buildings_105"))
    # test_intersection()
    # with open(r"D:\vs_code_test\spatialbot_test\data.json", "w") as json_file:
    #     json.dump(result, json_file, indent=4)
    #     print("json dumps save : ", json.dump(result, json_file, indent=4))

    tools = [
        {
        "type": "function",
        "function": {
            "name": "get_intersection",
            "description": "Calcul the spatial intersection between 2 layers",
            "parameters": {
            "type": "object",
            "properties": {
                "layer1" : {"type" : "string", "description": "The first layer name"},
                "layer2" : {"type" : "string", "description": "The second layer name"}
            },
            "required": ["layer1", "layer2"], 
            "additionalProperties": False
            }, 
            "strict" : True
        }
        }
    ]

    system_prompt = "You are a helpful spatial analyst assistant."
    messages = [
    {"role": "system", "content": system_prompt},
   {"role": "user", "content" :"What is spatial intersection between vcom and emprise" }
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content" :"What is spatial intersection between vcom and Emprise" }],
        tools=tools
    )

    completion.model_dump()

    for tool_call in completion.choices[0].message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print(args)
        messages.append(completion.choices[0].message)

        result = call_function(name, args)
        messages.append({
            "role" : "tool", "tool_call_id":tool_call.id, "content": json.dumps(result)
        })

    completion_2 = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06", 
        messages=messages, 
        tools=tools,
        response_format=IntersectionResponse
    )

    final_response = completion_2.choices[0].message.parsed
    print(final_response.layer1)
    print(final_response.layer2)
    print(final_response.operation)
    print(final_response.response)



   