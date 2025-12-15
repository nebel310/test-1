import asyncio
from abc import ABC, abstractmethod

class NotificationPlatform(ABC):
    @abstractmethod
    async def send(self, message: str, recipient: str):
        pass

class EmailPlatform(NotificationPlatform):
    async def send(self, message: str, recipient: str):
        await asyncio.sleep(0.3)
        return {
            "platform": "Email",
            "recipient": recipient,
            "status": "sent",
            "message": message[:50] + "..."
        }

class SMSPlatform(NotificationPlatform):
    async def send(self, message: str, recipient: str):
        await asyncio.sleep(0.2)
        return {
            "platform": "SMS",
            "recipient": recipient,
            "status": "sent",
            "message": message[:160]
        }

class PushPlatform(NotificationPlatform):
    async def send(self, message: str, recipient: str):
        await asyncio.sleep(0.1)
        return {
            "platform": "Push",
            "recipient": recipient,
            "status": "sent",
            "message": message[:100]
        }

class Notification(ABC):
    def __init__(self, platform: NotificationPlatform):
        self._platform = platform
    
    @abstractmethod
    async def send(self, recipient: str):
        pass

class SimpleNotification(Notification):
    def __init__(self, platform: NotificationPlatform, message: str):
        super().__init__(platform)
        self.message = message
    
    async def send(self, recipient: str):
        return await self._platform.send(self.message, recipient)

class UrgentNotification(Notification):
    def __init__(self, platform: NotificationPlatform, message: str, priority: int):
        super().__init__(platform)
        self.message = f"[URGENT {priority}] {message}"
    
    async def send(self, recipient: str):
        result = await self._platform.send(self.message, recipient)
        result["priority"] = "high"
        return result

class ScheduledNotification(Notification):
    def __init__(self, platform: NotificationPlatform, message: str, delay_seconds: int):
        super().__init__(platform)
        self.message = message
        self.delay_seconds = delay_seconds
    
    async def send(self, recipient: str):
        await asyncio.sleep(self.delay_seconds)
        return await self._platform.send(self.message, recipient)