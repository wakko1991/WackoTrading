#!/usr/bin/env python3
"""
configuracion.py: BLOQUE 2 y BLOQUE 6 - Variables globales y Configuración de APIs.
"""

import os
import sys
import base64
from colorama import Fore, Style

# Variables globales (BLOQUE 2)
BINANCE_ENDPOINTS = [
    "https://api.binance.com/api/v3",
    "https://api-gcp.binance.com/api/v3",
    "https://api1.binance.com/api/v3",
    "https://api2.binance.com/api/v3",
    "https://api3.binance.com/api/v3",
    "https://api4.binance.com/api/v3"
]
BINANCE_FUTURES_ENDPOINT = "https://fapi.binance.com/fapi/v1"

EXCHANGES = {
    'binance': {
        'base_urls': BINANCE_ENDPOINTS,
        'klines_endpoint': '/klines',
        'ticker24h_endpoint': '/ticker/24hr',
        'account_endpoint': '/account'
    },
    'coinbase': {
        'base_url': 'https://api.pro.coinbase.com',
        'candles_endpoint': '/products/{symbol}/candles'
    },
    'kraken': {
        'base_url': 'https://api.kraken.com/0/public',
        'ohlc_endpoint': '/OHLC'
    },
    'bybit': {
        'base_url': 'https://api.bybit.com',
        'klines_endpoint': '/v2/public/kline/list'
    },
    'okx': {
        'base_url': 'https://www.okx.com/api/v5',
        'klines_endpoint': '/market/candles'
    }
}
CUSTOM_APIS = {}
TEMPORALIDADES_VALIDAS = ['1m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w']
ESTRATEGIAS = {
    '1': {'nombre': 'scalping', 'timeframes': ['1m', '5m', '15m']},
    '2': {'nombre': 'swing', 'timeframes': ['4h', '1d']},
    '3': {'nombre': 'personalizada', 'timeframes': []}
}
ATR_PERIOD = 14
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
SMA_PERIOD_20 = 20
SMA_PERIOD_50 = 50
PIVOT_WINDOW = 20
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
REFRESH_INTERVAL = 10
TRADING_MAX_SECONDS = 86400
CONCLUSION_COLOR = Fore.LIGHTGREEN_EX

LISTA_CRIPTOS = [
    {"symbol": "BTC", "name": "Bitcoin"},
    {"symbol": "ETH", "name": "Ethereum"},
    {"symbol": "XRP", "name": "Ripple"},
    {"symbol": "LTC", "name": "Litecoin"},
    {"symbol": "BCH", "name": "Bitcoin Cash"},
    {"symbol": "ADA", "name": "Cardano"},
    {"symbol": "DOT", "name": "Polkadot"},
    {"symbol": "LINK", "name": "Chainlink"},
    {"symbol": "BNB", "name": "Binance Coin"},
    {"symbol": "XLM", "name": "Stellar"},
    {"symbol": "DOGE", "name": "Dogecoin"},
    {"symbol": "SOL", "name": "Solana"},
    {"symbol": "AVAX", "name": "Avalanche"},
    {"symbol": "MATIC", "name": "Polygon"},
    {"symbol": "UNI", "name": "Uniswap"},
    {"symbol": "ALGO", "name": "Algorand"},
    {"symbol": "ATOM", "name": "Cosmos"},
    {"symbol": "ICP", "name": "Internet Computer"},
    {"symbol": "VET", "name": "VeChain"},
    {"symbol": "TRX", "name": "Tron"}
]

# Variables para APIs personalizadas (se configurarán en tiempo de ejecución)
PERSONAL_API_KEY = None
PERSONAL_API_SECRET = None
PERSONAL_EXCHANGE = None
CMC_API_KEY = None

def mostrar_faq_api():
    print("\n================= FAQ de APIs =================")
    print("Una API permite que tu software se comunique con plataformas externas.")
    print("Ejemplo: APIs de exchanges (Binance, Bybit) para trading o CoinMarketCap para datos.")
    print("Ejemplo de API key: ABCD1234EFGH5678")
    print("================================================\n")

def configurar_api_exchange():
    print("\n--- Configuración de API de Exchange ---")
    mostrar_faq_api()
    while True:
        api_key = input("Ingrese su API Key de Exchange: ").strip()
        api_secret = input("Ingrese su API Secret de Exchange: ").strip()
        if " " in api_key or len(api_key) < 8:
            print("❌ API Key inválida. Debe tener al menos 8 caracteres sin espacios.")
            continue
        if " " in api_secret or len(api_secret) < 8:
            print("❌ API Secret inválida. Debe tener al menos 8 caracteres sin espacios.")
            continue
        break
    remember = input("¿Desea recordar su API para Exchange? (S/N): ").strip().lower()
    if remember == 's':
        encrypted_api_key = base64.b64encode(api_key.encode()).decode()
        encrypted_api_secret = base64.b64encode(api_secret.encode()).decode()
        print(f"✅ API configurada: {api_key[:4]}🔑{api_key[-4:]}")
        return encrypted_api_key, encrypted_api_secret, "exchange"
    else:
        print(f"✅ API configurada: {api_key[:4]}🔑{api_key[-4:]}")
        return api_key, api_secret, "exchange"

def configurar_api_cmc():
    print("\n--- Configuración de API de CoinMarketCap ---")
    mostrar_faq_api()
    while True:
        cmc_api_key = input("Ingrese su API Key de CoinMarketCap: ").strip()
        if " " in cmc_api_key or len(cmc_api_key) < 8:
            print("❌ API Key inválida. Debe tener al menos 8 caracteres sin espacios.")
            continue
        break
    remember = input("¿Desea recordar su API para CoinMarketCap? (S/N): ").strip().lower()
    if remember == 's':
        encrypted_cmc_key = base64.b64encode(cmc_api_key.encode()).decode()
        print(f"✅ API configurada: {cmc_api_key[:4]}🔑{cmc_api_key[-4:]}")
        return encrypted_cmc_key, "cmc"
    else:
        print(f"✅ API configurada: {cmc_api_key[:4]}🔑{cmc_api_key[-4:]}")
        return cmc_api_key, "cmc"

def obtener_configuracion_api():
    respuesta = input("¿Desea configurar una API? (S/N): ").strip().lower()
    if respuesta != 's':
        print("Se utilizarán los endpoints por defecto.")
        return None, None, None
    mostrar_faq_api()
    print("Seleccione qué API configurar:")
    print("  1. API de Exchange")
    print("  2. API de CoinMarketCap")
    op = input("Seleccione opción (1 o 2): ").strip()
    exchange_api_key = exchange_api_secret = cmc_api_key = None
    if op == '1':
        exchange_api_key, exchange_api_secret, _ = configurar_api_exchange()
    elif op == '2':
        cmc_api_key, _ = configurar_api_cmc()
    else:
        print("Opción no válida, se usarán los endpoints por defecto.")
    return exchange_api_key, exchange_api_secret, cmc_api_key
