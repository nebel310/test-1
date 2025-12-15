import asyncio
from abc import ABC, abstractmethod
from enum import Enum

class NotificationType(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"

class Notification(ABC):
    @abstractmethod
    async def send(self, message: str) -> dict:
        pass

class EmailNotification(Notification):
    async def send(self, message: str) -> dict:
        print(f"Отправляем email: {message}")
        await asyncio.sleep(0.3)
        return {
            "type": "email",
            "status": "sent",
            "message": message,
            "details": "Письмо отправлено на email пользователя"
        }

class SMSNotification(Notification):
    async def send(self, message: str) -> dict:
        print(f"Отправляем SMS: {message}")
        await asyncio.sleep(0.2)
        return {
            "type": "sms",
            "status": "sent",
            "message": message,
            "details": "SMS отправлено на номер телефона"
        }

class PushNotification(Notification):
    async def send(self, message: str) -> dict:
        print(f"Отправляем push-уведомление: {message}")
        await asyncio.sleep(0.1)
        return {
            "type": "push",
            "status": "sent",
            "message": message,
            "details": "Push-уведомление отправлено на устройство"
        }

class NotificationFactory:
    @staticmethod
    def create_notification(notification_type: NotificationType) -> Notification:
        if notification_type == NotificationType.EMAIL:
            return EmailNotification()
        elif notification_type == NotificationType.SMS:
            return SMSNotification()
        elif notification_type == NotificationType.PUSH:
            return PushNotification()
        else:
            raise ValueError(f"Неизвестный тип уведомления: {notification_type}")

async def test_factory_method():
    factory = NotificationFactory()
    
    email_notification = factory.create_notification(NotificationType.EMAIL)
    sms_notification = factory.create_notification(NotificationType.SMS)
    push_notification = factory.create_notification(NotificationType.PUSH)
    
    results = []
    for notification in [email_notification, sms_notification, push_notification]:
        result = await notification.send("Важное сообщение!")
        results.append(result)
    
    return results