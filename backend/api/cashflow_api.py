from backend.database.sql_connection import Database

"""
This file contains the API for the cashflow database

The database contains three tables:
    - Intrari
    - Iesiri
    - DateLunare
    - ConturiBancare
    - Salariati
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

from pypika import Query, Table, Field, Order, Case, SQLLiteQuery
from datetime import datetime

DB_PATH = 'backend/database/cashflow.db'


def create_db_connection():
    return Database(DB_PATH)

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
                URGENT BOOLEAN DEFAULT FALSE,
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
                URGENT BOOLEAN DEFAULT FALSE,
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

            #   Tabela angajati
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS Salariati (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    Nume VARCHAR(255),
                    Companie VARCHAR(255),
                    NrCTR VARCHAR(255),
                    Functie VARCHAR(255),
                    CNP VARCHAR(255),
                    CI VARCHAR(255),
                    Valabilitate VARCHAR(255),
                    FisaAptitudini VARCHAR(255),
                    Telefon VARCHAR(255),
                    IBAN VARCHAR(255)
                );
                """
            )
            #   Tabela config cont bancar
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS Salarii (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    Luna INTEGER DEFAULT 1,
                    An INTEGER DEFAULT 1970,
                    IdAngajat INTEGER,
                    Companie VARCHAR(255),
                    Salariu INTEGER DEFAULT 0,
                    Bonus INTEGER DEFAULT 0
                );
                """
            )

            db.execute(
                """
                CREATE TABLE IF NOT EXISTS Inventar (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    Nume VARCHAR(255),
                    Cantitate INTEGER DEFAULT 0,
                    Valoare DECIMAL(10, 2) DEFAULT 0,
                    IdAngajat INTEGER
                );
                """
            )

            db.execute(
                """
                CREATE TABLE IF NOT EXISTS Flota (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    Masina VARCHAR(255),
                    NrInmatriculare VARCHAR(255),
                    GPS VARCHAR(255),
                    SerieSasiu VARCHAR(255),
                    Combustibil VARCHAR(255),
                    ITP VARCHAR(255),
                    RCA VARCHAR(255),
                    Rovinieta VARCHAR(255),
                    CopieConforma VARCHAR(255),
                    Sofer VARCHAR(255)
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
        isUrgent: bool = False,
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
                'URGENT', 'Zi', 'Luna', 'An', 'Companie', 'Valoare', 'TVA', 'Total'
            ).insert(
                (isUrgent, *data, companie, val, tva, total)
            )

            return await db_connection.query_async(query.get_sql())


        with Database(DB_PATH) as db:
            query = Query.into(
                'Intrari'
            ).columns(
                'URGENT', 'Zi', 'Luna', 'An', 'Companie', 'Valoare', 'TVA', 'Total'
            ).insert(
                (isUrgent, *data, companie, val, tva, total)
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
                    float,
                    bool]
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

        else :
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
        isUrgent: bool = False,
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
                'URGENT', 'Zi', 'Luna', 'An', 'Companie', 'Valoare', 'TVA', 'Total'
            ).insert(
                (isUrgent, *data, companie, val, tva, total)
            )

            return await db_connection.query_async(query.get_sql())

        with Database(DB_PATH) as db:

            query = Query.into(
                'Iesiri'
            ).columns(
                'URGENT', 'Zi', 'Luna', 'An', 'Companie', 'Valoare', 'TVA', 'Total'
            ).insert(
                (isUrgent, *data, companie, val, tva, total)
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
                        float,
                        bool]
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

async def insert_angajat(
        nume: str,
        companii: list[str],
        nrCtr: str,
        functie: str,
        cnp: str,
        ci: str,
        valabilitate: str,
        fisaAptitudini: str,
        telefon: str,
        iban: str,
        db_connection: Database = None
):
    
    table = Table("Salariati")
    
    query = Query.into(table).columns("Nume", "Companie", "NrCTR", "Functie", "CNP", "CI", "Valabilitate", "FisaAptitudini", "Telefon", "IBAN")
    for companie in companii:
        query = query.insert(
            nume, companie, nrCtr, functie, cnp, ci, valabilitate, fisaAptitudini, telefon, iban
        )

        # For every employee, insert a salary for every company
        table_salarii = Table("Salarii")
        query_salarii = Query.into(table_salarii).columns(
            "Luna", "An", "IdAngajat", "Companie"
        )

        if db_connection:
            await db_connection.query_async(query_salarii.get_sql())
        else:
            with Database(DB_PATH) as db:
                await db.query_async(query_salarii.get_sql())

    #   print("QUERY: ", query.get_sql())

    try:
        if db_connection:
            return await db_connection.query_async(query.get_sql()), db_connection.lastrowid()
        
        with Database(DB_PATH) as db:
            return await db.query_async(query.get_sql()), db.lastrowid()
    
    except Exception as e:
        print(e)
        return []
    
