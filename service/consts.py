TABLES = [ 
    {
        'NAME': 'LOJA',
        'COLUMNS': ["ID", "CNPJ", "CNPJ_VALIDO"],
        'SQL_CREATE': """
            CREATE TABLE IF NOT EXISTS LOJA (
                ID bigserial NOT NULL PRIMARY KEY, 
                CNPJ varchar(18) NOT NULL, 
                CNPJ_VALIDO boolean NOT NULL
            ); COMMIT; 
            """,
    }, 
    {
        'NAME': 'CLIENTE',
        'COLUMNS': ["ID" , "DOCUMENTO" , "DOCUMENTO_VALIDO" ,  "PRIVADO" ,  "INCOMPLETO" ,"LOJA_MAIS_FREQUENTE" ,"LOJA_ULTIMA_COMPRA" ,"DATA_ULTIMA_COMPRA" , "TICKET_MEDIO", "TICKET_ULTIMA_COMPRA",]
        ,
        'SQL_CREATE': """
        
        CREATE TABLE IF NOT EXISTS CLIENTE (
            ID bigserial NOT NULL PRIMARY KEY, 
            DOCUMENTO varchar(18) NOT NULL, 
            DOCUMENTO_VALIDO boolean NOT NULL,  
            PRIVADO boolean NOT NULL,  
            INCOMPLETO boolean NOT NULL,
            LOJA_MAIS_FREQUENTE bigint NULL,
            LOJA_ULTIMA_COMPRA bigint NULL,
            DATA_ULTIMA_COMPRA DATE, 
            TICKET_MEDIO REAL, 
            TICKET_ULTIMA_COMPRA REAL
        ); COMMIT;

        """
    },
]