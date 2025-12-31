import pytest
from uuid import uuid4
from decimal import Decimal

from domain.models import Order, Money
from domain.exceptions import EmptyOrderException, OrderAlreadyPaidException, OrderModificationException, PaymentFailedException
from application.use_cases import PayOrderUseCase
from infrastructure.repositories import InMemoryOrderRepository
from infrastructure.gateways import FakePaymentGateway

class TestPayOrderUseCase:
    def test_successful_payment(self):
        order_repo = InMemoryOrderRepository()
        payment_gateway = FakePaymentGateway()
        use_case = PayOrderUseCase(order_repo, payment_gateway)

        order_id = uuid4()
        customer_id = uuid4()
        order = Order(order_id, customer_id)
        
        order.add_line(
            product_id=uuid4(),
            product_name="Test Product",
            price=Money(Decimal("100.00")),
            quantity=2
        )
        
        order_repo.save(order)

        result = use_case.execute(order_id)

        assert result["status"] == "paid"
        assert result["total_amount"] == 200.0
        assert result["currency"] == "USD"
        assert order.status.value == "paid"
        assert len(payment_gateway.get_payment_log()) == 1

    def test_payment_empty_order(self):
        order_repo = InMemoryOrderRepository()
        payment_gateway = FakePaymentGateway()
        use_case = PayOrderUseCase(order_repo, payment_gateway)

        order_id = uuid4()
        customer_id = uuid4()
        order = Order(order_id, customer_id)
        order_repo.save(order)

        with pytest.raises(EmptyOrderException):
            use_case.execute(order_id)

        assert order.status.value == "created"

    def test_double_payment_fails(self):
        order_repo = InMemoryOrderRepository()
        payment_gateway = FakePaymentGateway()
        use_case = PayOrderUseCase(order_repo, payment_gateway)

        order_id = uuid4()
        customer_id = uuid4()
        order = Order(order_id, customer_id)
        
        order.add_line(
            product_id=uuid4(),
            product_name="Test Product",
            price=Money(Decimal("50.00")),
            quantity=1
        )
        
        order_repo.save(order)

        use_case.execute(order_id)

        with pytest.raises(OrderAlreadyPaidException):
            use_case.execute(order_id)

        assert order.status.value == "paid"

    def test_cannot_modify_after_payment(self):
        order_repo = InMemoryOrderRepository()
        payment_gateway = FakePaymentGateway()
        use_case = PayOrderUseCase(order_repo, payment_gateway)

        order_id = uuid4()
        customer_id = uuid4()
        order = Order(order_id, customer_id)
        
        product_id = uuid4()
        order.add_line(
            product_id=product_id,
            product_name="Test Product",
            price=Money(Decimal("30.00")),
            quantity=3
        )
        
        order_repo.save(order)

        use_case.execute(order_id)

        with pytest.raises(OrderModificationException):
            order.remove_line(product_id)

        with pytest.raises(OrderModificationException):
            order.add_line(
                product_id=uuid4(),
                product_name="Another Product",
                price=Money(Decimal("20.00")),
                quantity=1
            )

        assert order.status.value == "paid"

    def test_correct_total_calculation(self):
        order_id = uuid4()
        customer_id = uuid4()
        order = Order(order_id, customer_id)
        
        order.add_line(
            product_id=uuid4(),
            product_name="Product A",
            price=Money(Decimal("10.00")),
            quantity=5
        )
        
        order.add_line(
            product_id=uuid4(),
            product_name="Product B",
            price=Money(Decimal("25.50")),
            quantity=2
        )
        
        total = order.total_amount
        assert total.amount == Decimal("10.00") * 5 + Decimal("25.50") * 2
        assert total.amount == Decimal("101.00")

    def test_payment_gateway_failure(self):
        order_repo = InMemoryOrderRepository()
        payment_gateway = FakePaymentGateway(should_fail=True)
        use_case = PayOrderUseCase(order_repo, payment_gateway)

        order_id = uuid4()
        customer_id = uuid4()
        order = Order(order_id, customer_id)
        
        order.add_line(
            product_id=uuid4(),
            product_name="Test Product",
            price=Money(Decimal("75.00")),
            quantity=1
        )
        
        order_repo.save(order)

        with pytest.raises(PaymentFailedException):
            use_case.execute(order_id)

        assert order.status.value == "created"