import cashflow_api as cAPI
import config_api as cfgAPI

import asyncio

cAPI.create_cashflow_table()

async def main():
    # print('a')
    # liste = await cAPI.insert_intrare_many(
    #     entries=[
    #         [(1, 2, 2021), 'Company 1', 100, 19, 119],
    #         [(1, 2, 2021), 'Company 2', 200, 19, 238],
    #     ]
    # )
    # await cAPI.insert_iesire_many(
    #     entries=[
    #         [(1, 2, 2021), 'Company 2', 120, 19, 119],
    #         [(1, 2, 2021), 'Company 3', 24, 19, 238],
    #     ]
    # )
    # print('b')
    print(await cAPI.get_recent_operations(limit=5))

if __name__ == "__main__":
    asyncio.run(main())