async def insert_angajat_many(
        angajati: list[
            tuple[
                str, list[str], str, str, str, str, str, str, str, str
                ]
            ],
        db_connection: Database = None
) -> bool:
    
    try:
        if db_connection:
            for angajat in angajati:
                print(angajat)
                await insert_angajat(
                    *angajat,
                    db_connection=db_connection
                )
            return True

        else:
            with Database(name=DB_PATH) as db:
                for angajat in angajati:
                    #print(*angajat)
                    await insert_angajat(
                        *angajat,
                        db_connection=db
                    )
            return True
        
    except Exception as e:
        print(e)
        return False
    

async def insert_salariu(
        luna: int,
        an: int,
        id_angajat: int,
        companie: str,
        valoare: float,
        bonus: float,
        db_connection: Database = None
):
    
    table = Table("Salarii")
    
    query = Query.into(table).columns(
        "Luna", "An", "IdAngajat", "Companie", "Salariu", "Bonus"
    ).insert(
        luna, an, id_angajat, companie, valoare, bonus
    )

    try:
        if db_connection:
            return await db_connection.query_async(query.get_sql())
        
        with Database(DB_PATH) as db:
            return await db.query_async(query.get_sql())
    
    except Exception as e:
        print(e)
        return []

async def insert_inventar(
        nume: str,
        cantitate: int,
        valoare: float,
        id_angajat: int,
        db_connection: Database = None
):

        table = Table("Inventar")

        query = Query.into(table).columns(
            "Nume", "Cantitate", "Valoare", "IdAngajat"
        ).insert(
            nume, cantitate, valoare, id_angajat
        )

        try:
            if db_connection:
                return await db_connection.query_async(query.get_sql())

            with Database(DB_PATH) as db:
                return await db.query_async(query.get_sql())

        except Exception as e:
            print(e)
            return []

async def insert_inventar_many(
        inventar: list[
            tuple[
                str, int, float, int
                ]
            ],
        db_connection: Database = None
) -> bool:

    try:
        if db_connection:
            for item in inventar:
                await insert_inventar(
                    *item,
                    db_connection=db_connection
                )
            return True

        else:
            with Database(name=DB_PATH) as db:
                for item in inventar:
                    await insert_inventar(
                        *item,
                        db_connection=db
                    )
            return True

    except Exception as e:
        print(e)
        return False


async def insert_salariu_many(
        salarii: list[
            tuple[
                tuple, int, str, float, float
            ]
        ],
        db_connection: Database = None
) -> bool:
    
    try:
        if db_connection:
            for salariu in salarii:
                await insert_salariu(
                    *salariu,
                    db_connection=db_connection
                )
            return True

        else:
            with Database(name=DB_PATH) as db:
                for salariu in salarii:
                    await insert_salariu(
                        *salariu,
                        db_connection=db_connection
                    )
            return True
        
    except Exception as e:
        print(e)
        return False


