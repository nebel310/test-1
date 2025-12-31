DEFAULT_CURRENCY = "USD"
TAX_RATE = 0.21
COUPON_SAVE10 = "SAVE10"
COUPON_SAVE20 = "SAVE20"
COUPON_VIP = "VIP"
SAVE10_DISCOUNT_RATE = 0.10
SAVE20_DISCOUNT_RATE_HIGH = 0.20
SAVE20_DISCOUNT_RATE_LOW = 0.05
SAVE20_THRESHOLD = 200
VIP_DISCOUNT_HIGH = 50
VIP_DISCOUNT_LOW = 10
VIP_THRESHOLD = 100

def parse_request(request):
    user_id = request.get("user_id")
    items = request.get("items")
    coupon = request.get("coupon")
    currency = request.get("currency")
    return user_id, items, coupon, currency

def validate_request(user_id, items, currency):
    if user_id is None:
        raise ValueError("user_id is required")
    if items is None:
        raise ValueError("items is required")
    if currency is None:
        currency = DEFAULT_CURRENCY
    
    if not isinstance(items, list):
        raise ValueError("items must be a list")
    if len(items) == 0:
        raise ValueError("items must not be empty")
    
    for item in items:
        if "price" not in item or "qty" not in item:
            raise ValueError("item must have price and qty")
        if item["price"] <= 0:
            raise ValueError("price must be positive")
        if item["qty"] <= 0:
            raise ValueError("qty must be positive")
    
    return currency

def calculate_subtotal(items):
    subtotal = 0
    for item in items:
        subtotal += item["price"] * item["qty"]
    return subtotal

def calculate_discount(coupon, subtotal):
    if coupon is None or coupon == "":
        return 0
    
    if coupon == COUPON_SAVE10:
        return int(subtotal * SAVE10_DISCOUNT_RATE)
    
    if coupon == COUPON_SAVE20:
        if subtotal >= SAVE20_THRESHOLD:
            return int(subtotal * SAVE20_DISCOUNT_RATE_HIGH)
        else:
            return int(subtotal * SAVE20_DISCOUNT_RATE_LOW)
    
    if coupon == COUPON_VIP:
        if subtotal >= VIP_THRESHOLD:
            return VIP_DISCOUNT_HIGH
        else:
            return VIP_DISCOUNT_LOW
    
    raise ValueError("unknown coupon")

def calculate_tax(amount):
    return int(amount * TAX_RATE)

def generate_order_id(user_id, items_count):
    return f"{user_id}-{items_count}-X"

def process_checkout(request):
    user_id, items, coupon, currency = parse_request(request)
    
    currency = validate_request(user_id, items, currency)
    subtotal = calculate_subtotal(items)
    discount = calculate_discount(coupon, subtotal)
    
    total_after_discount = subtotal - discount
    if total_after_discount < 0:
        total_after_discount = 0
    
    tax = calculate_tax(total_after_discount)
    total = total_after_discount + tax
    order_id = generate_order_id(user_id, len(items))
    
    return {
        "order_id": order_id,
        "user_id": user_id,
        "currency": currency,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "items_count": len(items),
    }