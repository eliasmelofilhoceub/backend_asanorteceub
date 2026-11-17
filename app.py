from flask import Flask, jsonify, make_response

from routes.autores import autores_bp
from routes.livros import livros_bp
from routes.auth import auth_bp

app = Flask(__name__)

app.register_blueprint(autores_bp)
app.register_blueprint(livros_bp)
app.register_blueprint(auth_bp)

@app.errorhandler(404)
def erroderota(erro):
    return jsonify({
        "erro": True,
        "Aviso": "Rota não encontrada",
        "Status": 404
    }), 404

@app.route("/", methods=["GET"])
def inicio():

    return jsonify({
        "Informações": "API de Biblioteca",
        "Versao": "3.0"
    })

@app.route("/status", methods=["GET"])
def verificacao():
    resposta = make_response(
        jsonify({
            "Aviso": "API estável",
            "Nível": "OK"
        }), 200
    )

    resposta.headers["API"] = "Versao4.0"

    return resposta

if __name__ == "__main__":
    app.run(debug=True)