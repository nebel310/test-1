from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import List
from uuid import UUID, uuid4
from .exceptions import EmptyOrderException, OrderAlreadyPaidException, OrderModificationException

class OrderStatus(Enum):
    CREATED = "created"
    PAID = "paid"
    CANCELLED = "cancelled"

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, quantity):
        return Money(self.amount * Decimal(str(quantity)), self.currency)

@dataclass
class OrderLine:
    product_id: UUID
    product_name: str
    price: Money
    quantity: int

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

    @property
    def total(self) -> Money:
        return self.price * self.quantity

class Order:
    def __init__(self, order_id: UUID, customer_id: UUID):
        self._id = order_id
        self._customer_id = customer_id
        self._status = OrderStatus.CREATED
        self._lines: List[OrderLine] = []
        self._total_amount = Money(Decimal("0"))

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def customer_id(self) -> UUID:
        return self._customer_id

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def lines(self) -> List[OrderLine]:
        return self._lines.copy()

    @property
    def total_amount(self) -> Money:
        return self._total_amount

    def add_line(self, product_id: UUID, product_name: str, price: Money, quantity: int):
        if self._status != OrderStatus.CREATED:
            raise OrderModificationException("Cannot modify order after payment or cancellation")

        new_line = OrderLine(product_id, product_name, price, quantity)
        self._lines.append(new_line)
        self._recalculate_total()

    def remove_line(self, product_id: UUID):
        if self._status != OrderStatus.CREATED:
            raise OrderModificationException("Cannot modify order after payment or cancellation")

        self._lines = [line for line in self._lines if line.product_id != product_id]
        self._recalculate_total()

    def mark_as_paid(self):
        if self._status == OrderStatus.PAID:
            raise OrderAlreadyPaidException("Order is already paid")

        if not self._lines:
            raise EmptyOrderException("Cannot pay empty order")

        self._status = OrderStatus.PAID

    def mark_as_cancelled(self):
        if self._status == OrderStatus.PAID:
            raise OrderModificationException("Cannot cancel paid order")
        self._status = OrderStatus.CANCELLED

    def _recalculate_total(self):
        total = Money(Decimal("0"))
        for line in self._lines:
            total = total + line.total
        self._total_amount = total

    def __repr__(self):
        return f"Order(id={self._id}, status={self._status.value}, total={self._total_amount.amount})"