from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def start():
    return "Primeiro Projeto"

@app.route("/curso")
def curso():
    return jsonify({
        "curso": "Engenharia de Software"
    })

@app.route("/professor")
def professor():
    return jsonify({
        "professor": "Elias"
    })

@app.route("/professor/<nome>")
def professorX(nome):
    return jsonify ({
        "nome": nome,
        "curso": "Engenharia de Software",
        "Numero": "1"
    })

if __name__ == "__main__":
    app.run(debug=True)