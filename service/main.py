from data_reader import load_data
from data_writer import LojaWriter, ClienteWriter
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
    print('    -Verificando tabelas ...')
    if verify_tables() is True: # PRIMEIRAMENTE GARANTIMOS QUE TEREMOS AS TABELAS CRIADAS NO BANCO DE DADOS

        print('    -Tabelas verificadas')
        print('    -Lendo dados do arquivo base ...')

        data = load_data()
        cnpj_col_1 = set(list(map(lambda tup: tup[-2], data)))
        cnpj_col_2 = set(list(map(lambda tup: tup[-1], data)))
        cnpjs = set(list(cnpj_col_1) + list(cnpj_col_2))
        
        print('    -Dados lidos, gravando informações no banco de dados ...')
        
        LW = LojaWriter(cnpjs=cnpjs)
        LW.start()

        CW = ClienteWriter(clientes_data=data)
        CW.write()
        print('    -Todos os dados foram escritos')

if __name__ == '__main__':
    print('\n\n            ====== INICIANDO SERVICO  ======           ', end='\n\n')
    init = time.time()
    run_service()
    final = time.time()
    print('    -Tempo de execução:', final - init, 'segundos')
    print('\n\n            ====== SERVICO FINALIZADO  ======           ', end='\n\n')