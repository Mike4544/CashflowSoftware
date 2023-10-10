from backend.database.sql_connection import Database

"""
This file contains the API for the cashflow database

The database contains three tables:
    - Intrari
    - Iesiri
    - Config

The Intrari table contains the following columns:
    -------------------------------------------------------------------------
    |   ID  |   DataIntrare |   Companie    |   Valoare |   TVA |   Total   |
    -------------------------------------------------------------------------
    |   INT |   DATE        |   VARCHAR     |   FLOAT   | FLOAT |   FLOAT   |


The Iesiri table contains the following columns:
    -------------------------------------------------------------------------
    |   ID  |   DataIesire  |   Companie    |   Valoare |   TVA |   Total   |
    -------------------------------------------------------------------------
    |   INT |   DATE        |   VARCHAR     |   FLOAT   | FLOAT |   FLOAT   |


The Config table contains the following columns:
    ---------------------------------------------
    |   ID  |   Parola_Useri    |   Parola_Admin |
    ---------------------------------------------
    |   INT |   VARCHAR         |   VARCHAR      |


:author:    Mihai Tira
"""

#   Create the table if it doesn't exist
def create_config_table() -> bool:
    """
    Create the config table if it doesn't exist
    :return: Boolean value indicating if the table was created or not
    """

    try:
        with Database('cashflow.db') as db:
            db.execute("""
            CREATE TABLE IF NOT EXISTS Config (
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Parola_Useri VARCHAR(255),
                Parola_Admin VARCHAR(255)
            );
            """)

            return True
    except Exception as e:
        print(e)
        return False

#   Update the config table
async def update_config_table(parola_useri: str, parola_admin: str) -> list[tuple]:
    """
    Update the config table
    :param parola_useri: The password for the user
    :param parola_admin: The password for the admin
    :return: Boolean value indicating if the table was updated or not
    """

    try:
        with Database('cashflow.db') as db:
            return await db.query_async("""
            UPDATE Config
            SET Parola_Useri = ?, Parola_Admin = ?
            WHERE ID = 1;
            """, (parola_useri, parola_admin))

    except Exception as e:
        print(e)
        return []