async def insert_flota(
        masina: str,
        nrInmatriculare: str,
        gps: str,
        serieSasiu: str,
        combustibil: str,
        itp: str,
        rca: str,
        rovinieta: str,
        copieConforma: str,
        sofer: str,
        db_connection: Database = None
):

        table = Table("Flota")

        query = Query.into(table).columns(
            "Masina", "NrInmatriculare", "GPS", "SerieSasiu", "Combustibil", "ITP", "RCA", "Rovinieta", "CopieConforma", "Sofer"
        ).insert(
            masina, nrInmatriculare, gps, serieSasiu, combustibil, itp, rca, rovinieta, copieConforma, sofer
        )

        try:
            if db_connection:
                return await db_connection.query_async(query.get_sql()), db_connection.lastrowid()

            with Database(DB_PATH) as db:
                return await db.query_async(query.get_sql()), db.lastrowid()

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
        only_urgent: bool = False,
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

        if only_urgent:
            query = query.where(
                table.URGENT == True
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
        only_urgent: bool = False,
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

        if only_urgent:
            query = query.where(
                table.URGENT == True
            )


        if db_connection:
            entries = await db_connection.query_async(query.get_sql())


        with Database(DB_PATH) as db:
            entries = await db.query_async(query.get_sql())

        # Get the sum of the salaries
        salarii = await get_salarii(
            an=an or datetime.now().year,
            luna=luna or datetime.now().month,
        )

        # Get the sum of the salaries
        sum = 0;
        for salariu in salarii:
            sum += salariu[5] + salariu[6]

        # In a 10-a a lunii, add 1/3 of the salaries to the total
        third = sum / 3
        entries.append(
            (-99, 'Iesire', True,  10, luna or datetime.now().month, an or datetime.now().year, 'Salarii', third, 0,
             sum / 3)
        )

        # In a 25-a a lunii, add 2/3 of the salaries to the total
        entries.append(
            (-99, 'Iesire', True, 25, luna or datetime.now().month, an or datetime.now().year, 'Salarii', 2 * third, 0,
             sum * 2 / 3)
        )

        return entries

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
    query = Query.from_(intrari).select('*').where(
        (intrari.Luna == datetime.now().month) & (intrari.An == datetime.now().year)
    ) + Query.from_(iesiri).select('*').where(
        (iesiri.Luna == datetime.now().month) & (iesiri.An == datetime.now().year)
    )
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
    

async def get_angajat(
        id,
        db_connection: Database = None
) -> list[tuple]:

        try:
            table = Table('Salariati')
            query = Query.from_(table).select('*').where(
                table.ID == id
            )

            if db_connection:
                return await db_connection.query_async(query.get_sql())

            with Database(DB_PATH) as db:
                return await db.query_async(query.get_sql())

        except Exception as e:
            print(e)
            return []

async def get_angajati(
        db_connection: Database = None
) -> list[tuple]:
    
    db = db_connection or Database(DB_PATH)

    table_salariati = Table("Salariati")
    query = Query.from_(
        table_salariati
    ).select("*")

    try:
        return await db.query_async(query.get_sql())
    except Exception as e:
        print(e)
        return []
    
    
async def get_salarii(
        an: int = None,
        luna = None,
        angajati: list[int] = None,
        companii: list[str] = None,
        db_connection: Database = None
):
    
    db = db_connection or Database(DB_PATH)


    table = Table("Salarii")
    query = Query.from_(table).select('*').where(
        table.An == (an or datetime.now().year)
    )

    if luna:
        query = query.where(
            table.Luna == luna
        )


    if angajati:
        query = query.where(
            table.IdAngajat.isin(angajati)
        )

    if companii:
        query = query.where(
            table.Companie.isin(companii)
        )

    try:
        return await db.query_async(query.get_sql())
    except Exception as e:
        print(e)
        return []

async def get_inventar(
        id_angajat: list[int] = None,
        db_connection: Database = None
):

    db = db_connection or Database(DB_PATH)

    table = Table("Inventar")
    query = Query.from_(table).select('*')

    if id_angajat:
        query = query.where(
            table.IdAngajat.isin(id_angajat)
        )

    try:
        return await db.query_async(query.get_sql())
    except Exception as e:
        print(e)
        return []

async def get_flota(
        db_connection: Database = None
):

        db = db_connection or Database(DB_PATH)

        table = Table("Flota")
        query = Query.from_(table).select('*')

        try:
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


async def update_angajat(
        id: int,
        data: dict[str, str, str, str, str, str, str, str, str],
        db_connection: Database = None
) -> list[tuple]:

        try:
            if db_connection:
                query = Query.update('Salariati')

                for name, value in data.items():
                    query = query.set(name, value)

                query = query.where(
                    Field('ID') == id
                )

                return await db_connection.query_async(query.get_sql())

            with Database(DB_PATH) as db:
                query = Query.update('Salariati')

                for name, value in data.items():
                    query = query.set(name, value)

                query = query.where(
                    Field('ID') == id
                )

                return await db.query_async(query.get_sql())

        except Exception as e:
            print(e)
            return []

async def update_salariu(
        luna: int,
        an: int,
        id_angajat: int,
        companie: str,
        valoare: float,
        bonus: float,
        db_connection: Database = None
) -> list[tuple]:

    try:
        if db_connection:
            query = Query.update('Salarii')\
                .set('Salariu', valoare)\
                .set('Bonus', bonus)\
                .where(
                    (Field('Luna') == luna) & (Field('An') == an) & (Field('IdAngajat') == id_angajat) & (Field('Companie') == companie)
                )

            return await db_connection.query_async(query.get_sql())

        with Database(DB_PATH) as db:
            query = Query.update('Salarii')\
                .set('Salariu', valoare)\
                .set('Bonus', bonus)\
                .where(
                    (Field('Luna') == luna) & (Field('An') == an) & (Field('IdAngajat') == id_angajat) & (Field('Companie') == companie)
                )

            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []

async def update_inventar(
        id_angajat: int,
        id_item: int,
        new_nume: str = None,
        new_cantitate: int = None,
        new_valoare: float = None,
        new_id_angajat: int = None,
        db_connection: Database = None
) -> list[tuple]:

    query = Query.update('Inventar')
    if new_nume:
        query = query.set('Nume', new_nume)
    if new_cantitate:
        query = query.set('Cantitate', new_cantitate)
    if new_valoare:
        query = query.set('Valoare', new_valoare)
    if new_id_angajat:
        query = query.set('IdAngajat', new_id_angajat)

    query = query.where(
        (Field('IdAngajat') == id_angajat) & (Field('ID') == id_item)
    )

    try:
        if db_connection:

            return await db_connection.query_async(query.get_sql())

        with Database(DB_PATH) as db:

            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []

async def update_flota(
        id: int,
        data: dict,
        db_connection: Database = None
):

            try:
                if db_connection:
                    query = Query.update('Flota')

                    for name, value in data.items():
                        query = query.set(name, value)

                    query = query.where(
                        Field('ID') == id
                    )

                    return await db_connection.query_async(query.get_sql())

                with Database(DB_PATH) as db:
                    query = Query.update('Flota')

                    for name, value in data.items():
                        query = query.set(name, value)

                    query = query.where(
                        Field('ID') == id
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


async def delete_angajat(id: int) -> list[list[tuple]]:

        try:
            with Database(DB_PATH) as db:

                table = Table('Salariati')
                query = Query.from_(table).where(
                    table.ID == id
                ).delete()

                # Delete all salaries for the employee
                table_salarii = Table("Salarii")
                query_salarii = Query.from_(table_salarii).where(
                    table_salarii.IdAngajat == id
                ).delete()

                return await db.query_async(query.get_sql()) and await db.query_async(query_salarii.get_sql())

        except Exception as e:
            print(e)
            return []

async def delete_salariu(
        luna: int,
        an: int,
        id_angajat: int,
        companie: str,
        db_connection: Database = None
) -> list[tuple]:

    try:
        if db_connection:
            query = Query.from_('Salarii').where(
                (Field('Luna') == luna) & (Field('An') == an) & (Field('IdAngajat') == id_angajat) & (Field('Companie') == companie)
            ).delete()

            return await db_connection.query_async(query.get_sql())

        with Database(DB_PATH) as db:
            query = Query.from_('Salarii').where(
                (Field('Luna') == luna) & (Field('An') == an) & (Field('IdAngajat') == id_angajat) & (Field('Companie') == companie)
            ).delete()

            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []

async def delete_inventar(
        id_item: int,
        id_angajat: int,
        db_connection: Database = None
):

    try:
        if db_connection:
            query = Query.from_('Inventar').where(
                (Field('ID') == id_item) & (Field('IdAngajat') == id_angajat)
            ).delete()

            return await db_connection.query_async(query.get_sql())

        with Database(DB_PATH) as db:
            query = Query.from_('Inventar').where(
                (Field('ID') == id_item) & (Field('IdAngajat') == id_angajat)
            ).delete()

            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []


async def delete_flota(
        id: int,
        db_connection: Database = None
):

    try:
        if db_connection:
            query = Query.from_('Flota').where(
                Field('ID') == id
            ).delete()

            return await db_connection.query_async(query.get_sql())

        with Database(DB_PATH) as db:
            query = Query.from_('Flota').where(
                Field('ID') == id_masina
            ).delete()

            return await db.query_async(query.get_sql())

    except Exception as e:
        print(e)
        return []