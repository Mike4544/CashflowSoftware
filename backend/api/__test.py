import cashflow_api as cAPI
import config_api as cfgAPI

import asyncio

cAPI.create_cashflow_table()

async def main():
    # liste = await cAPI.insert_intrare_many(
    #     entries=[
    #         ('2021-asd-01', 'Company 1', 100, 19, 119),
    #         ('2021-04-02', 'Company 2', 200, 19, 238),
    #     ]
    # )
    print(await cAPI.get_intrari(['02']))

if __name__ == "__main__":
    asyncio.run(main())