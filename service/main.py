from data_reader import load_cnpjs, load_clientes
from data_writer import write_lojas, write_clientes
from psql import Interface
from consts import TABLES
import time

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
    if verify_tables() is True: # PRIMEIRAMENTE GARANTIMOS QUE TEREMOS AS TABELAS CRIADAS NO BANCO DE DADOS

        print('Tabelas encontradas no banco, prosseguindo ...')
        print('Carregando Dados das lojas ...')
        cnpjs = load_cnpjs()
        print('Dados lidas, gravando dados das lojas no banco de dados ...')
        write_lojas(TABLES[0]['NAME'], cnpjs)
        print('Dados das lojas gravados, prosseguindo ...')
        print('Carregando Dados dos clientes ...')
        clientes = load_clientes()
        print('Dados carregandos, gravando dados dos clientes no banco de dados ...')
        write_clientes(clientes_table_name=TABLES[1]['NAME'], clientes_data=clientes, loja_table_name=TABLES[0]['NAME'])
        print('Dados migradros com sucesso.')

if __name__ == '__main__':
    init = time.time()
    run_service()
    final = time.time()
    print('\nTempo total de execução:', final - init)