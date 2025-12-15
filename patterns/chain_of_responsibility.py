import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Dict

class Handler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass
    
    @abstractmethod
    async def handle(self, request: Dict) -> Optional[Dict]:
        pass

class AbstractHandler(Handler):
    _next_handler: Handler = None
    
    def set_next(self, handler: Handler):
        self._next_handler = handler
        return handler
    
    async def handle(self, request: Dict) -> Optional[Dict]:
        if self._next_handler:
            return await self._next_handler.handle(request)
        return None

class AuthenticationHandler(AbstractHandler):
    async def handle(self, request: Dict) -> Optional[Dict]:
        if not request.get("token"):
            return {"error": "Требуется аутентификация", "handler": "Authentication"}
        request["user_id"] = 123
        return await super().handle(request)

class ValidationHandler(AbstractHandler):
    async def handle(self, request: Dict) -> Optional[Dict]:
        if not request.get("data"):
            return {"error": "Отсутствуют данные", "handler": "Validation"}
        request["validated"] = True
        return await super().handle(request)

class AuthorizationHandler(AbstractHandler):
    async def handle(self, request: Dict) -> Optional[Dict]:
        if request.get("user_role") != "admin":
            return {"error": "Недостаточно прав", "handler": "Authorization"}
        request["authorized"] = True
        return await super().handle(request)

class ProcessingHandler(AbstractHandler):
    async def handle(self, request: Dict) -> Optional[Dict]:
        await asyncio.sleep(0.2)
        return {
            "status": "success",
            "message": "Запрос успешно обработан",
            "data": request.get("data", {}),
            "user_id": request.get("user_id")
        }

class RequestProcessor:
    def __init__(self):
        self.handler = AuthenticationHandler()
        validation = ValidationHandler()
        authorization = AuthorizationHandler()
        processing = ProcessingHandler()
        
        self.handler.set_next(validation)
        validation.set_next(authorization)
        authorization.set_next(processing)
    
    async def process_request(self, request: Dict) -> Dict:
        result = await self.handler.handle(request)
        return result or {"error": "Не удалось обработать запрос"}