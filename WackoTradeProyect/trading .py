#!/usr/bin/env python3
"""
trading.py: BLOQUE 14 - Funciones para trading automatizado y creación de órdenes.
"""

import time
import hmac
import hashlib
import requests
import random
import logging
from colorama import Fore, Style
import configuracion
import datos_mercado

def bybit_create_order(api_key: str, api_secret: str, symbol: str, side: str, order_type: str, qty: float, price: float = None, testnet: bool = True) -> dict:
    base_url = "https://api-testnet.bybit.com" if testnet else "https://api.bybit.com"
    endpoint = "/v2/private/order/create"
    params = {
        "api_key": api_key,
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "qty": qty,
        "time_in_force": "GoodTillCancel",
        "timestamp": str(int(time.time() * 1000)),
        "recv_window": "5000"
    }
    if order_type.lower() == "limit" and price:
        params["price"] = price
    param_str = "&".join([f"{key}={params[key]}" for key in sorted(params)])
    sign = hmac.new(api_secret.encode(), param_str.encode(), hashlib.sha256).hexdigest()
    params["sign"] = sign
    try:
        response = requests.post(base_url + endpoint, params=params, timeout=5, verify=False)
        logging.info(f"Orden creada en Bybit para {symbol}.")
        return response.json()
    except Exception as e:
        logging.error(f"Error creando orden en Bybit: {e}")
        return {"error": str(e)}

def binance_create_order(api_key: str, api_secret: str, symbol: str, side: str, order_type: str, qty: float, price: float = None) -> dict:
    base_url = random.choice(configuracion.EXCHANGES['binance']['base_urls'])
    endpoint = "/order"
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol,
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": qty,
        "timestamp": timestamp,
        "recvWindow": 5000
    }
    if order_type.lower() == "limit" and price:
        params["price"] = price
        params["timeInForce"] = "GTC"
    param_str = "&".join([f"{key}={params[key]}" for key in sorted(params)])
    sign = hmac.new(api_secret.encode(), param_str.encode(), hashlib.sha256).hexdigest()
    params["signature"] = sign
    headers = {"X-MBX-APIKEY": api_key}
    try:
        response = requests.post(base_url + endpoint, params=params, headers=headers, timeout=5)
        logging.info(f"Orden creada en Binance para {symbol}.")
        return response.json()
    except Exception as e:
        logging.error(f"Error creando orden en Binance: {e}")
        return {"error": str(e)}

def trading_automatizado():
    from configuracion import PERSONAL_API_KEY, PERSONAL_API_SECRET, PERSONAL_EXCHANGE
    if not (PERSONAL_API_KEY and PERSONAL_API_SECRET and PERSONAL_EXCHANGE):
        print(Fore.RED + "Para el trading automatizado es necesaria la API personalizada. Configure su API desde el inicio." + Style.RESET_ALL)
        logging.warning("Intento de trading automatizado sin API personalizada.")
        return
    coin = input("Ingrese el símbolo de la moneda (ej: BTC): ").strip().upper() or "BTC"
    symbol = f"{coin}USDT"
    try:
        qty = float(input("Ingrese la cantidad a operar: ").strip())
    except:
        print("Cantidad inválida.")
        logging.error("Cantidad inválida en trading automatizado.")
        return
    metodo = input("Seleccione método (scalping/swing/grids): ").strip().lower()
    try:
        df = datos_mercado.obtener_datos_mercado(coin, "1m", "1")
        precio_actual = df['close'].iloc[-1]
    except Exception as e:
        print(Fore.RED + f"Error obteniendo precio: {e}" + Style.RESET_ALL)
        logging.error(f"Error obteniendo precio para trading automatizado: {e}")
        return
    print(Fore.BLUE + f"Precio actual de {symbol}: {precio_actual}" + Style.RESET_ALL)
    if metodo == "scalping":
        target = round(precio_actual * 1.01, 4)
    elif metodo == "swing":
        target = round(precio_actual * 1.05, 4)
    elif metodo == "grids":
        target = round(precio_actual * 1.03, 4)
    else:
        print("Método no reconocido.")
        logging.warning("Método no reconocido en trading automatizado.")
        return
    print(Fore.GREEN + f"Se procederá a comprar {qty} {coin} a mercado y vender a {target}." + Style.RESET_ALL)
    if PERSONAL_EXCHANGE.lower() == "bybit":
        buy_response = bybit_create_order(PERSONAL_API_KEY, PERSONAL_API_SECRET, symbol, "Buy", "Market", qty, testnet=True)
        print("Orden de compra (Bybit):", buy_response)
        time.sleep(2)
        sell_response = bybit_create_order(PERSONAL_API_KEY, PERSONAL_API_SECRET, symbol, "Sell", "Limit", qty, price=target, testnet=True)
        print("Orden de venta (Bybit):", sell_response)
    elif PERSONAL_EXCHANGE.lower() == "binance":
        buy_response = binance_create_order(PERSONAL_API_KEY, PERSONAL_API_SECRET, symbol, "BUY", "MARKET", qty)
        print("Orden de compra (Binance):", buy_response)
        time.sleep(2)
        sell_response = binance_create_order(PERSONAL_API_KEY, PERSONAL_API_SECRET, symbol, "SELL", "LIMIT", qty, price=target)
        print("Orden de venta (Binance):", sell_response)
    else:
        print("Trading automatizado no implementado para este exchange.")
        logging.warning("Trading automatizado no implementado para el exchange seleccionado.")
