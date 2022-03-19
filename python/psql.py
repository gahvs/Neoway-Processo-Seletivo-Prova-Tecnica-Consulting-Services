from typing import Any
import psycopg2
import psycopg2.errors as errs
from sys import exit

class Interface():

    def __init__(self, user='postgres', password='postgres', host='localhost', port=5432, database='postgres') -> None:
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port
        self.__database = database

        try:
            self.__conn = psycopg2.connect(
                user=self.__user, password=self.__password, host=self.__host, port=self.__port, database=self.__database
            )
            self.__cursor = self.__conn.cursor()
        except errs.DatabaseError as e:
            print('Database Error:\n', e)
            exit()
        
        print('Connected to %s in %s.' % (self.__database, self.__host))


    def __reconnect(self) -> None:
        try:
            self.__conn = psycopg2.connect(
                user=self.__user, password=self.__password, host=self.__host, port=self.__port, database=self.__database
            )
            self.__cursor = self.__conn.cursor()
        except errs.DatabaseError as e:
            print('Database Error:\n', e)
            exit()

    def close(self):
        self.__cursor.close()
        self.__conn.close()
        print('Connection closed')

    def __isSelectQuery(self, query:str) -> bool:
        return True if query.split(' ')[0].lower() == 'select' else False

    def dbIsValid(self) -> bool:
        return self.__cursor != None

    def exec(self, query: str) -> Any:
        if self.dbIsValid():
            try:
                self.__cursor.execute(query=query)
                if self.__isSelectQuery(query=query):
                    rows = self.__cursor.fetchall()
                    return None if not len(rows) else [r for r in rows]
                else:
                    self.__conn.commit()
                return
            except psycopg2.InterfaceError:
                opt = input('Conexão com o banco de dados encerrada.\nDigite S para conectar novamente ... \n')
                if opt.lower() == 's': 
                    self.__reconnect()
                    print('Conexão reestabelecida')
                return
            except errs.SyntaxError as e: print('Erro de Sintaxe:\n', e)
            except errs.UndefinedTable as e: print('Tabela inexistente:\n', e)
            except errs.UndefinedColumn as e: print('Coluna inexistente:\n', e)
            self.__reconnect()

    def tables(self) -> None:
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'"
        tables = self.exec(query)
        if tables is not None:
            print('Relations of %s in %s' % (self.__database, self.__host))
            for t in tables: print('    -',t[0])

    def columns(self, table_name: str) -> None:
        query = "SELECT COLUMN_NAME, DATA_TYPE FROM information_schema.COLUMNS WHERE TABLE_NAME = '%s'" % table_name
        columns_information = self.exec(query)
        if columns_information is not None:
            print('Columns of %s' % table_name)
            for c in columns_information:
                print('    -', c[0],':', c[1])

