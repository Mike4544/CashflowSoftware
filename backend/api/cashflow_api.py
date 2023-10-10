from backend.database.sql_connection import Database

"""
This file contains the API for the cashflow database

The database contains three tables:
    - Intrari
    - Iesiri
    - Config
    
The Intrari table contains the following columns:
    -----------------------------------------------------------------------------------------
    |   ID  |       TIP     |   DataIntrare |   Companie    |   Valoare |   TVA |   Total   |
    -----------------------------------------------------------------------------------------
    |   INT |   'Intrare'   |   DATE        |   VARCHAR     |   FLOAT   | FLOAT |   FLOAT   |
    
    
The Iesiri table contains the following columns:
    -----------------------------------------------------------------------------------------
    |   ID  |     TIP      |   DataIesire  |   Companie    |   Valoare |   TVA |   Total   |
    -----------------------------------------------------------------------------------------
    |   INT |   'Iesire'   |   DATE        |   VARCHAR     |   FLOAT   | FLOAT |   FLOAT   |
    

The Config table contains the following columns:
    ---------------------------------------------
    |   ID  |   Parola_Useri    |   Parola_Admin |
    ---------------------------------------------
    |   INT |   VARCHAR         |   VARCHAR      |
    
    
:author:    Mihai Tira
"""

#   Create the tables if they don't exist
def create_cashflow_table() -> bool:
    """
    Create the cashflow table if it doesn't exist
    :return: Boolean value indicating if the table was created or not
    """

    try:
        with Database('cashflow.db') as db:
            db.execute("""
            CREATE TABLE IF NOT EXISTS Intrari (
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                TIP VARCHAR(25) DEFAULT 'Intrare',
                DataIntrare DATE,
                Companie VARCHAR(255),
                Valoare DECIMAL(10, 2),
                TVA DECIMAL(10, 2),
                Total DECIMAL(10, 2)
            );
            """)

            db.execute("""
            CREATE TABLE IF NOT EXISTS Iesiri (
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                TIP VARCHAR(25) DEFAULT 'Iesire',
                DataIesire DATE,
                Companie VARCHAR(255),
                Valoare DECIMAL(10, 2),
                TVA DECIMAL(10, 2),
                Total DECIMAL(10, 2)
                );
            """)
    except:
        return False

    return True


#   Create operations   -   ASYNC
async def insert_intrare(data: str, companie: str, val: float, tva: float, total: float) -> list[tuple]:

    """
    Insert a new entry into the Intrari table
    :param data: Date of the entry
    :param companie: Company name
    :param val: Value
    :param tva: TVA
    :param total: Total
    :return: Boolean value indicating if the entry was inserted or not
    """

    try:
        with Database('cashflow.db') as db:
            return await db.query_async("""
            INSERT INTO Intrari (DataIntrare, Companie, Valoare, TVA, Total)
            VALUES (?, ?, ?, ?, ?);
            """, (data, companie, val, tva, total))
    except:
        return []

async def insert_intrare_many(entries: list[tuple[str, str, float, float, float]]) -> list[tuple]:
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

        with Database('cashflow.db') as db:
            for entry in entries:
                res = await db.query_async("""
                INSERT INTO Intrari (DataIntrare, Companie, Valoare, TVA, Total)
                VALUES (?, ?, ?, ?, ?);
                """, entry)

                entries_added.append(res)

        return entries_added
    except Exception as e:
        print(e)
        return []


async def insert_iesire(data: str, companie: str, val: float, tva: float, total: float) -> list[tuple]:

    """
    Insert a new entry into the Iesiri table
    :param data: Date of the entry
    :param companie: Company name
    :param val: Value
    :param tva: TVA
    :param total: Total
    :return: Boolean value indicating if the entry was inserted or not
    """

    try:
        with Database('cashflow.db') as db:
            return await db.query_async("""
            INSERT INTO Iesiri (DataIesire, Companie, Valoare, TVA, Total)
            VALUES (?, ?, ?, ?, ?);
            """, (data, companie, val, tva, total))
    except:
        return []

async def insert_iesire_many(data: list[str], companie: list[str], val: list[float], tva: list[float], total: list[float]) -> list[list[tuple]]:
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

        with Database('cashflow.db') as db:
            for entry in entries:
                res = await db.query_async("""
                INSERT INTO Iesiri (DataIntrare, Companie, Valoare, TVA, Total)
                VALUES (?, ?, ?, ?, ?);
                """, entry)

                entries_added.append(res)

        return entries_added
    except Exception as e:
        print(e)
        return []


#   Read operations     -   ASYNC
async def get_intrari(luni: list[str] | int) -> list[list[tuple]]:

    """
    Get all the entries from the Intrari table
    :param luna: Lunile dorite (daca e -1, se vor returna toate intrarile)
    :return: List of entries
    """

    try:
        with Database('cashflow.db') as db:
            if luni == -1:
                return await db.query_async("""
                SELECT * FROM Intrari;
                """)
            else:
                return await db.query_async("""
                SELECT * FROM Intrari WHERE strftime('%m', DataIntrare) IN (""" + ','.join('?'*len(luni)) + ')', luni)

    except Exception as e:
        print(e)
        return []

