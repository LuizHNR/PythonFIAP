# Atividade do momento criar uma função que mostre um
# menu de opções conforme abaixo:

# Programa Agenda de Contatos
# Menu de opções:
# 	(C)adastrar
# 	(L)er registros
# 	(R)emover
# 	(A)tualizar
# 	(S)air

# Faça um código que repita as chamadas para esta função
# Menu até que o usuário escolha a opção Sair

# Fazer o codigo da função Cadastrar, que deve pedir para o usuário digitar:
	# nome : String
	# telefone : String
	# email : String
	# nascimento : Date
# Deverá validar os dados e encaminha-los para uma função
# que salve-os no banco de dados

# Fazer o código da função que salva os dados no banco de dados

# Fazer o codigo para pesquisar contatos, e mostrar na tela todos os contatos encontrados

import os
from datetime import datetime
import oracledb


class Contato():
    """
        Classe de contato para servir como padrão para os objetos do tipo contato
    """
    nome = ""
    telefone = ""
    email = ""
    nascimento = datetime.now()


def gerar_conexao_db():
    usuario = os.environ.get("FIAP_ORACLE_USER")
    senha = os.environ.get("FIAP_ORACLE_PASS")
    db_path="oracle.fiap.com.br:1521/orcl"
    con = oracledb.connect(
        user=usuario,
        password=senha,
        dsn=db_path)
    return con


def gravar_db( contato: Contato ) -> bool:
    conexao = gerar_conexao_db()
    cursor = conexao.cursor()
    sql = """INSERT INTO agenda (nome, telefone, email, nascimento)
             VALUES (:1, :2, :3, :4)"""
    try:
        cursor.execute(sql, (contato.nome, contato.telefone, contato.email, contato.nascimento))
        conexao.commit()
    except Exception as err:
        print("Erro: ", err)
        conexao.rollback()
        return False
    conexao.close()
    return True


def gerar_tabela() -> bool:
    conexao = gerar_conexao_db()
    cursor = conexao.cursor()
    sql_drop = """DROP TABLE IF EXISTS agenda"""
    sql_drop_constraint = """DROP CONSTRAINT IF EXISTS agenda_pk"""
    sql = """
        CREATE TABLE agenda (
            nome varchar2(100),
            telefone varchar2(20),
            email varchar2(50),
            nascimento DATE,
            CONSTRAINT agenda_pk PRIMARY KEY (nome)
        )
        """
    try:
        cursor.execute(sql_drop)
        cursor.execute(sql_drop_constraint)
        cursor.execute(sql)
        conexao.commit()
    except Exception as err:
        print("Erro: ", err)
        conexao.rollback()
        return False
    conexao.close()
    return True

def ler_db( nome ):
    conexao = gerar_conexao_db()
    cursor = conexao.cursor()
    sql = """SELECT * FROM agenda WHERE nome LIKE :1"""
    cursor.execute(sql, ("%" + nome + "%", ))
    
    resultado = []
    for dados in cursor:
        resultado.append(dados)
        
    conexao.close()
    return resultado

def remover_db( nome ):
    conexao = gerar_conexao_db()
    cursor = conexao.cursor()
    sql = """DELETE FROM agenda WHERE nome = :1"""
    try: 
        cursor.execute(sql, (nome, ))
        conexao.commit()
        conexao.close()
        return True
    except Exception as err:
        conexao.rollback()
        conexao.close()
        return False
        
def atualizar_db( nome : str, contato: Contato ) -> bool:
    conexao = gerar_conexao_db()
    cursor = conexao.cursor()
    sql = """UPDATE agenda SET telefone = :1, email = :2, nascimento = :3
             WHERE nome = :4"""
    try:
        cursor.execute(sql, (contato.telefone, 
                             contato.email, 
                             contato.nascimento,
                             nome))
        conexao.commit()
    except Exception as err:
        print("Erro: ", err)
        conexao.rollback()
        return False
    conexao.close()
    return True


