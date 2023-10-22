from backend.database.sql_connection import Database

"""
This file contains the API for the cashflow database

The database contains three tables:
    - Intrari
    - Iesiri
    - DateLunare
    - ConturiBancare
    - Config
    
The Intrari table contains the following columns:
    -------------------------------------------------------------------------------------------------------
    |   ID  |     TIP      |   ZI   |   LUNA    |   AN    |   Companie    |   Valoare |   TVA |   Total   |
    -------------------------------------------------------------------------------------------------------
    |   INT |   'Iesire'   |   INT  |   INT     |   INT    |  VARCHAR     |   FLOAT   | FLOAT |   FLOAT   |
    
    
The Iesiri table contains the following columns:
    -------------------------------------------------------------------------------------------------------
    |   ID  |     TIP      |   ZI   |   LUNA    |   AN    |   Companie    |   Valoare |   TVA |   Total   |
    -------------------------------------------------------------------------------------------------------
    |   INT |   'Iesire'   |   INT  |   INT     |   INT    |  VARCHAR     |   FLOAT   | FLOAT |   FLOAT   |
    

The DateLunare table contains the following columns:
    -------------------------------------------------
    |   ID  |   Luna    |   An  |   SumaInitiala    |
    -------------------------------------------------
    |   INT |   INT     |   INT |   FLOAT           |


The ConturiBancare table contains the following columns:
    -------------------------------------------------
    |   ID  |   Banca   |   Sold    |
    -------------------------------------------------
    |   INT |   VARCHAR |   FLOAT   |


The Config table contains the following columns:
    ---------------------------------------------
    |   ID  |   Parola_Useri    |   Parola_Admin |
    ---------------------------------------------
    |   INT |   VARCHAR         |   VARCHAR      |
    
    
:author:    Mihai Tira
"""

from pypika import Query, Table, Field, Order, Case
from datetime import datetime

DB_PATH = 'backend/database/cashflow.db'

#   Create the tables if they don't exist
async def create_cashflow_table() -> bool:
    """
    Create the cashflow table if it doesn't exist
    :return: Boolean value indicating if the table was created or not
    """

    try:
        with Database(DB_PATH) as db:

            #   Tabele intrari-iesiri
            db.execute("""
            CREATE TABLE IF NOT EXISTS Intrari (
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                TIP VARCHAR(25) DEFAULT 'Intrare',
                Zi INTEGER NOT NULL,
                Luna INTEGER NOT NULL,
                An INTEGER NOT NULL,
                Companie VARCHAR(255),
                Valoare DECIMAL(10, 3),
                TVA DECIMAL(10, 3),
                Total DECIMAL(10, 3)
            );
            """)

            db.execute("""
            CREATE TABLE IF NOT EXISTS Iesiri (
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                TIP VARCHAR(25) DEFAULT 'Iesire',
                Zi INTEGER NOT NULL,
                Luna INTEGER NOT NULL,
                An INTEGER NOT NULL,
                Companie VARCHAR(255),
                Valoare DECIMAL(10, 3),
                TVA DECIMAL(10, 3),
                Total DECIMAL(10, 3)
                );
            """)

            #   Tabela date lunare
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS DateLunare (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    Luna INTEGER NOT NULL,
                    An INTEGER NOT NULL,
                    SumaInitiala DECIMAL(10, 3) DEFAULT 0
                );
                """
            )

            #   Tabela config cont bancar
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS ConturiBancare (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    Banca VARCHAR(255),
                    Sold INTEGER DEFAULT 0
                );
                """
            )

    except Exception as e:
        print(e)
        return False

    return True




#   Create operations   -   ASYNC
async def insert_intrare(
        data: str | list[int, int, int],
        companie: str,
        val: float,
        tva: float,
        total: float,
        db_connection: Database = None
) -> list[tuple]:

    """
    Insert a new entry into the Intrari table
    :param data: Date of the entry
    :param companie: Company name
    :param val: Value
    :param tva: TVA
    :param total: Total
    :return: Boolean value indicating if the entry was inserted or not
    """

    if isinstance(data, str):
        data = [int(x) for x in data.split('-')]

    try:
        if db_connection:
            query = Query.into(
                'Intrari'
            ).columns(
                'Zi', 'Luna', 'An', 'Companie', 'Valoare', 'TVA', 'Total'
            ).insert(
                (*data, companie, val, tva, total)
            )

            return await db_connection.query_async(query.get_sql())


        with Database(DB_PATH) as db:
            query = Query.into(
                'Intrari'
            ).columns(
                'Zi', 'Luna', 'An', 'Companie', 'Valoare', 'TVA', 'Total'
            ).insert(
                (*data, companie, val, tva, total)
            )

            return await db.query_async(query.get_sql())
    except Exception as e:
        print(e)
        return []

