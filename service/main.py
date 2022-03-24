from data_reader import load_data
from data_writer import LojaWriter, ClienteWriter, CompraWriter
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
    if verify_tables() is True: # PRIMEIRAMENTE GARANTIMOS QUE TEREMOS AS TABELAS CRIADAS NO BANCO DE DADOS

        print('Tabelas verificadas, lendo dados do arquivo base ...')

        data = load_data()
        cnpj_col_1 = set(list(map(lambda tup: tup[-2], data)))
        cnpj_col_2 = set(list(map(lambda tup: tup[-1], data)))
        cnpjs = set(list(cnpj_col_1) + list(cnpj_col_2))
        
        print('Dados lidos, gravando informações no banco de dados ...')
        
        LW = LojaWriter(cnpjs=cnpjs)
        LW.start()

        CW = ClienteWriter(clientes_data=data)
        CW.start()

        # CIW = CompraWriter(clientes_info_data=data)
        # CIW.start()        

        

if __name__ == '__main__':
    run_service()