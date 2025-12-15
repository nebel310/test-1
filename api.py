from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any
from patterns.strategy import PaymentStrategyFactory, PaymentContext
from patterns.chain_of_responsibility import RequestProcessor
from patterns.iterator import TaskCollection, PaginatedResults
from patterns.proxy import RealDatabase, DatabaseProxy
from patterns.bridge import (
        EmailPlatform, SMSPlatform, PushPlatform,
        SimpleNotification, UrgentNotification, ScheduledNotification
    )
from patterns.adapter import LegacyXMLService, XMLToJSONAdapter, ModernClient, ThirdPartyAPIAdapter

router = APIRouter()

class ChainRequest(BaseModel):
    token: str = "test-token-123"
    data: Dict[str, Any] = {"action": "test", "value": 42}
    user_role: str = "admin"

@router.get("/health")
async def health_check():
    return {"status": "ok", "patterns": 6}

@router.get("/strategy/test/{method}")
async def test_strategy(method: str, amount: float = 100.0):
    
    try:
        strategy = PaymentStrategyFactory.create_strategy(method)
        context = PaymentContext(strategy)
        result = await context.execute_payment(amount)
        
        return {
            "pattern": "Strategy",
            "result": result
        }
    except ValueError as e:
        return {"error": str(e), "available_methods": ["credit_card", "paypal", "crypto"]}

@router.post("/chain/test")
async def test_chain(chain_request: ChainRequest = None):
    
    if chain_request is None:
        chain_request = ChainRequest()
    
    processor = RequestProcessor()
    result = await processor.process_request(chain_request.dict())
    
    return {
        "pattern": "Chain of Responsibility",
        "result": result
    }

@router.get("/iterator/test")
async def test_iterator():
    
    collection = TaskCollection()
    collection.add_task("Анализ требований")
    collection.add_task("Проектирование")
    collection.add_task("Разработка")
    collection.add_task("Тестирование")
    collection.add_task("Деплой")
    
    iterator = await collection.create_iterator()
    
    tasks = []
    while await iterator.has_next():
        task = await iterator.next()
        tasks.append(task)
    
    results = [f"Результат {i}" for i in range(1, 11)]
    paginated = PaginatedResults(results, page_size=3)
    
    pages = []
    async for page in paginated:
        pages.append(page)
    
    return {
        "pattern": "Iterator",
        "classic_iterator": tasks,
        "async_iterator": pages
    }

@router.get("/proxy/test")
async def test_proxy():

    real_db = RealDatabase()
    proxy = DatabaseProxy(real_db)
    
    try:
        await proxy.connect()
        
        results = []
        for i in range(3):
            result = await proxy.execute_query(f"SELECT * FROM users WHERE id = {i}")
            results.append(result)
        
        cached_result = await proxy.execute_query("SELECT * FROM users WHERE id = 0")
        results.append({"cached": cached_result})
        
        await proxy.disconnect()
        
        return {
            "pattern": "Proxy",
            "results": results
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/bridge/test")
async def test_bridge():
    
    email_platform = EmailPlatform()
    sms_platform = SMSPlatform()
    push_platform = PushPlatform()
    
    notifications = [
        SimpleNotification(email_platform, "Добро пожаловать в нашу систему!"),
        UrgentNotification(sms_platform, "Необходимо подтвердить действие", 1),
        ScheduledNotification(push_platform, "Напоминание о встрече", 1),
        SimpleNotification(push_platform, "Новое сообщение в чате")
    ]
    
    results = []
    for notification in notifications:
        result = await notification.send("user@example.com")
        results.append(result)
    
    return {
        "pattern": "Bridge",
        "results": results
    }

@router.get("/adapter/test/{city}")
async def test_adapter(city: str = "Moscow"):
    
    legacy_service = LegacyXMLService()
    adapter = XMLToJSONAdapter(legacy_service)
    client = ModernClient(adapter)
    
    adapter_result = await client.process_user_data()
    
    weather_adapter = ThirdPartyAPIAdapter()
    weather_result = await weather_adapter.get_unified_weather(city)
    
    return {
        "pattern": "Adapter",
        "xml_to_json": adapter_result,
        "weather_api": weather_result
    }