import sqlite3
import asyncio

class Database:
    def __init__(self, name):
        try:
            self.__con = sqlite3.connect(name, check_same_thread=False)
        except sqlite3.Error as e:
            print(e)
            raise Exception(e)

        self.__cur = self.__con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__con.commit()
        self.__con.close()

    @property
    def connection(self):
        return self.__con

    @property
    def cursor(self):
        return self.__cur

    def close(self, commit=True):
        if commit:
            self.__con.commit()
        self.__con.close()

    def execute(self, sql, params=None):
        self.__cur.execute(sql, params or ())

    def fetchall(self):
        return self.__cur.fetchall()

    def fetchone(self):
        return self.__cur.fetchone()

    def lastrowid(self):
        return self.__cur.lastrowid

    def query(self, sql, params=None):
        self.execute(sql, params)
        return self.fetchall()

    async def query_async(self, sql: str, params=None):
        print(sql)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self.query, sql, params
        )
