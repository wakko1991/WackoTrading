#!/usr/bin/env python3
"""
estrategias.py: Integración de estrategias inspiradas en CryptoSignal/Crypto-Signal y Token Metrics.
Se incluyen funciones para generar señales de trading basadas en análisis técnico.
"""

import pandas as pd
import talib
import numpy as np
from datetime import datetime

def estrategia_cryptosignal(df: pd.DataFrame) -> dict:
    """
    Función inspirada en CryptoSignal: utiliza indicadores técnicos para generar una señal de trading.
    
    Parámetros:
        df (DataFrame): Datos históricos del mercado (columnas: open, high, low, close, volume).
        
    Retorna:
        dict: Diccionario con la señal ('compra', 'venta' o 'neutral') y valores de indicadores.
    """
    if len(df) < 50:
        return {"señal": "datos insuficientes", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    close = df['close']
    # Calcula RSI (periodo 14)
    rsi = talib.RSI(close, timeperiod=14)
    # Calcula MACD
    macd, macd_signal, _ = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    # Calcula SMA de 50 períodos
    sma50 = talib.SMA(close, timeperiod=50)
    
    # Condiciones simples para generar señales
    if rsi.iloc[-1] < 30 and macd.iloc[-1] > macd_signal.iloc[-1] and close.iloc[-1] > sma50.iloc[-1]:
        señal = "compra"
    elif rsi.iloc[-1] > 70 and macd.iloc[-1] < macd_signal.iloc[-1] and close.iloc[-1] < sma50.iloc[-1]:
        señal = "venta"
    else:
        señal = "neutral"
    
    return {
        "señal": señal,
        "rsi": round(rsi.iloc[-1], 2),
        "macd": round(macd.iloc[-1], 2),
        "macd_signal": round(macd_signal.iloc[-1], 2),
        "sma50": round(sma50.iloc[-1], 2),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
