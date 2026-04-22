# Binance Futures Testnet Trading Bot

A Python CLI trading bot for placing Market and Limit orders on Binance Futures Testnet (USDT-M).

## Setup

### 1. Register on Binance Futures Testnet
- Visit https://testnet.binancefuture.com
- Sign in with GitHub and generate API credentials

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set credentials (recommended)
```bash
export BINANCE_API_KEY=your_api_key
export BINANCE_API_SECRET=your_api_secret
```

## How to Run

### Market BUY order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Limit SELL order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 95000
```

### Passing credentials inline
```bash
python cli.py --symbol ETHUSDT --side BUY --type MARKET --quantity 0.1 \
  --api-key YOUR_KEY --api-secret YOUR_SECRET
```

## Logs
All logs are written to `logs/trading_bot.log`.

## Assumptions
- Only USDT-M Futures (not COIN-M)
- Quantity must match Binance's lot size for the symbol (e.g., 0.001 min for BTC)
- LIMIT orders use GTC (Good Till Cancelled) by default
