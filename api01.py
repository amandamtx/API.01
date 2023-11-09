# Importa a biblioteca 'json'.
import json

items = [
    {
        "id": 1,
        "nome": "Bagulho",
        "description": "apenas um bagulho",
        "location": "em uma caixa"
    }, {
        "id": 2,
        "name": "Tranqueira",
        "description": "Apenas uma tranqueira qualquer",
        "location": "Em um gaveteiro"
     }, {
        "id": 3,
        "name": "Bagulete",
        "description": "Um bagulete qualquer",
        "location": "Na esquina"
    }
]

#def get_all():
    # Converte o dicionário 'items' para json e armazena em 'var_json'.

    # Imprime o json.
    #print(var_json)
    
    
def get_one(id):
 var_json = json.dumps(items[id], indent=2)
 print(var_json)
    
    
get_one(1)
#get_all()