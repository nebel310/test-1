class DomainException(Exception):
    pass

class EmptyOrderException(DomainException):
    pass

class OrderAlreadyPaidException(DomainException):
    pass

class OrderModificationException(DomainException):
    pass

class PaymentFailedException(DomainException):
    pass