async def insert_intrare_many(
        entries: list[
                list[
                    tuple[int, int, int] | str,
                    str,
                    float,
                    float,
                    float]
            ],
        db_connection: Database = None
) -> list[tuple]:
    """
    Insert multiple entries into the Intrari table
    :param data: Date of the entries
    :param companie: Company names
    :param val: Values
    :param tva: TVAs
    :param total: Totals
    :return: Boolean value indicating if the entries were inserted or not
    """

    try:
        entries_added = []

        if db_connection:
            for entry in entries:

                if isinstance(entry[0], str):
                    entry[0] = [int(x) for x in entry[0].split('-')]

                res = await insert_intrare(*entry, db_connection=db_connection)

                entries_added.append(res)

        with Database(DB_PATH) as db:
            for entry in entries:

                if isinstance(entry[0], str):
                    entry[0] = [int(x) for x in entry[0].split('-')]

                res = await insert_intrare(*entry, db_connection=db)

                entries_added.append(res)

        return entries_added
    except Exception as e:
        print(e)
        return []


async def insert_iesire(
        data: str | list[int, int, int],
        companie: str,
        val: float,
        tva: float,
        total: float,
        db_connection: Database = None
) -> list[tuple]:

    """
    Insert a new entry into the Iesiri table
    :param data: Date of the entry
    :param companie: Company name
    :param val: Value
    :param tva: TVA
    :param total: Total
    :return: Boolean value indicating if the entry was inserted or not
    """
    if isinstance(data, str):
        data = [int(x) for x in data.split('-')]

    try:

        if db_connection:
            query = Query.into(
                'Iesiri'
            ).columns(
                'Zi', 'Luna', 'An', 'Companie', 'Valoare', 'TVA', 'Total'
            ).insert(
                (*data, companie, val, tva, total)
            )

            return await db_connection.query_async(query.get_sql())

        with Database(DB_PATH) as db:

            query = Query.into(
                'Iesiri'
            ).columns(
                'Zi', 'Luna', 'An', 'Companie', 'Valoare', 'TVA', 'Total'
            ).insert(
                (*data, companie, val, tva, total)
            )

            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []

async def insert_iesire_many(
        entries: list[
                    tuple[
                        list[int, int, int] | str,
                        str,
                        float,
                        float,
                        float]
                ],
        db_connection: Database = None
) -> list[tuple]:
    """
    Insert multiple entries into the Iesiri table
    :param data: Date of the entries
    :param companie: Company names
    :param val: Values
    :param tva: TVAs
    :param total: Totals
    :return: Boolean value indicating if the entries were inserted or not
    """

    try:
        entries_added = []

        if db_connection:
            for entry in entries:

                if isinstance(entry[0], str):
                    entry[0] = [int(x) for x in entry[0].split('-')]

                res = await insert_iesire(*entry, db_connection=db_connection)

                entries_added.append(res)

        with Database(DB_PATH) as db:
            for entry in entries:

                if isinstance(entry[0], str):
                    entry[0] = [int(x) for x in entry[0].split('-')]

                res = await insert_iesire(*entry, db_connection=db)

                entries_added.append(res)

        return entries_added
    except Exception as e:
        print(e)
        return []

async def insert_date_lunare(
        luna: int,
        an: int,
        suma_initiala: float,
        db_connection: Database = None
) -> list[tuple]:

    """
    Insert a new entry into the DateLunare table
    :param luna: Luna
    :param an: An
    :param suma_initiala: Suma initiala
    :return: Boolean value indicating if the entry was inserted or not
    """

    try:
        if db_connection:
            query = Query.into(
                'DateLunare'
            ).columns(
                'Luna', 'An', 'SumaInitiala'
            ).insert(
                luna, an, suma_initiala
            )

            return await db_connection.query_async(query.get_sql())

        with Database(DB_PATH) as db:
            query = Query.into(
                'DateLunare'
            ).columns(
                'Luna', 'An', 'SumaInitiala'
            ).insert(
                luna, an, suma_initiala
            )

            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []

async def insert_cont_bancar(
        banca: str,
        sold: float,
        db_connection: Database = None
) -> list[tuple]:

    try:
        if db_connection:
            query = Query.into(
                'ConturiBancare'
            ).columns(
                'Banca', 'Sold'
            ).insert(
                banca, sold
            )

            return await db_connection.query_async(query.get_sql())

        with Database(DB_PATH) as db:
            query = Query.into(
                'ConturiBancare'
            ).columns(
                'Banca', 'Sold'
            ).insert(
                banca, sold
            )

            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []


