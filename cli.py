import argparse
import sys
import os
from bot.client import BinanceClient
from bot.orders import place_order
from bot.validators import validate_inputs
from bot.logging_config import setup_logger

logger = setup_logger()


def print_order_summary(symbol, side, order_type, quantity, price):
    print("\n" + "="*50)
    print("       ORDER REQUEST SUMMARY")
    print("="*50)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"  Price      : {price}")
    print("="*50 + "\n")


def print_order_response(response: dict):
    print("\n" + "="*50)
    print("       ORDER RESPONSE DETAILS")
    print("="*50)
    print(f"  Order ID   : {response.get('orderId', 'N/A')}")
    print(f"  Status     : {response.get('status', 'N/A')}")
    print(f"  Executed   : {response.get('executedQty', '0')}")
    avg_price = response.get('avgPrice') or response.get('price', 'N/A')
    print(f"  Avg Price  : {avg_price}")
    print(f"  Symbol     : {response.get('symbol', 'N/A')}")
    print(f"  Side       : {response.get('side', 'N/A')}")
    print(f"  Type       : {response.get('type', 'N/A')}")
    print("="*50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("--symbol",     required=True,  help="Trading pair symbol, e.g. BTCUSDT")
    parser.add_argument("--side",       required=True,  help="Order side: BUY or SELL")
    parser.add_argument("--type",       required=True,  dest="order_type", help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity",   required=True,  type=float, help="Order quantity")
    parser.add_argument("--price",      required=False, type=float, default=None, help="Price (required for LIMIT orders)")
    parser.add_argument("--api-key",    required=False, default=os.getenv("BINANCE_API_KEY"),    help="Binance API key (or set BINANCE_API_KEY env var)")
    parser.add_argument("--api-secret", required=False, default=os.getenv("BINANCE_API_SECRET"), help="Binance API secret (or set BINANCE_API_SECRET env var)")

    args = parser.parse_args()

    # Check credentials
    if not args.api_key or not args.api_secret:
        print("ERROR: API key and secret required. Use --api-key/--api-secret or set environment variables.")
        logger.error("Missing API credentials.")
        sys.exit(1)

    # Validate inputs
    try:
        symbol, side, order_type = validate_inputs(
            args.symbol, args.side, args.order_type, args.quantity, args.price
        )
    except ValueError as e:
        print(f"\nValidation Error: {e}")
        logger.error(f"Validation failed: {e}")
        sys.exit(1)

    # Show request summary
    print_order_summary(symbol, side, order_type, args.quantity, args.price)

    # Place order
    client = BinanceClient(api_key=args.api_key, api_secret=args.api_secret)

    try:
        response = place_order(
            client=client,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=args.quantity,
            price=args.price
        )
        print_order_response(response)
        print("✅ Order placed successfully!\n")
        logger.info("Order completed successfully.")

    except RuntimeError as e:
        print(f"\n❌ Order failed: {e}\n")
        logger.error(f"Order failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        logger.exception("Unexpected error during order placement.")
        sys.exit(1)


if __name__ == "__main__":
    main()
