import asyncio
import sys
sys.path.insert(0, '.')

async def test():
    from bot.core.database import get_pool
    
    pool = await get_pool()
    async with pool.acquire() as conn:
        result = await conn.fetchval("SELECT COUNT(*) FROM companies")
        print(f"✅ Database connected! Companies count: {result}")
        
    await pool.close()

asyncio.run(test())
