from bot.client import BinanceClient
from bot.logging_config import setup_logger

logger = setup_logger()


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None
) -> dict:
    """
    Place a MARKET or LIMIT order on Binance Futures Testnet.
    Returns the API response dict.
    """

    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"  # Good Till Cancelled

    # Log the request summary
    logger.info(f"Placing {order_type} {side} order | Symbol: {symbol} | Qty: {quantity}" +
                (f" | Price: {price}" if price else ""))

    response = client.post("/fapi/v1/order", params)

    logger.info(f"Order placed successfully | OrderID: {response.get('orderId')} | Status: {response.get('status')}")

    return response