async def get_iesiri(luni: list[int] | int) -> list[list[tuple]]:

    """
    Get all the entries from the Iesiri table
    :param luna: Lunile dorite (daca e -1, se vor returna toate intrarile)
    :return: List of entries
    """

    try:
        with Database('cashflow.db') as db:
            if luni == -1:
                return await db.query_async("""
                SELECT * FROM Iesiri;
                """)
            else:
                return await db.query_async("""
                SELECT * FROM Intrari WHERE strftime('%m', DataIntrare) IN (
                """ + ','.join('?'*len(luni)) + ')', luni)

    except:
        return []

async def get_total_difference(companii: list[str] | int) -> list[list[tuple]]:

    """
    Get the total difference of the entries from the joined tables
    :param companii: Companiile dorite (daca e -1, se vor returna toate intrarile)
    :return: List of entries
    """

    try:
        with Database('cashflow.db') as db:
            if companii == -1:
                return await db.query_async("""
                SELECT SUM(Intrari.Total) - SUM(Iesiri.Total) AS TotalDifference, Intrari.Companie
                FROM Intrari
                JOIN Iesiri ON Intrari.Companie = Iesiri.Companie;
                """)
            else:
                return await db.query_async("""
                SELECT SUM(Intrari.Total) - SUM(Iesiri.Total) AS TotalDifference, Intrari.Companie
                FROM Intrari
                JOIN Iesiri ON Intrari.Companie = Iesiri.Companie
                WHERE Intrari.Companie IN (?);
                """, (companii,))

    except:
        return []


#   Update operations   -   ASYNC
async def update_intrari(data: str, companie: str, values: tuple) -> list[list[tuple]]:
    """
    Update an entry from the Intrari table
    :param data: Data dorita pentru update (daca e ALL, se vor updata toate intrarile)
    :param companie: Compania dorita pentru update (daca e ALL, se vor updata toate intrarile)
    :param values: Valori noi (In ordinea: DataIntrare, Companie, Valoare, TVA, Total)
    :return:
    """

    try:
        with Database('cashflow.db') as db:

            # Build the string for the query
            query = f"UPDATE Intrari SET Valoare = ?, TVA = ?, Total = ?"

            # Add the WHERE clause if needed
            if data != "ALL" and companie != "ALL":
                query += " WHERE DataIntrare = ? AND Companie = ?"
            elif data != "ALL":
                query += " WHERE DataIntrare = ?"
            elif companie != "ALL":
                query += " WHERE Companie = ?"

            return await db.query_async(query, (*values, data, companie))

    except:
        return []

async def update_iesiri(data: str, companie: str, values: tuple) -> list[list[tuple]]:
    """
    Update an entry from the Iesiri table
    :param data: Data dorita pentru update (daca e ALL, se vor updata toate intrarile)
    :param companie: Compania dorita pentru update (daca e ALL, se vor updata toate intrarile)
    :param values: Valori noi (In ordinea: DataIesire, Companie, Valoare, TVA, Total)
    :return:
    """

    try:
        with Database('cashflow.db') as db:

            # Build the string for the query
            query = f"UPDATE Iesiri SET Valoare = ?, TVA = ?, Total = ?"

            # Add the WHERE clause if needed
            if data != "ALL" and companie != "ALL":
                query += " WHERE DataIesire = ? AND Companie = ?"
            elif data != "ALL":
                query += " WHERE DataIesire = ?"
            elif companie != "ALL":
                query += " WHERE Companie = ?"

            return await db.query_async(query, (*values, data, companie))

    except:
        return []


#   Delete operations
async def delete_intrari(data: str, companie: str) -> list[list[tuple]]:
    """
    Delete an entry from the Intrari table
    :param data: Data dorita pentru delete (daca e ALL, se vor sterge toate intrarile)
    :param companie: Compania dorita pentru delete (daca e ALL, se vor sterge toate intrarile)
    :return:
    """

    try:
        with Database('cashflow.db') as db:

            # Build the string for the query
            query = "DELETE FROM Intrari"

            # Add the WHERE clause if needed
            if data != "ALL" and companie != "ALL":
                query += " WHERE DataIntrare = ? AND Companie = ?"
            elif data != "ALL":
                query += " WHERE DataIntrare = ?"
            elif companie != "ALL":
                query += " WHERE Companie = ?"

            return await db.query_async(query, (data, companie))

    except:
        return []

async def delete_iesiri(data: str, companie: str) -> list[list[tuple]]:
    """
    Delete an entry from the Iesiri table
    :param data: Data dorita pentru delete (daca e ALL, se vor sterge toate intrarile)
    :param companie: Compania dorita pentru delete (daca e ALL, se vor sterge toate intrarile)
    :return:
    """

    try:
        with Database('cashflow.db') as db:

            # Build the string for the query
            query = "DELETE FROM Iesiri"

            # Add the WHERE clause if needed
            if data != "ALL" and companie != "ALL":
                query += " WHERE DataIesire = ? AND Companie = ?"
            elif data != "ALL":
                query += " WHERE DataIesire = ?"
            elif companie != "ALL":
                query += " WHERE Companie = ?"

            return await db.query_async(query, (data, companie))

    except:
        return []