def ler():
    nome = input("Digite o nome que você deseja pesquisar: ")
    lista = ler_db( nome )
    
    for contato in lista:
        print(f"""
              --------Contato-----------
              Nome: {contato[0]} 
              Telefone: {contato[1]}
              Email: {contato[2]}
              Nascimento: {contato[3].strftime("%d-%B-%Y")}
              --------------------------
              """)
    

def remover():
    nome = input("Digite o nome Completo que você deseja pesquisar: ")
    remove = remover_db(nome)
    if remove :
        print("Contato removido com sucesso!!")
    else:
        print("Não foi encontrado esse usuario :(")

def atualizar():
    nome = input("Digite o nome Completo que você deseja atualizar: ")
    
    print("Agora digite as novas informação para este contato: ")
    telefone = input("Telefone (DD)XXXXX-XXXX: ")
    email = input("Email XXXXX@YYYY.ZZZ: ")
    nascimento = input("Nascimento DD/MM/YYYY: ")
    if  len(nome) > 5 and \
        len(telefone) > 5 and \
        len(email) > 5 and len(nascimento) == 10:
        date_format = '%d/%m/%Y'
        nascimento_date = datetime.strptime(nascimento, date_format)
        if nascimento_date < datetime.now():
            contato = Contato()
            contato.nome = nome
            contato.telefone = telefone
            contato.email = email
            contato.nascimento = nascimento_date
            resultado = atualizar_db(nome, contato)
            if resultado:
                print("Contato atualizado com sucesso!!")
            else:
                print("Não foi encontrado esse usuario :(")
            
        else:
            print("Data de nascimento incorreta")
    else:        
        print("Os valores precisam ser preenchidos com mais do que 5 caracteres em cada campo")
    
    
        
    
def menu_principal():
    """
        Função para mostrar um menu principal na tela, 
        que retornará a opção selecionada pelo cliente
    """
    while True:
        os.system("cls")
        print('''
            ------------------Menu----------------------
                  (G)erar a tabela no banco de dados   
                  (C)adastrar                          
                  (L)er Registro                       
                  (R)emover
                  (A)tualizar Registo                          
                  (S)air\n                             
            ---------------------------------------------
            ''')

        opcao = input("Escolha sua opção ==>")
        opcao_filtrada = opcao.lower()[0]
        if opcao_filtrada in ['g', 'c', 'l', 'r', 'a', 's']:
            return opcao_filtrada
        print("Opção é inválida, tecle <ENTER> para prosseguir")
        input()


def cadastrar() -> Contato:
    """
        Função para pedir os dados de contato, e retorna um objeto do tipo Contato
    """
    os.system("cls")
    print("Cadastro de Contato")
    nome = input("Nome completo: ")
    telefone = input("Telefone (DD)XXXXX-XXXX: ")
    email = input("Email XXXXX@YYYY.ZZZ: ")
    nascimento = input("Nascimento DD/MM/YYYY: ")
    if  len(nome) > 5 and \
        len(telefone) > 5 and \
        len(email) > 5 and len(nascimento) == 10:
        date_format = '%d/%m/%Y'
        nascimento_date = datetime.strptime(nascimento, date_format)
        if nascimento_date < datetime.now():
            contato = Contato()
            contato.nome = nome
            contato.telefone = telefone
            contato.email = email
            contato.nascimento = nascimento_date
            return contato
        print("Data de nascimento incorreta")
    print("Os valores precisam ser preenchidos com mais do que 5 caracteres em cada campo")
    return None



if __name__ == "__main__":
    executando = True
    while executando:
        escolha = menu_principal()
        print(f"O usuário escolheu: {escolha}")
        
        if escolha == 'g':
            gerar_tabela()
            
        elif escolha == 'c':
            contato = cadastrar()
            if contato is not None:
                if gravar_db( contato ):
                    print("\nContato cadastrado com sucesso")
                else:
                    print("\nErro ao cadatrar o contato")
            else:
                print("Contato inválido")
                
        elif escolha == 'l':
            ler()
            
        elif escolha == 'r':
            remover()
            
        elif escolha == 'a':
            atualizar()
            
        elif escolha == 's':
            executando = False
            print("Tchau até breve")
        input("Tecle <ENTER> para continuar")