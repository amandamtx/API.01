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

# Função que lista todos os itens da coleção.
def get_all():
    # Converte o dicionário 'items' para json e armazena em 'var_json'.
    return json.dumps(items, indent=2)
    
# Função que lê um item específico, identificado pelo índice.
def get_one(id):
    
    for item in items:
        if item.get("id") == id:
            return json.dumps(item, indent=2)

 
#Chama a função get_all(). 
#print(get_all())

# Chama a função get_one(), passando a índice como parâmetro.
print(get_one(4))