#   =================================================================
#   =================================================================


#   Read operations     -   ASYNC
async def get_intrari(
        luna: int= None,
        an: int = None,
        firma: str = None,
        db_connection: Database = None
) -> list[list[tuple]]:

    """
    Get all the entries from the Intrari table
    :param luna: Lunile dorite
    :return: List of entries
    """

    try:
        table = Table('Intrari')
        query = Query.from_(table).select('*')

        print(query.get_sql())

        if luna:
            luna = int(luna)
            query = query.where(
                table.Luna == luna
            )
        else:
            query = query.where(
                table.Luna == datetime.now().month
            )


        if an:
            an = int(an)
            query = query.where(
                table.An == an
            )
        else:
            query = query.where(
                table.An == datetime.now().year
            )

        if firma:
            query = query.where(
                table.Companie == firma
            )

        if db_connection:
            return await db_connection.query_async(query.get_sql())


        with Database(DB_PATH) as db:
            return await db.query_async(query.get_sql())


    except Exception as e:
        print(e)
        return []

async def get_iesiri(
        luna: int = None,
        an: int = None,
        firma: str = None,
        db_connection: Database = None
) -> list[list[tuple]]:

    """
    Get all the entries from the Intrari table
    :param luna: Lunile dorite (daca e -1, se vor returna toate intrarile)
    :return: List of entries
    """

    try:

        table = Table('Iesiri')
        query = Query.from_(table).select('*')

        if luna:
            luna = int(luna)
            query = query.where(
                table.Luna == luna
            )
        else:
            query = query.where(
                table.Luna == datetime.now().month
            )

        if an:
            an = int(an)
            query = query.where(
                table.An == an
            )
        else:
            query = query.where(
                table.An == datetime.now().year
            )

        if firma:
            query = query.where(
                table.Companie == firma
            )


        if db_connection:
            return await db_connection.query_async(query.get_sql())


        with Database(DB_PATH) as db:
            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []

async def get_recent_operations(
        limit: int,
        db_connection: Database = None
) -> list[list[tuple]]:

    """
    Get the most recent operations
    :param limit: Limit of operations
    :return: List of entries
    """

    intrari = Table('Intrari')
    iesiri = Table('Iesiri')

    # Make an union of the two tables
    query = Query.from_(intrari).select('*') + Query.from_(iesiri).select('*')
    query = query.orderby('Zi', order=Order.desc).orderby('Luna', order=Order.desc).orderby('An', order=Order.desc)
    query = query.limit(limit)

    try:
        query = str(query)
        query = query.translate(
            str.maketrans(
                {
                    '(': '',
                    ')': '',
                })
        )

        if db_connection:
            return await db_connection.query_async(query)

        with Database(DB_PATH) as db:
            return await db.query_async(query)

    except Exception as e:
        print(e)
        return []

async def get_date_lunare(
        luna: int = None,
        an: int = None,
        db_connection: Database = None
) -> tuple:

    """
    Get the most recent operations
    :param limit: Limit of operations
    :return: List of entries
    """

    try:
        table = Table('DateLunare')
        query = Query.from_(table).select('SumaInitiala')

        if luna:
            luna = int(luna)
            query = query.where(
                table.Luna == luna
            )
        else:
            query = query.where(
                table.Luna == datetime.now().month
            )

        if an:
            an = int(an)
            query = query.where(
                table.An == an
            )
        else:
            query = query.where(
                table.An == datetime.now().year
            )

        if db_connection:
            return await db_connection.query_async(query.get_sql())

        with Database(DB_PATH) as db:
            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return ()

async def get_conturi_bancare(
        db_connection: Database = None
) -> list[tuple]:

    try:
        table = Table('ConturiBancare')
        query = Query.from_(table).select('Banca', 'Sold')

        if db_connection:
            return await db_connection.query_async(query.get_sql())

        with Database(DB_PATH) as db:
            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []


#   =================================================================
#   =================================================================


#   Update operations   -   ASYNC
async def update_intrari(
        data: tuple[int, int, int],
        companie: str,
        values: tuple) -> list[list[tuple]]:
    """
    Update an entry from the Intrari table
    :param data: Data dorita pentru update (daca e ALL, se vor updata toate intrarile)
    :param companie: Compania dorita pentru update (daca e ALL, se vor updata toate intrarile)
    :param values: Valori noi (In ordinea: DataIntrare, Companie, Valoare, TVA, Total)
    :return:
    """

    # try:
    #     with Database(DB_PATHas db:
    #
    #         query = Query.update('Intrari')\
    #             .set('')
    #
    # except:
    #     return []
    raise NotImplementedError

