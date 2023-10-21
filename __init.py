import backend.api.cashflow_api as cAPI
import backend.api.config_api as cfgAPI

import asyncio

async def main():
    # Create the necessary tables
    await cAPI.create_cashflow_table()

    # Insert some data
    await cAPI.insert_intrare_many(
        entries=[
            [(20, 10, 2023), 'Company 1', 100, 19, 119],
            [(19, 10, 2023), 'Company 2', 200, 19, 238],
        ]
    )
    await cAPI.insert_iesire_many(
        entries=[
            [(20, 10, 2023), 'Company 2', 120, 19, 119],
            [(19, 10, 2023), 'Company 3', 24, 19, 238],
        ]
    )

    # Get the data
    print(await cAPI.get_intrari())
    print(await cAPI.get_date_lunare())

if __name__ == "__main__":
    asyncio.run(main())