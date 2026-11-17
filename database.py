import sqlite3

def conectar_banco():
    conexao = sqlite3.connect("biblioteca.db")
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS autores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nacionalidade TEXT            
        )
    """)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,            
        ano INTEGER,            
        autorid INTEGER,
        FOREIGN KEY (autorid)
            REFERENCES autores(id)            
        )
    """)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,            
        email TEXT NOT NULL,            
        senha TEXT NOT NULL,
        perfil TEXT DEFAULT 'usuario'            
        )
    """)

    conexao.commit()
    conexao.close()

    print("Banco de Dados conectado e tabelas criadas")

if __name__ == "__main__":
    criar_tabelas()