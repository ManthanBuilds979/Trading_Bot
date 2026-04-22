from bot.logging_config import setup_logger

logger = setup_logger()

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """Validate all CLI inputs. Raises ValueError on bad input."""

    if not symbol or not symbol.isalpha():
        raise ValueError(f"Invalid symbol '{symbol}'. Must be alphabetic, e.g. BTCUSDT.")

    symbol = symbol.upper()

    if side.upper() not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be BUY or SELL.")

    if order_type.upper() not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type '{order_type}'. Must be MARKET or LIMIT.")

    if quantity <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got: {quantity}")

    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("Price is required and must be > 0 for LIMIT orders.")

    logger.debug(f"Validation passed: symbol={symbol}, side={side}, type={order_type}, qty={quantity}, price={price}")

    return symbol.upper(), side.upper(), order_type.upper()
