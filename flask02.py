# -*- coding: utf-8 -*-

# Importa bibliotecas.
from flask import Flask, jsonify, request, abort, make_response, json, Response
import sqlite3

# Cria aplicativo Flask.
app = Flask(__name__)

# Configura o character set das transações HTTP para UTF-8.
json.provider.DefaultJSONProvider.ensure_ascii = False

# Especifica a base de dados SQLite3.
database = "./temp_db.db"


def prefix_remove(prefix, data):

    # Função que remove os prefixos dos nomes dos campos de um 'dict'.
    # Por exemplo, prefix_remove('owner_', { 'owner_id': 2, 'owner_name': 'Coisa', 'owner_status': 'on' })
    # retorna { 'id': 2, 'name': 'Coisa', 'status': 'on' }
    # Créditos: Comunidade StackOverflow.

    new_data = {}
    for key, value in data.items():
        if key.startswith(prefix):
            new_key = key[len(prefix):]
            new_data[new_key] = value
        else:
            new_data[key] = value
    return new_data


@app.route("/owner", methods=["GET"])
def get_all():

    # Obtém todos os registros válidos de 'owner'.
    # Request method → GET
    # Request endpoint → /owners
    # Response → JSON

    try:

        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)

        # Formata os dados retornados na factory como SQLite.Row.
        conn.row_factory = sqlite3.Row

        # Cria um cursor de dados.
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute(
            "SELECT * FROM owner WHERE owner_status = 'on' ORDER BY owner_name")

        # Retorna todos os resultados da consulta para 'owner_rows'.
        owners_rows = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        conn.close()

        # Cria uma lista para armazenar os registros.
        owners = []

        # Converte cada SQLite.Row em um dicionário e adiciona à lista 'registros'.
        for owner in owners_rows:
            owners.append(dict(owner))

        # Verifica se há registros antes de retornar...
        if owners:

            # Remove prefixos dos campos.
            new_owners = [prefix_remove('owner_', owner) for owner in owners]

            # Se houver registros, retorna tudo.
            return new_owners, 200
        else:
            # Se não houver registros, retorna erro.
            return {"error": "Nenhum owner encontrado"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/owner/<int:id>", methods=["GET"])
def get_one(id):

    # Obtém um registro único de 'owner', identificado pelo 'id'.
    # Request method → GET
    # Request endpoint → /owners/<id>
    # Response → JSON

    try:
        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa o SQL.
        cursor.execute(
            "SELECT * FROM owner WHERE owner_id = ? AND owner_status = 'on'", (id,))

        # Retorna o resultado da consulta para 'owner_row'.
        owner_row = cursor.fetchone()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Se o registro existe...
        if owner_row:

            # Converte SQLite.Row para dicionário e armazena em 'owner'.
            owner = dict(owner_row)

            # Remove prefixos dos campos.
            new_owner = prefix_remove('owner_', owner)

            # Retorna owner.
            return new_owner, 200
        else:
            # Se não encontrar o registro, retorna erro.
            return {"error": "Owner não encontrado"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route('/owner', methods=["POST"])
def create():

    # Cadastra um novo registro em 'owner'.
    # Request method → POST
    # Request endpoint → /owners
    # Request body → JSON (raw) → { String:name, String:description, String:location, int:owner }
    # Response → JSON → { "success": "Registro criado com sucesso", "id": id do novo registro }}

    try:
        # Recebe dados do body da requisição na forma de 'dict'.
        new_owner = request.get_json()

        # Conecta ao banco de dados.
        # Observe que 'row_factory' é desnecessário porque não receberemos dados do banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Query que insere um novo registro na tabela 'owner'.
        sql = "INSERT INTO owner (owner_name, owner_email, owner_password, owner_birth) VALUES (?, ?, ?, ?)"

        # Dados a serem inseridos, obtidos do request.
        sql_data = (
            new_owner['name'],
            new_owner['email'],
            new_owner['password'],
            new_owner['birth'],
        )

        # Executa a query, fazendo as devidas substituições dos curingas (?) pelos dados (sql_data).
        cursor.execute(sql, sql_data)

        # Obter o ID da última inserção
        inserted_id = int(cursor.lastrowid)

        # Salvar as alterações no banco de dados.
        conn.commit()

        # Fecha a conexão com o banco de dados.
        conn.close()

        # Retorna com mensagem de sucesso e status HTTP "201 Created".
        return {"success": "Registro criado com sucesso", "id": inserted_id}, 201

    except json.JSONDecodeError as e:  # Erro ao obter dados do JSON.
        return {"error": f"Erro ao decodificar JSON: {str(e)}"}, 500

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/owner/<int:id>", methods=["DELETE"])
def delete(id):

    # Marca, como apagado, um registro único de 'owner', identificado pelo 'id'.
    # Request method → DELETE
    # Request endpoint → /owners/<id>
    # Response → JSON → { "success": "Registro apagado com sucesso", "id": id do registro }

    try:

        # Conecta ao banco de dados.
        # Observe que 'row_factory' é desnecessário porque não receberemos dados do banco de dados.
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Query que pesquisa a existência do registro.
        sql = "SELECT owner_id FROM owner WHERE owner_id = ? AND owner_status != 'off'"

        # Executa a query.
        cursor.execute(sql, (id,))

        # Retorna o resultado da consulta para 'owner_row'.
        owner_row = cursor.fetchone()

        # Se o registro exite e está ativo...
        if owner_row:

            # Query para atualizar o owner no banco de dados.
            sql = "UPDATE owner SET owner_status = 'off' WHERE owner_id = ?"

            # Executa a query.
            cursor.execute(sql, (id,))

            # Salvar no banco de dados.
            conn.commit()

            # Fecha o banco de dados.
            conn.close()

            # Retorna com mensagem de sucesso e status HTTP "200 Ok".
            return {"success": "Registro apagado com sucesso", "id": id}, 200

        # Se o registro não existe, não pode ser apagado.
        else:

            # Fecha o banco de dados.
            conn.close()

            # Retorna mensagem de erro 404.
            return {"error": "Owner não existe"}, 404

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


@app.route("/owner/<int:id>", methods=["PUT", "PATCH"])
def edit(id):

    # Edita um registro em 'owner', identificado pelo 'id'.
    # Request method → PUT ou PATCH
    # Request endpoint → /owners/<id>
    # Request body → JSON (raw) → { String:name, String:description, String:location, int:owner }
    #       OBS: usando "PATCH", não é necessário enviar todos os campos, apenas os que serão alterados.
    # Response → JSON → { "success": "Registro atualizado com sucesso", "id": id do registro }

    try:

        # Recebe os dados do corpo da requisição.
        owner_json = request.get_json()

        # Conecta ao banco de dados.
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Loop para atualizar os campos específicos do registro na tabela 'owner'.
        # Observe que o prefixo 'owner_' é adicionado ao(s) nome(s) do(s) campo(s).
        set_clause = ', '.join([f"owner_{key} = ?" for key in owner_json.keys()])

        # Monta SQL com base nos campos a serem atualizados.
        sql = f"UPDATE owner SET {set_clause} WHERE owner_id = ? AND owner_status = 'on'"
        cursor.execute(sql, (*owner_json.values(), id))

        # Commit para salvar as alterações.
        conn.commit()

        # Fechar a conexão com o banco de dados.
        conn.close()

        # Confirma a atualização.
        return {"success": "Registro atualizado com sucesso", "id": id}, 201

    except sqlite3.Error as e:  # Erro ao processar banco de dados.
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  # Outros erros.
        return {"error": f"Erro inesperado: {str(e)}"}, 500


# Desafio 1.
@app.route("/owner/<int:id>/items", methods=["GET"])
def get_items_by_owner(id):

    try:
      
        conn = sqlite3.connect(database) 
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM item WHERE item_owner = ? AND item_status = 'on'", (id,))

        items_rows = cursor.fetchall()

        conn.close()

        if items_rows:
            items = [dict(item) for item in items_rows]

            new_items = [prefix_remove('item_', item) for item in items]

            return new_items, 200
        else:
            return {"error": "Nenhum item encontrado para este proprietário"}, 404

    except sqlite3.Error as e:  
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  
        return {"error": f"Erro inesperado: {str(e)}"}, 500

# Desafio 2.
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item_with_owner(item_id):


    try:
        
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM item WHERE item_id = ? AND item_status = 'on'", (item_id,))
        
        item_row = cursor.fetchone()

        if item_row:
            item = dict(item_row)
            
            owner_id = item['item_owner']

            cursor.execute(
                "SELECT * FROM owner WHERE owner_id = ? AND owner_status = 'on'", (owner_id,))
            
            owner_row = cursor.fetchone()

            if owner_row:
                owner = dict(owner_row)

                new_item = prefix_remove('item_', item)
                new_owner = prefix_remove('owner_', owner)

                new_item['owner'] = new_owner

                return new_item, 200
            else:
                return {"error": "Proprietário do item não encontrado"}, 404
        else:
            return {"error": "Item não encontrado"}, 404

    except sqlite3.Error as e:  
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:  
        return {"error": f"Erro inesperado: {str(e)}"}, 500
    
    
# Desafio 3

@app.route("/item/search/<string:item_name>", methods=["GET"])
def search_items(item_name):
    try:
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Utiliza a consulta SQL com pesquisa no campo 'item_name' e status válido
        cursor.execute(
            "SELECT*FROM item WHERE item_status != 'off' AND item_name LIKE '%'||?||'%' OR item_description LIKE '%'||?||'%' OR item_location LIKE '%'||?||'%'",
            (item_name, item_name, item_name)
        )

        items_rows = cursor.fetchall()
        conn.close()

        if items_rows:
            items = [dict(item) for item in items_rows]
            new_items = [prefix_remove('item_', item) for item in items]
            return new_items, 200
        else:
            return {"error": "Nenhum item encontrado com o nome especificado"}, 404

    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500


# Desafio 3

@app.route("/item/search/<string:item_name>", methods=["GET"])
def search_items(item_name):
    try:
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Utiliza a consulta SQL com pesquisa no campo 'item_name' e status válido
        cursor.execute(
            "SELECT*FROM item WHERE item_status != 'off' AND item_name LIKE '%'||?||'%' OR item_description LIKE '%'||?||'%' OR item_location LIKE '%'||?||'%'",
            (item_name, item_name, item_name)
        )

        items_rows = cursor.fetchall()
        conn.close()

        if items_rows:
            items = [dict(item) for item in items_rows]
            new_items = [prefix_remove('item_', item) for item in items]
            return new_items, 200
        else:
            return {"error": "Nenhum item encontrado com o nome especificado"}, 404

    except sqlite3.Error as e:
        return {"error": f"Erro ao acessar o banco de dados: {str(e)}"}, 500

    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}, 500


if __name__ == "__main__":
    app.run(debug=True)
