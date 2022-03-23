from utils import cnpj_is_valid, cpf_is_valid
from psql import Interface

def cnpj_already_exists(cnpj: str) -> bool:
    """
        Verifica se o CNPJ já existe no banco antes de fazer uma inserção.
        Evita Unique Violation.
    """
    ps = Interface()
    query = "SELECT ID FROM LOJA WHERE cnpj = '%s'" % cnpj
    ID_FROM_CNPJ = ps.exec(query=query)
    ps.close(detail=False)
    if ID_FROM_CNPJ is None:
        return False
    return True

def cpf_already_exists( cpf: str) -> bool: 
    """
        Verifica se o CPF já existe no banco de dados antes de fazer uma inserção.
        Evita Unique Violation
    """
    ps = Interface()
    query = "SELECT ID FROM CLIENTE WHERE cpf = '%s'" % cpf
    ID_FROM_CPF = ps.exec(query=query)
    ps.close(detail=False)
    if ID_FROM_CPF is None:
        return False
    return True

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

def loja_id_from_cnpj(table_name: str, cnpj: str) -> int:
    '''
        Retorna o valor do campo ID, da tupla que contem o cnpj 
        passado como parâmetro na tabela referida.
    '''
    if cnpj == 'NULL': return "null"
    ps = Interface()
    query = "SELECT ID FROM %s WHERE CNPJ = '%s'" % (table_name, cnpj)
    LOJA_ID = ps.exec(query=query)
    ps.close(detail=False)
    return LOJA_ID[0][0] # o retorno é no formato [(1,)] (tupla dentro de lista)

def write_lojas(table_name:str, cnpjs: list):
    '''
        Recebe a lista de CNPJS e persiste os dados na tabela LOJA.
    '''
    query_insert = """
        INSERT INTO %s (id, cnpj, cnpj_valido) VALUES ('%d', '%s', %s)
    """
    ps = Interface()
    for cnpj in cnpjs:
        if not cnpj_already_exists(cnpj=cnpj):
            ps.exec(query=query_insert % (table_name, last_id_from(table_name) + 1, cnpj, cnpj_is_valid(cnpj)))

    ps.close(detail=False)

def write_clientes(clientes_table_name: str, clientes_data: list, loja_table_name: str):
    '''
        Recebe os dados do arquivo base e os persiste no banco de dados.
    '''
    query_insert = """

        INSERT INTO %s (id, cpf, cpf_valido, privado, incompleto, data_ultima_compra, ticket_medio,
         ticket_ultima_compra, loja_mais_frequente, loja_ultima_compra) 
         VALUES ('%d', '%s', %s, %s, %s, %s, '%f', '%f', %s, %s)

    """
    ps = Interface()
    for cliente in clientes_data:

        query=query_insert % (clientes_table_name,
            last_id_from(table_name=clientes_table_name) + 1, 
            cliente['cpf'], 
            cpf_is_valid(cliente['cpf']), 
            cliente['private'], 
            cliente['incompleto'],
            cliente['data_ultima_compra'].lower(), 
            cliente['ticket_medio'], 
            cliente['ticket_ultima_compra'], 
            str(loja_id_from_cnpj(table_name=loja_table_name, cnpj=cliente['loja_mais_frequente'])),
            str(loja_id_from_cnpj(table_name=loja_table_name, cnpj=cliente['loja_ultima_compra']))
        )

        # if not cpf_already_exists(cpf=cliente['cpf']):
        ps.exec(query=query)        

    ps.close(detail=False)