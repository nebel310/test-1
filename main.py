from uuid import uuid4
from decimal import Decimal
from domain.models import Order, Money
from application.use_cases import PayOrderUseCase
from infrastructure.repositories import InMemoryOrderRepository
from infrastructure.gateways import FakePaymentGateway

def main():
    order_repo = InMemoryOrderRepository()
    payment_gateway = FakePaymentGateway()
    use_case = PayOrderUseCase(order_repo, payment_gateway)

    order_id = uuid4()
    customer_id = uuid4()
    order = Order(order_id, customer_id)
    
    order.add_line(
        product_id=uuid4(),
        product_name="Laptop",
        price=Money(Decimal("999.99")),
        quantity=1
    )
    
    order.add_line(
        product_id=uuid4(),
        product_name="Mouse",
        price=Money(Decimal("29.99")),
        quantity=2
    )
    
    order_repo.save(order)

    print(f"Order created: {order}")
    print(f"Total amount: {order.total_amount.amount} {order.total_amount.currency}")

    try:
        result = use_case.execute(order_id)
        print(f"Payment successful: {result}")
    except Exception as e:
        print(f"Payment failed: {type(e).__name__}: {e}")

    print(f"Order status after payment attempt: {order.status.value}")

if __name__ == "__main__":
    main()