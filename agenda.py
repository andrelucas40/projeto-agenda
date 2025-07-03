import sqlite3

def criar_conexao():
    """Cria e retorna uma conexão com o banco de dados 'agenda.db'."""
    return sqlite3.connect("agenda.db")

def criar_tabela():
    """Cria a tabela 'contatos' no banco de dados, incluindo os novos campos."""
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            endereco TEXT,  -- Novo campo
            cpf TEXT UNIQUE -- Novo campo, com restrição UNIQUE
        )
    """)
    conexao.commit()
    conexao.close()
    print("Tabela 'contatos' verificada/criada com sucesso.")

def adicionar_contato(nome, telefone, endereco, cpf):
    """Adiciona um novo contato com nome, telefone, endereço e CPF."""
    conexao = criar_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("INSERT INTO contatos (nome, telefone, endereco, cpf) VALUES (?, ?, ?, ?)",
                       (nome, telefone, endereco, cpf))
        conexao.commit()
        print("Contato adicionado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: CPF já existe. Cada CPF deve ser único.")
    except Exception as e:
        print(f"Ocorreu um erro ao adicionar o contato: {e}")
    finally:
        conexao.close()

def listar_contatos():
    """Lista todos os contatos com todos os seus dados."""
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM contatos")
    contatos = cursor.fetchall()
    if contatos:
        print("\n--- Lista de Contatos ---")
        for contato in contatos:
            print(f"ID: {contato[0]}, Nome: {contato[1]}, Telefone: {contato[2]}, "
                  f"Endereço: {contato[3] if contato[3] else 'Não informado'}, " # Trata caso seja NULL
                  f"CPF: {contato[4] if contato[4] else 'Não informado'}") # Trata caso seja NULL
        print("------------------------")
    else:
        print("Nenhum contato encontrado.")
    conexao.close()

def buscar_contato_por_nome(nome):
    """Busca contatos pelo nome e exibe todos os seus dados."""
    conexao = criar_conexao()
    cursor = conexao.cursor()
    # Usamos LIKE para busca parcial e % para curinga
    cursor.execute("SELECT * FROM contatos WHERE nome LIKE ?", (f'%{nome}%',))
    resultados = cursor.fetchall() # Pode haver mais de um contato com o mesmo nome
    if resultados:
        print(f"\n--- Resultados da busca por '{nome}' ---")
        for resultado in resultados:
            print(f"ID: {resultado[0]}, Nome: {resultado[1]}, Telefone: {resultado[2]}, "
                  f"Endereço: {resultado[3] if resultado[3] else 'Não informado'}, "
                  f"CPF: {resultado[4] if resultado[4] else 'Não informado'}")
        print("---------------------------------------")
    else:
        print(f"Nenhum contato encontrado com o nome '{nome}'.")
    conexao.close()

def remover_contato_por_id(contato_id):
    """Remove um contato pelo ID."""
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM contatos WHERE id = ?", (contato_id,))
    conexao.commit()
    # Verifica se alguma linha foi afetada para confirmar a remoção
    if cursor.rowcount > 0:
        print("Contato removido com sucesso.")
    else:
        print(f"Nenhum contato encontrado com o ID {contato_id}.")
    conexao.close()

def menu():
    """Exibe o menu da agenda e processa as opções do usuário."""
    criar_tabela() # Garante que a tabela com os novos campos existe
    while True:
        print("\n--- Menu da Agenda ---")
        print("1 - Adicionar contato")
        print("2 - Listar contatos")
        print("3 - Buscar contato por nome")
        print("4 - Remover contato por ID")
        print("5 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            endereco = input("Endereço (opcional): ")
            cpf = input("CPF (opcional, mas único): ")
            adicionar_contato(nome, telefone, endereco, cpf)
        elif opcao == "2":
            listar_contatos()
        elif opcao == "3":
            nome = input("Nome para buscar: ")
            buscar_contato_por_nome(nome)
        elif opcao == "4":
            try:
                contato_id = int(input("ID do contato a remover: "))
                remover_contato_por_id(contato_id)
            except ValueError:
                print("ID inválido. Por favor, digite um número inteiro.")
        elif opcao == "5":
            print("Saindo da agenda. Até mais!")
            break
        else:
            print("Opção inválida! Por favor, escolha uma opção de 1 a 5.")

if __name__ == "__main__":
    menu()