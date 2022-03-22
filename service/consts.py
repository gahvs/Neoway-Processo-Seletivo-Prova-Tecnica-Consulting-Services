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
            CPF varchar(14) NOT NULL UNIQUE, 
            CPF_VALIDO boolean NOT NULL,  
            PRIVADO boolean NOT NULL,  
            INCOMPLETO boolean NOT NULL, 
            DATA_ULTIMA_COMPRA DATE, 
            TICKET_MEDIO REAL, 
            TICKET_ULTIMA_COMPRA REAL, 
            LOJA_MAIS_FREQUENTE bigserial,
            LOJA_ULTIMA_COMPRA bigserial,
            FOREIGN KEY(LOJA_MAIS_FREQUENTE) REFERENCES LOJA (ID) ON DELETE CASCADE,
            FOREIGN KEY(LOJA_ULTIMA_COMPRA) REFERENCES LOJA (ID) ON DELETE CASCADE
        ); COMMIT;

        """
    }
]