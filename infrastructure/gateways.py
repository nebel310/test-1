from uuid import UUID
from domain.models import Money
from application.use_cases import PaymentGateway

class FakePaymentGateway(PaymentGateway):
    def __init__(self, should_fail: bool = False):
        self._should_fail = should_fail
        self._payment_log = []

    def charge(self, order_id: UUID, money: Money) -> bool:
        self._payment_log.append({
            "order_id": order_id,
            "amount": float(money.amount),
            "currency": money.currency
        })
        
        if self._should_fail:
            return False
        
        return True

    def get_payment_log(self):
        return self._payment_log.copy()

    def clear_log(self):
        self._payment_log.clear()