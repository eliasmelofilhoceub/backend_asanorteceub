from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def conectar_banco():
    conexao = sqlite3.connect("biblioteca2_0.db")
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS autores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nacionalidade TEXT NOT NULL            
        )
    """)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,            
        ano TEXT NOT NULL,            
        autorid INTEGER NOT NULL,
        FOREIGN KEY (autorid)
            REFERENCES autores(id)            
        )
    """)

    conexao.commit()
    conexao.close()

@app.route("/", methods=["GET"])
def inicio():

    return jsonify({
        "Informações": "API Geral de Livros",
        "Versao": "2.0"
    })

#autores

@app.route("/autores", methods=["POST"])
def cadastrar_autor():

    dados = request.get_json()

    if not dados:
        return jsonify({
            "Aviso": "JSON não digitado"
        }), 400

    if "nome" not in dados:
        return jsonify({
            "Aviso": "Nome é obrigatorio"
        }), 400
    
    if "nacionalidade" not in dados:
        return jsonify({
            "Aviso": "Nacionalidade é obrigatorio"
        }), 400
    
    if dados["nome"].strip() == "":
        return jsonify({
            "Aviso": "O nome está vazio"
        }), 400
    
    nome = dados["nome"]
    nacionalidade = dados["nacionalidade"]

    conexao = conectar_banco()

    cursor = conexao.execute("""
        INSERT INTO autores
        (nome, nacionalidade)
        VALUES (?, ?)
    """,
        (nome, nacionalidade)
    )

    conexao.commit()
    idautor = cursor.lastrowid
    conexao.close()

    return jsonify({
        "Aviso": "Autor cadastrado com sucesso!!!",
        "Autor": {
            "id": idautor,
            "nome": nome,
            "nacionalidade": nacionalidade
        }
    }), 201

@app.route("/autores", methods=["GET"])
def listarautores():

    conexao = conectar_banco()

    autores = conexao.execute(
        """
        SELECT *
        FROM autores
        ORDER BY id
        """
    ).fetchall()

    conexao.close()

    return jsonify([
        dict(autor)
        for autor in autores
    ])

@app.route("/autores/<int:id>", methods=["GET"])
def buscarautor(id):

    conexao = conectar_banco()

    autor = conexao.execute(
        """
        SELECT *
        FROM autores
        WHERE id = ?
        """, (id,)
    ).fetchone()

    conexao.close()

    if autor is None:

        return jsonify({
        "Aviso": "Autor nao encontrado!!!"
    })
    
    return jsonify(dict(autor))

@app.route("/autores/<int:id>", methods=["PUT"])
def atualizarautor(id):

    dados = request.get_json()

    nome = dados["nome"]
    nacionalidade = dados["nacionalidade"]

    conexao = conectar_banco()

    resultado = conexao.execute(
        """
        UPDATE autores
        SET
        nome = ?,
        nacionalidade = ?
        WHERE id = ?
        """, (
            nome,
            nacionalidade,
            id
        ))
    
    conexao.commit()
    conexao.close()

    if resultado.rowcount == 0:

        return jsonify({
        "Aviso": "Autor nao encontrado!!!"
    }), 404

    return jsonify({
        "Aviso": "Autor aualizado com sucesso!!!"
    })

@app.route("/autores/<int:id>", methods=["DELETE"])
def excluirrautor(id):

    conexao = conectar_banco()

    resultado = conexao.execute(
        """
        DELETE FROM autores
        WHERE id = ?
        """, (id,))
    
    conexao.commit()
    conexao.close()

    if resultado.rowcount == 0:

        return jsonify({
        "Aviso": "Autor nao encontrado!!!"
    }), 404

    return jsonify({
        "Aviso": "Autor excluido com sucesso!!!"
    })

#Livros

