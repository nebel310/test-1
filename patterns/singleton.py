import asyncio

class DatabaseConnection:
    """
    Singleton для управления подключением к базе данных.
    Гарантирует только одно соединение на всё приложение.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance
    
    async def connect(self):
        """Асинхронное подключение к БД (имитация)"""
        if self._connection is None:
            print("Устанавливаем подключение к базе данных...")
            await asyncio.sleep(0.5)
            self._connection = "PostgreSQL Connection"
            print("Подключение установлено!")
        return self._connection
    
    async def disconnect(self):
        """Асинхронное отключение от БД"""
        if self._connection:
            print("Закрываем подключение к базе данных...")
            await asyncio.sleep(0.2)
            self._connection = None
            print("Подключение закрыто!")


async def test_singleton():
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"Один и тот же объект? {db1 is db2}")
    
    conn1 = await db1.connect()
    conn2 = await db2.connect()
    
    print(f"Подключение из db1: {conn1}")
    print(f"Подключение из db2: {conn2}")