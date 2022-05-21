from utils import cnpj_is_valid, cpf_is_valid
from psql import Interface

def last_id_from(table_name: str) -> int:
    '''
        Retorna o último ID na tabela passada como parâmetro. Se não 
        houverem registros o retorno será 0. Assume-se que a tabela 
        possui um campo ID: BIGSERIAL
    '''
    ps = Interface()
    query = 'SELECT ID FROM %s ORDER BY ID DESC LIMIT 1' % table_name
    LAST_ID_IN_TABLE = ps.exec(query=query)
    ps.close(detail=False)
    if LAST_ID_IN_TABLE is None: 
        return 0
    return LAST_ID_IN_TABLE[0][0] # o retorno é no formato [(1,)] (tupla dentro de lista)

def make_dict_from_loja() -> list:
    '''
        Cria um dicionario que associa cada CNPJ da tabela LOJA
        com seu respectivo ID. É usado para evitar que as inserções 
        de tuplas na tabela CLIENTE necessitem de consultas ao banco de dados para 
        recuperar o ID da loja (usado no campos LOJA_MAIS_FREQUENTE, LOJA_ULTIMA_COMPRA).
    '''
    ps = Interface()
    lojas = ps.exec('SELECT * FROM LOJA')
    lojas_dict = dict()
    for tup in lojas:
        lojas_dict[tup[1]] = tup[0] 
    lojas_dict['NULL'] = 'NULL'
    return lojas_dict

class LojaWriter():
    '''
        Classe usada para persistir os dados referentes a tabela LOJA
    '''
    def __init__(self, cnpjs: set) -> None:
        self.loja_data = cnpjs
        self.query_insert = """ INSERT INTO LOJA (id, cnpj, cnpj_valido) VALUES ('%d', '%s', %s);"""
    
    def write(self):
        '''
            Monta um script de inserção para a tabela LOJA de acordo 
            com os dados lidos do arquivo base e então executa o script no
            banco de dados.
        '''
        ps = Interface()
        query = ''
        LOJA_ID = last_id_from('LOJA') + 1
        for cnpj in self.loja_data:
            if cnpj != 'NULL':
                query += self.query_insert % (LOJA_ID, cnpj, cnpj_is_valid(cnpj))
                LOJA_ID += 1
        ps.exec(query)
        print('    -Dados das lojas inseridos')
        ps.close(detail=False)

class ClienteWriter():
    '''
        Classe usada para persistir os dados referentes a tabela CLIENTE
    '''
    def __init__(self, clientes_data: list) -> None:
        self.clientes_data = clientes_data
        self.query_insert_with_data_non_null = """ INSERT INTO CLIENTE (id, documento, documento_valido, privado, incompleto, loja_mais_frequente, loja_ultima_compra, data_ultima_compra, ticket_medio,
         ticket_ultima_compra) 
         VALUES ('%d', '%s', %s, %s, %s, %s, %s, '%s', '%f', '%f');
        """
        self.query_insert_with_data_null = """ INSERT INTO CLIENTE (id, documento, documento_valido, privado, incompleto, loja_mais_frequente, loja_ultima_compra, data_ultima_compra, ticket_medio,
         ticket_ultima_compra) 
         VALUES ('%d', '%s', %s, %s, %s, %s, %s, %s, '%f', '%f');
        """
    
    def write(self):
        '''
            Monta um script de inserção para a tabela CLIENTE de acordo 
            com os dados lidos do arquivo base e então executa o script no
            banco de dados.
        '''
        ps = Interface()
        query = ''
        loja_id_map = make_dict_from_loja()
        for c in self.clientes_data:
            if c[4] == 'NULL':
                query += self.query_insert_with_data_null % (c[0], c[1], cpf_is_valid(c[1]), c[2], c[3], loja_id_map[c[-2]], loja_id_map[c[-1]], c[4], c[5], c[6])
            else:
                query += self.query_insert_with_data_non_null % (c[0], c[1], cpf_is_valid(c[1]), c[2], c[3], loja_id_map[c[-2]], loja_id_map[c[-1]], c[4], c[5], c[6])
        ps.exec(query=query)
        print('    -Dados dos clientes inseridos')
        ps.close(detail=False)
