from database import conectar_banco

conexao = conectar_banco()

autores = [
        ("Machado de Assis", "Brasileira"),
        ("Ana Furtado", "Brasileira"),
        ("MC do Poze", "Brasileira")
    ]

for nome, nacionalidade in autores:
    conexao.execute("""
        INSERT INTO autores (nome, nacionalidade)
        SELECT ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM autores WHERE nome = ?        
            )
    """, (nome, nacionalidade, nome))

conexao.commit()

livros =  [
    ("As andorinhas", 1899, "Machado de Assis"),
    ("Caverna do Dragão", 1500, "Ana Furtado"),
    ("Como sobreviver", 1200, "MC do Poze")
]

for titulo, ano, autor in livros:
    conexao.execute("""
        INSERT INTO livros (titulo, ano, autorid)
        SELECT ?, ?, id
        FROM autores
        WHERE nome = ?
        AND NOT EXISTS (
            SELECT 1 FROM livros WHERE titulo = ?        
            )
    """, (titulo, ano, autor, titulo))

conexao.commit()
conexao.close()

print("Banco de Dados aberto com sucesso!!!")
