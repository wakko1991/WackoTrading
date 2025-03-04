#!/usr/bin/env python3
"""
datos_mercado.py: BLOQUES 3, 4, 5, 7, 8 y 9 - Funciones para obtener y validar datos de mercado.
"""

import time
import random
import requests
import logging
import pandas as pd
import urllib3
from datetime import datetime
from colorama import Fore, Style
import configuracion

# NO MODIFICAR: Configuración SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def validar_simbolo(symbol: str) -> bool:
    return len(symbol) >= 5 and symbol.endswith('USDT')

def get_random_binance_endpoint() -> str:
    endpoint = random.choice(configuracion.EXCHANGES['binance']['base_urls'])
    try:
        response = requests.get(endpoint + '/ping', timeout=3)
        return endpoint if response.status_code == 200 else configuracion.BINANCE_ENDPOINTS[0]
    except Exception as e:
        logging.error(f"Error al validar endpoint: {e}")
        return configuracion.BINANCE_ENDPOINTS[0]

def obtener_ticker_info(symbol: str, futures_mode: bool = False) -> dict:
    if not validar_simbolo(symbol):
        logging.error(f"Símbolo inválido: {symbol}")
        return {}
    try:
        if futures_mode:
            url = configuracion.BINANCE_FUTURES_ENDPOINT + configuracion.EXCHANGES['binance']['ticker24h_endpoint']
        else:
            url = get_random_binance_endpoint() + configuracion.EXCHANGES['binance']['ticker24h_endpoint']
        params = {'symbol': symbol}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error obteniendo ticker info para {symbol}: {e}")
        return {}

def obtener_klines_binance(symbol: str, interval: str, futures_mode: bool = False, limit: int = 300) -> list:
    if not validar_simbolo(symbol):
        return []
    try:
        base_url = configuracion.BINANCE_FUTURES_ENDPOINT if futures_mode else get_random_binance_endpoint()
        url = base_url + configuracion.EXCHANGES['binance']['klines_endpoint']
        params = {'symbol': symbol, 'interval': interval, 'limit': limit}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error obteniendo klines para {symbol} en intervalo {interval}: {e}")
        return []

def obtener_datos_mercado(crypto: str, timeframe: str, tipo_operacion: str) -> pd.DataFrame:
    symbol = f"{crypto.upper()}USDT"
    futures_mode = True if tipo_operacion == '2' else False
    klines = obtener_klines_binance(symbol, timeframe, futures_mode=futures_mode, limit=300)
    if not klines:
        raise Exception("No se pudieron obtener datos de mercado reales.")
    try:
        df = pd.DataFrame(klines, columns=["open_time", "open", "high", "low", "close", "volume",
                                             "close_time", "quote_asset_volume", "number_of_trades",
                                             "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df["open_time"] = pd.to_datetime(df["open_time"], unit='ms')
        df = df.set_index("open_time")
        return df
    except Exception as e:
        logging.error(f"Error procesando datos de mercado: {e}")
        raise e

def validar_simbolo_binance(symbol: str, tipo_operacion: str = '1') -> bool:
    if tipo_operacion == '2':
        endpoints = ["https://fapi.binance.com/fapi/v1/exchangeInfo"]
    else:
        endpoints = [f"{url}/exchangeInfo" for url in configuracion.BINANCE_ENDPOINTS]
    for url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            symbols = [s["symbol"] for s in data.get("symbols", [])]
            if symbol in symbols:
                return True
        except Exception as e:
            logging.error(f"Error validando símbolo en Binance en {url}: {e}")
    return False

def obtener_info_cmc(crypto: str) -> dict:
    from configuracion import CMC_API_KEY
    if not CMC_API_KEY:
        print("API Key de CoinMarketCap no configurada. No se pueden obtener datos reales.")
        return {}
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {"symbol": crypto.upper(), "convert": "USD"}
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    try:
        response = requests.get(url, headers=headers, params=parameters, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "data" in data and crypto.upper() in data["data"]:
            crypto_data = data["data"][crypto.upper()]
            net_cash_flow = crypto_data.get("quote", {}).get("USD", {}).get("market_cap", "N/A")
            fear_and_greed = "No disponible"
            return {"net_cash_flow": net_cash_flow, "fear_and_greed": fear_and_greed}
        else:
            return {}
    except Exception as e:
        logging.error(f"Error en obtener_info_cmc: {e}")
        return {}

def run_bybit_websocket(symbol: str, interval: str, callback, testnet: bool = True):
    class FakeWS:
        def close(self):
            pass
    return FakeWS()

def run_binance_websocket(stream: str, combined: bool = False, callback=None):
    class FakeWS:
        def close(self):
            pass
    return FakeWS()
