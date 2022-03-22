from tkinter import LAST
from utils import cnpj_is_valid, cpf_is_valid
from psql import Interface

def cnpj_already_exists(table_name: str, cnpj: str) -> bool:
    """
        Verifica se o CNPJ já existe no banco antes de fazer uma inserção.
        Evita Unique Violation.
    """
    ps = Interface()
    query = "SELECT ID FROM %s WHERE cnpj = '%s'" % (table_name, cnpj)
    ID_FROM_CNPJ = ps.exec(query=query)
    ps.close(detail=False)
    if ID_FROM_CNPJ is None:
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

def write_lojas(table_name:str, cnpjs: list):
    query_insert = """
        INSERT INTO %s (id, cnpj, cnpj_valido) VALUES ('%d', '%s', %s)
    """
    ps = Interface()
    for cnpj in cnpjs:
        if not cnpj_already_exists(table_name=table_name, cnpj=cnpj):
            ps.exec(query=query_insert % (table_name, last_id_from(table_name) + 1, cnpj, cnpj_is_valid(cnpj)))


    