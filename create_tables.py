import asyncio
from app.database import engine, Base
from app.models import user, chat_room, message

async def build_database():
    print("Connecting directly to the live Railway database...")
    try:
        async with engine.begin() as connection:
            print("Syncing SQLAlchemy models with PostgreSQL...")
            await connection.run_sync(Base.metadata.create_all)
        print("🎉 SUCCESS! All tables (users, chat_rooms, messages) have been physically built!")
    except Exception as e:
        print(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(build_database())