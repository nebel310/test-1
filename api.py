from fastapi import APIRouter
from patterns.singleton import DatabaseConnection
from patterns.factory_method import NotificationFactory, NotificationType
from patterns.abstract_factory import (
        OSType, UIFactoryProducer, test_abstract_factory as test_af
    )
from patterns.builder import test_builder as test_builder_func

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

@router.get("/factory-method/test")
async def test_factory_method():
    """
    Тестирование паттерна Factory Method.
    Создает разные типы уведомлений через фабрику.
    """
    
    factory = NotificationFactory()
    
    notifications = []
    for notification_type in NotificationType:
        notification = factory.create_notification(notification_type)
        result = await notification.send(f"Тестовое сообщение через {notification_type.value}")
        notifications.append(result)
    
    return {
        "pattern": "Factory Method",
        "notifications": notifications,
        "description": "Фабричный метод создает объекты, не указывая конкретных классов"
    }

@router.get("/abstract-factory/test/{os_type}")
async def test_abstract_factory(os_type: str):
    """
    Тестирование паттерна Abstract Factory.
    Создает набор UI-компонентов для указанной ОС.
    """
    
    try:
        os_enum = OSType(os_type.lower())
    except ValueError:
        return {
            "error": f"Неизвестный тип ОС: {os_type}",
            "available_os": [os.value for os in OSType]
        }
    
    result = await test_af(os_enum)
    
    return {
        "pattern": "Abstract Factory",
        "result": result,
        "description": "Абстрактная фабрика создает семейства связанных объектов"
    }

@router.get("/builder/test")
async def test_builder():
    """
    Тестирование паттерна Builder.
    Создает различные HTTP запросы с разными конфигурациями.
    """
    
    results = await test_builder_func()
    
    return {
        "pattern": "Builder",
        "results": results,
        "description": "Builder позволяет создавать сложные объекты пошагово, скрывая детали конструирования"
    }