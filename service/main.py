from data_reader import load_cnpjs
from data_writer import write_lojas
from psql import Interface
from consts import TABLES

def verify_tables():
    ps = Interface()
    try:
        for table in TABLES:
            _ = ps.exec(query=table['SQL_CREATE'])
        return True
    except:
        print('Algo deu errado, encerrando execução do serviço.')
        return False

def run_service():
    print('Verificando tabelas ...')
    if verify_tables() is True:
         # PRIMEIRAMENTE GARANTIMOS QUE TEREMOS AS TABELAS CRIADAS NO BANCO DE DADOS
        print('Tabelas encontradas no banco, prosseguindo ...')
        print('Lendo informações das lojas ...')
        cnpjs = load_cnpjs()
        print('Informações lidas, gravando dados das lojas no banco de dados ...')
        write_lojas(TABLES[0]['NAME'], cnpjs)
        print('Dados das lojas gravados, prosseguindo ...')
        

if __name__ == '__main__':
    run_service()