@app.route("/livros", methods=["POST"])
def cadastrar_livro():

    dados = request.get_json()

    titulo = dados["titulo"]
    ano = dados["ano"]
    autorid = dados["autorid"]

    conexao = conectar_banco()

    autor = conexao.execute(
        """
        SELECT id
        FROM autores
        WHERE id = ?
        """, (autorid,)
    ).fetchone()

    if autor is None:

        conexao.close()

        return jsonify({
            "Aviso": "Autor nao encontrado!!!"
        }), 404

    cursor = conexao.execute(
        """
        INSERT INTO livros
        (titulo, ano, autorid)
        VALUES (?, ?, ?)
        """, (
            titulo,
            ano,
            autorid
        ))

    conexao.commit()

    idlivro = cursor.lastrowid

    conexao.close()

    return jsonify({
        "Aviso": "Livro cadastrado com sucesso!!",

        "Livro": {
            "id": idlivro,
            "titulo": titulo,
            "ano": ano,
            "autorid": autorid
        }
    }), 201

@app.route("/livros", methods=["GET"])
def listar_livros():
    
    conexao = conectar_banco()

    livros = conexao.execute(
       """
        SELECT
        livros.id,
        livros.titulo,
        livros.ano,
        autores.nome AS autor,
        autores.nacionalidade
        FROM livros
        JOIN autores
        ON livros.autorid = autores.id
        ORDER BY livros.id
        """
    ).fetchall()

    conexao.close()

    return jsonify([
        dict(livro)
        for livro in livros  
    ])

@app.route("/livros/buscarnome", methods=["GET"])
def buscarnome():
    
    titulo = request.args.get("titulo")
    conexao = conectar_banco()
    livros = conexao.execute(
       """
        SELECT
            livros.id,
            livros.titulo,
            livros.ano,
        autores.nome AS autor
        FROM livros
        JOIN autores
        ON livros.autorid = autores.id
        WHERE livros.titulo LIKE ? 
        """, (f"%{titulo}%",)).fetchall()
    conexao.close()

    return jsonify([
        dict(livro)
        for livro in livros  
    ])

@app.route("/livros/<int:id>", methods=["GET"])
def listar_livro(id):
    
    conexao = conectar_banco()

    livro = conexao.execute(
       """
        SELECT
        livros.id,
        livros.titulo,
        livros.ano,
        autores.nome AS autor,
        autores.nacionalidade
        FROM livros
        JOIN autores
        ON livros.autorid = autores.id
        WHERE livros.id = ?
        """, (id,)
    ).fetchone()

    conexao.close()

    if livro is None:
        return jsonify({
            "Aviso": "Livro nao encontrado!!!"
        }), 404
    
    return jsonify(dict(livro))

@app.route("/livros/<int:id>", methods=["PUT"])
def atualizar_livro(id):

   dados = request.get_json()

   titulo = dados["titulo"]
   ano = dados["ano"]
   autor_id = dados["autor_id"]

   conexao = conectar_banco()

   autor = conexao.execute("""
       SELECT id
       FROM autores

       WHERE id = ?
   """, (autor_id,)).fetchone()

   if autor is None:

       conexao.close()

       return jsonify({
           "erro": "Autor não encontrado!"
       }), 404

   resultado = conexao.execute("""
       UPDATE livros
       SET
           titulo = ?,
           ano = ?,
           autor_id = ?
       WHERE id = ?
   """, (
       titulo,
       ano,
       autor_id,
       id
   ))

   conexao.commit()
   conexao.close()

   if resultado.rowcount == 0:

       return jsonify({
           "Aviso": "Livro não encontrado!"
       }), 404

   return jsonify({
       "Aviso": "Livro atualizado com sucesso!"
   })


@app.route("/livros/<int:id>", methods=["DELETE"])
def excluir_livro(id):

   conexao = conectar_banco()

   resultado = conexao.execute("""
       DELETE FROM livros

       WHERE id = ?
   """, (id,))

   conexao.commit()
   conexao.close()

   if resultado.rowcount == 0:

       return jsonify({
           "Aviso": "Livro não encontrado!"
       }), 404

   return jsonify({
       "Aviso": "Livro excluído com sucesso!"
   })

@app.route("/livros/quantidade", methods=["GET"])
def quantidade():
    
    conexao = conectar_banco()

    resultado = conexao.execute("""
        SELECT COUNT(*) AS total
        FROM livros
    """).fetchone()

    conexao.close()

    return jsonify({
        "Total de Livros": resultado["total"]
    })


if __name__ == "__main__":

    criar_tabelas()

    app.run(debug=True)