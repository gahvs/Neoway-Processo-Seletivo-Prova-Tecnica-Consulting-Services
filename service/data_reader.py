
FILE_NAME = "base_teste.txt"

# CPF, PRIVATE, INCOMPLETO, DATA DA ÚLTIMA COMPRA, 
# TICKET MÉDIO, TICKET DA ÚLTIMA COMPRA,  LOJA MAIS FREQUÊNTE,
# LOJA DA ÚLTIMA COMPRA

def tratar(linha: str, id: int):
    cpf, private, \
    incompleto, data_ultima_compra, \
    ticket_medio, ticket_ultima_compra, \
    loja_mais_frequente, loja_ultima_compra = linha.split() # Desestruturando string do arquivo usando espaço em branco como separador

    # Substituindo 0 / 1 por representações booleanas no Postgres
    private = "true" if private else "false"
    incompleto = "true" if incompleto else "false"  

    # Substituindo ',' por '.' nos dados que representam moeda, que sejam diferentes de 'NULL',
    # para permitir conversão de str para float. Os dados com valor igual a 'NULL' são convertidos para 0.0
    ticket_medio = float(ticket_medio.replace(',', '.')) if ticket_medio != 'NULL' else 0.0
    ticket_ultima_compra =  float(ticket_ultima_compra.replace(',', '.')) if ticket_ultima_compra != 'NULL' else  0.0

    return (
        id,
        cpf,
        private,
        incompleto,
        data_ultima_compra,
        ticket_medio,
        ticket_ultima_compra,
        loja_mais_frequente,
        loja_ultima_compra
    )

def load_data() -> list:
    '''
        Essa rotina faz a leitura de todas as linhas do arquivo base, armazenando-os (já tratados)
        em uma lista e devolvendo como retorno.
    '''
    id = 1
    data = list()
    # cpfs_included = list()
    with open(FILE_NAME, mode='r') as file:
        _ = file.readline() # cabeçalho do arquivo ignorado, interesse apenas nos dados
        for linha in file.readlines():
            linha_tratada = tratar(linha, id)
            id = id + 1
            # if not linha_tratada[0] in cpfs_included:
                # cpfs_included.append(linha_tratada[0])
            data.append(linha_tratada)
         
    return data