import asyncio
import asyncpg


async def main():
    connection = await asyncpg.connect(
        user="postgres",
        password="lenny_dev_password",
        host="127.0.0.1",
        port=5433,
        database="lenny_assistant",
    )

    print("PYTHON POSTGRES CONNECTION SUCCESS")

    await connection.close()


asyncio.run(main())