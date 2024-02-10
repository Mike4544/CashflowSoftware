import backend.api.cashflow_api as cAPI
import backend.api.config_api as cfgAPI

import asyncio

async def main():
    # Create the necessary tables
    await cAPI.create_cashflow_table()


if __name__ == "__main__":
    asyncio.run(main())