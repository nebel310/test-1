from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional
from uuid import UUID

from domain.models import Order, Money, OrderStatus
from domain.exceptions import PaymentFailedException, OrderAlreadyPaidException, EmptyOrderException

class OrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    def save(self, order: Order):
        pass

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, order_id: UUID, money: Money) -> bool:
        pass

class PayOrderUseCase:
    def __init__(self, order_repository: OrderRepository, payment_gateway: PaymentGateway):
        self._order_repository = order_repository
        self._payment_gateway = payment_gateway

    def execute(self, order_id: UUID) -> dict:
        order = self._order_repository.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found")

        if order.status != OrderStatus.CREATED:
            raise OrderAlreadyPaidException("Order is already paid or cancelled")

        if not order.lines:
            raise EmptyOrderException("Cannot pay empty order")

        payment_success = self._payment_gateway.charge(order_id, order.total_amount)
        if not payment_success:
            raise PaymentFailedException("Payment processing failed")

        order.mark_as_paid()
        self._order_repository.save(order)

        return {
            "order_id": str(order_id),
            "status": "paid",
            "total_amount": float(order.total_amount.amount),
            "currency": order.total_amount.currency
        }