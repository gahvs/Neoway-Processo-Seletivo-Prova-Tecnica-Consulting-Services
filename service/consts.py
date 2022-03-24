TABLES = [ 
    {
        'NAME': 'LOJA',
        'SQL_CREATE': """
            CREATE TABLE IF NOT EXISTS LOJA (
                ID bigserial NOT NULL PRIMARY KEY, 
                CNPJ varchar(18) NOT NULL UNIQUE, 
                CNPJ_VALIDO boolean NOT NULL
            ); COMMIT; 
            """,
    }, 
    {
        'NAME': 'CLIENTE',
        'SQL_CREATE': """
        
        CREATE TABLE IF NOT EXISTS CLIENTE (
            ID bigserial NOT NULL PRIMARY KEY, 
            DOCUMENTO varchar(18) NOT NULL, 
            DOCUMENTO_VALIDO boolean NOT NULL,  
            PRIVADO boolean NOT NULL,  
            INCOMPLETO boolean NOT NULL,
            LOJA_MAIS_FREQUENTE bigint NULL,
            LOJA_ULTIMA_COMPRA bigint NULL
        ); COMMIT;

        """
    },
    {
        'NAME': 'COMPRA',
        'SQL_CREATE': """
        CREATE TABLE IF NOT EXISTS COMPRA (
            ID bigserial NOT NULL PRIMARY KEY,
            CLIENTE bigint NOT NULL,
            DATA_ULTIMA_COMPRA DATE, 
            TICKET_MEDIO REAL, 
            TICKET_ULTIMA_COMPRA REAL
        ); COMMIT;
        """
    }
]


# Observações:

# Foi verificado antes da criação do serviço que
# cada linha do arquivo possui um CPF diferente, portanto não há problemas em usar 
# um campo tipo UNIQUE para armazená-los.