async def update_iesiri(
        data: tuple[int, int, int],
        companie: str,
        values: tuple) -> list[list[tuple]]:
    """
    Update an entry from the Iesiri table
    :param data: Data dorita pentru update (daca e ALL, se vor updata toate intrarile)
    :param companie: Compania dorita pentru update (daca e ALL, se vor updata toate intrarile)
    :param values: Valori noi (In ordinea: DataIesire, Companie, Valoare, TVA, Total)
    :return:
    """

    # try:
    #     with Database(DB_PATHas db:
    #
    #         # Build the string for the query
    #         query = f"UPDATE Iesiri SET Valoare = ?, TVA = ?, Total = ?"
    #
    #         # Add the WHERE clause if needed
    #         if data != "ALL" and companie != "ALL":
    #             query += " WHERE DataIesire = ? AND Companie = ?"
    #         elif data != "ALL":
    #             query += " WHERE DataIesire = ?"
    #         elif companie != "ALL":
    #             query += " WHERE Companie = ?"
    #
    #         return await db.query_async(query, (*values, data, companie))
    #
    # except:
    #     return []
    raise NotImplementedError

async def update_date_lunare(
        luna: int,
        an: int,
        suma_initiala: float,
        db_connection: Database = None
) -> list[tuple]:

    """
    Update an entry from the DateLunare table
    :param luna: Luna
    :param an: An
    :param suma_initiala: Suma initiala
    :return: Boolean value indicating if the entry was inserted or not
    """

    try:
        if db_connection:
            query = Query.update('DateLunare')\
                .set('SumaInitiala', suma_initiala)\
                .where(
                    (Field('Luna') == luna) & (Field('An') == an)
                )

            return await db_connection.query_async(query.get_sql())

        with Database(DB_PATH) as db:
            query = Query.update('DateLunare')\
                .set('SumaInitiala', suma_initiala)\
                .where(
                    (Field('Luna') == luna) & (Field('An') == an)
                )

            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []

async def update_cont_bancar(
        banca: str,
        sold: float,
        db_connection: Database = None
) -> list[tuple]:

    try:
        if db_connection:
            query = Query.update('ConturiBancare')\
                .set('Sold', sold)\
                .where(
                    Field('Banca') == banca
                )

            return await db_connection.query_async(query.get_sql())

        with Database(DB_PATH) as db:
            query = Query.update('ConturiBancare')\
                .set('Sold', sold)\
                .where(
                    Field('Banca') == banca
                )

            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []


#   Delete operations
async def delete_intrare(
        data: str | tuple[int, int, int],
        companie: str,
        suma: float
) -> list[list[tuple]]:
    """
    Delete an entry from the Intrari table
    :param data: Data dorita pentru delete (daca e ALL, se vor sterge toate intrarile)
    :param companie: Compania dorita pentru delete (daca e ALL, se vor sterge toate intrarile)
    :return:
    """

    if isinstance(data, str):
        data = [int(x) for x in data.split('-')]
        data = tuple(data)


    try:
        with Database(DB_PATH) as db:

            table = Table('Intrari')
            select_query = Query.from_(table).select('ID').where(
                (table.Zi == data[0]) & (table.Luna == data[1]) & (table.An == data[2]) & (table.Valoare == suma) & (table.Companie == companie)
            ).limit(1)

            id = (await db.query_async(select_query.get_sql()))[0]

            query = Query.from_(table).where(
                table.ID == id
            ).delete()

            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []

async def delete_iesire(
        data: str | tuple[int, int, int],
        companie: str,
        suma: float
) -> list[list[tuple]]:
    """
    Delete an entry from the Iesiri table
    :param data: Data dorita pentru delete (daca e ALL, se vor sterge toate intrarile)
    :param companie: Compania dorita pentru delete (daca e ALL, se vor sterge toate intrarile)
    :return:
    """

    if isinstance(data, str):
        data = [int(x) for x in data.split('-')]
        data = tuple(data)

    try:
        with Database(DB_PATH) as db:

            table = Table('Iesiri')
            query = Query.from_(table).where(
                (table.Zi == data[0]) & (table.Luna == data[1]) & (table.An == data[2]) & (table.Valoare == suma) & (table.Companie == companie)
            ).delete()

            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []

async def delete_cont_bancar(banca: str) -> list[list[tuple]]:

    try:
        with Database(DB_PATH) as db:

            table = Table('ConturiBancare')
            query = Query.from_(table).where(
                table.Banca == banca
            ).delete()

            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []
