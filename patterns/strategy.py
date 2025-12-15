import asyncio
from abc import ABC, abstractmethod
from typing import Dict

class PaymentContext:
    def __init__(self, strategy=None):
        self._strategy = strategy
    
    def set_strategy(self, strategy):
        self._strategy = strategy
    
    async def execute_payment(self, amount: float) -> Dict:
        if self._strategy:
            return await self._strategy.process_payment(amount)
        raise ValueError("Стратегия не установлена")

class PaymentStrategy(ABC):
    @abstractmethod
    async def process_payment(self, amount: float) -> Dict:
        pass

class CreditCardPayment(PaymentStrategy):
    async def process_payment(self, amount: float) -> Dict:
        await asyncio.sleep(0.2)
        return {
            "method": "Credit Card",
            "amount": amount,
            "fee": amount * 0.02,
            "status": "completed",
            "message": f"Оплата картой на сумму {amount}$"
        }

class PayPalPayment(PaymentStrategy):
    async def process_payment(self, amount: float) -> Dict:
        await asyncio.sleep(0.3)
        return {
            "method": "PayPal",
            "amount": amount,
            "fee": amount * 0.01,
            "status": "completed",
            "message": f"Оплата PayPal на сумму {amount}$"
        }

class CryptoPayment(PaymentStrategy):
    async def process_payment(self, amount: float) -> Dict:
        await asyncio.sleep(0.5)
        return {
            "method": "Cryptocurrency",
            "amount": amount,
            "fee": amount * 0.005,
            "status": "completed",
            "message": f"Оплата криптовалютой на сумму {amount}$"
        }

class PaymentStrategyFactory:
    @staticmethod
    def create_strategy(method: str) -> PaymentStrategy:
        if method == "credit_card":
            return CreditCardPayment()
        elif method == "paypal":
            return PayPalPayment()
        elif method == "crypto":
            return CryptoPayment()
        else:
            raise ValueError(f"Неизвестный метод оплаты: {method}")