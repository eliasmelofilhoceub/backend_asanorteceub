from flask import Blueprint, request, jsonify
from database import conectar_banco
from werkzeug.security import generate_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/cadastro", methods=["POST"])
def cadastrarusuario():
    dados = request.get_json()
    if not dados:
        return jsonify({
            "Aviso": "Envie os dados"
        }), 400
    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome or not email or not senha:
        return jsonify({
            "Aviso": "Todos os campos obrigatórios"
        }), 400
    
    senhahash = generate_password_hash(senha)
    conexao = conectar_banco()

    conexao.execute("""
        INSERT INTO usuarios (nome, email, senha)
        VALUES (?, ?, ?)
    """, (nome, email, senhahash))

    conexao.commit()        
    conexao.close()

    return jsonify({
        "Aviso": "Usuário cadastrado com sucesso"
        }), 201            