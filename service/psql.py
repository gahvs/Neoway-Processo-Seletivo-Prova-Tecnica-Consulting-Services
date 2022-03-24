from typing import Any
import psycopg2
import psycopg2.errors as errs
from sys import exit
import os
# from consts import TABLES

class Interface():

    def __init__(self, user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD'), host='db', port=5432, database=os.environ.get('POSTGRES_NAME')) -> None:
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
        
    def status(self) -> None:
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

    def close(self, detail: bool):
        self.__cursor.close()
        self.__conn.close()
        if detail: print('Connection closed')

    def __isSelectQuery(self, query:str) -> bool:
        return True if query.split(' ')[0].lower() == 'select' else False

    def dbIsValid(self) -> bool:
        return self.__cursor != None

    def exec(self, query: str) -> Any:

        if not self.dbIsValid(): self.__reconnect()
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
        except errs.SyntaxError as e:
            print(e) 
            self.__reconnect()
            return errs.SyntaxError
        except errs.UndefinedTable as e: 
            print(e) 
            self.__reconnect()
            return errs.UndefinedTable
        except errs.UndefinedColumn as e: 
            print(e) 
            self.__reconnect()
            return errs.UndefinedColumn

    def get(self, table_name: str, id: int) -> list:
        if not self.dbIsValid(): self.__reconnect()        
        query_data = "SELECT * FROM %s WHERE ID = %d" % (table_name, id)
        return self.exec(query=query_data)

    def size(self, table_name: str) -> list:
        if not self.dbIsValid(): self.__reconnect()
        query = "SELECT COUNT(ID) FROM %s" % table_name
        return self.exec(query=query)

    def head(self, table_name: str) -> list:
        if not self.dbIsValid(): self.__reconnect()
        query_data = "SELECT * FROM %s LIMIT 5;" % table_name
        return self.exec(query=query_data)

    def delete(self, table_name: str) -> bool:
        if not self.dbIsValid(): self.__reconnect()
        query = "DELETE FROM %s; COMMIT;" % table_name
        return self.exec(query=query)

    def drop(self, table_name: str) -> bool:
        if not self.dbIsValid(): self.__reconnect()
        query = 'DROP TABLE %s; COMMIT;' % table_name
        return self.exec(query=query)

    def tables(self) -> None:
        if not self.dbIsValid(): self.__reconnect()
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'"
        tables = self.exec(query)
        if tables is not None:
            print('Relations of %s in %s' % (self.__database, self.__host))
            for t in tables: print('    -',t[0])

    def columns(self, table_name: str) -> None:
        if not self.dbIsValid(): self.__reconnect()
        query = "SELECT COLUMN_NAME, DATA_TYPE FROM information_schema.COLUMNS WHERE TABLE_NAME = '%s'" % table_name
        columns_information = self.exec(query)
        if columns_information is not None:
            print('Columns of %s' % table_name)
            for c in columns_information:
                print('    -', c[0],':', c[1])
