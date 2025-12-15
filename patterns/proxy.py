import asyncio
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    async def connect(self):
        pass
    
    @abstractmethod
    async def execute_query(self, query: str):
        pass
    
    @abstractmethod
    async def disconnect(self):
        pass

class RealDatabase(Database):
    async def connect(self):
        await asyncio.sleep(1.0)
    
    async def execute_query(self, query: str):
        await asyncio.sleep(0.5)
        return {"result": f"Данные для запроса: {query}", "rows": 100}
    
    async def disconnect(self):
        await asyncio.sleep(0.3)

class DatabaseProxy(Database):
    def __init__(self, real_database: RealDatabase):
        self._real_database = real_database
        self._cache = {}
        self._connection_count = 0
        self._max_connections = 2
    
    async def connect(self):
        if self._connection_count >= self._max_connections:
            raise Exception("Достигнуто максимальное количество подключений")
        
        self._connection_count += 1
        await self._real_database.connect()
    
    async def execute_query(self, query: str):
        if query in self._cache:
            return self._cache[query]
        
        if "DELETE" in query.upper() or "DROP" in query.upper():
            raise Exception("Недостаточно прав для выполнения этого запроса")
        
        result = await self._real_database.execute_query(query)
        self._cache[query] = result
        
        return result
    
    async def disconnect(self):
        if self._connection_count > 0:
            self._connection_count -= 1
            await self._real_database.disconnect()
    
    def clear_cache(self):
        self._cache.clear()