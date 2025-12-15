from fastapi import APIRouter
from patterns.singleton import DatabaseConnection

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/singleton/test")
async def test_singleton():
    """
    Тестирование паттерна Singleton.
    Показывает, что всегда возвращается один и тот же объект.
    """
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    connection1 = await db1.connect()
    connection2 = await db2.connect()
    
    return {
        "is_same_object": db1 is db2,
        "connection_id_1": str(connection1),
        "connection_id_2": str(connection2),
        "message": "Singleton гарантирует, что это один и тот же объект"
    }