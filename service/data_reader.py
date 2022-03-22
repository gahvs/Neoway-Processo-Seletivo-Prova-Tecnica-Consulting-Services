from unicodedata import normalize

FILE_NAME = "base_teste.txt"

# CPF, PRIVATE, INCOMPLETO, DATA DA ÚLTIMA COMPRA, 
# TICKET MÉDIO, TICKET DA ÚLTIMA COMPRA,  LOJA MAIS FREQUÊNTE,
# LOJA DA ÚLTIMA COMPRA

def tratar(linha: str):
    cpf, private, \
    incompleto, data_ultima_compra, \
    ticket_medio, ticket_ultima_compra, \
    loja_mais_frequente, loja_ultima_compra = linha.split() # Desestruturando string do arquivo usando espaço em branco como separador

    # Substituindo 0 / 1 por representações booleanas no Postgres
    private = 'true' if private else 'false'
    incompleto = 'true' if incompleto else 'false'  

    # Substituindo ',' por '.' nos dados que representam moeda, que sejam diferentes de 'NULL',
    # para permitir conversão de str para float.
    ticket_medio = float(ticket_medio.replace(',', '.')) if ticket_medio != 'NULL' else 'NULL'
    ticket_ultima_compra =  float(ticket_ultima_compra.replace(',', '.')) if ticket_ultima_compra != 'NULL' else  'NULL'

    return (cpf, private, incompleto, data_ultima_compra, ticket_medio, ticket_ultima_compra, loja_mais_frequente, loja_ultima_compra)

def load_cnpjs() -> list:
    '''
        Essa rotina faz a leitura dos CNPJ's contidos nas últimas colunas 
        do arquivo (LOJA MAIS FREQUÊNTE ,LOJA DA ÚLTIMA COMPRA), armazenando-os em uma lista
        e retornando-a.
    '''
    cnpjs = list()
    with open(FILE_NAME, mode='r') as file:
        _ = file.readline() # cabeçalho do arquivo ignorado, interesse apenas nos dados
        for line in file.readlines():
            # os cnpjs estão contidos nas duas últimas colunas,
            # portanto é feito um split usando um espaço em branco como separador
            # para 'pegar' as duas últimas posições da lista resultante.
            doc_1, doc_2 = line.split()[-2], line.split()[-1] 
            # ignoramos CNPJ's nulos, e verificamos se o CNPJ lido já não foi lido
            # antes, para evitar duplicação de valores
            if not doc_1 in cnpjs and doc_1 != 'NULL': cnpjs.append(doc_1)
            if not doc_2 in cnpjs and doc_2 != 'NULL': cnpjs.append(doc_2)

    return cnpjs
 
def carregar_dados():
    with open(FILE_NAME, mode='r') as file:
        _ = file.readline() #ignorando header
        for linha in file.readlines():
            linha_tratada = tratar(linha)
            return linha_tratada