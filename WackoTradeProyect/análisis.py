#!/usr/bin/env python3
"""
analisis.py: BLOQUES 10, 11, 13, 16, 18, 19, 21 y 23 - Funciones de análisis, backtesting y selección.
"""

import os
import sys
import time
import random
import threading
import logging
import pandas as pd
import numpy as np
import talib
from datetime import datetime, timedelta
from colorama import Fore, Style
from scipy.signal import argrelextrema
import datos_mercado
import configuracion
import utils

def calcular_entrada_tp_sl(precio_actual: float, cruce_info: dict) -> dict:
    if "Alcista" in cruce_info.get('cruce', ""):
        entrada = precio_actual
        tp1 = round(precio_actual * 1.01, 4)
        tp2 = round(precio_actual * 1.02, 4)
        tp3 = round(precio_actual * 1.03, 4)
        sl = round(precio_actual * 0.99, 4)
        direction = "Alcista 🐂"
    elif "Bajista" in cruce_info.get('cruce', ""):
        entrada = precio_actual
        tp1 = round(precio_actual * 0.99, 4)
        tp2 = round(precio_actual * 0.98, 4)
        tp3 = round(precio_actual * 0.97, 4)
        sl = round(precio_actual * 1.01, 4)
        direction = "Bajista 🐻"
    else:
        entrada = precio_actual
        tp1 = tp2 = tp3 = None
        sl = None
        direction = "Neutral ⚠️"
    return {"entrada": entrada, "tp_levels": [tp1, tp2, tp3], "stop_loss": sl, "direction": direction}

def calcular_indicadores(df: pd.DataFrame) -> dict:
    try:
        close = df["close"]
        rsi = talib.RSI(close, timeperiod=configuracion.RSI_PERIOD)
        macd, macd_signal, _ = talib.MACD(close, fastperiod=configuracion.MACD_FAST, slowperiod=configuracion.MACD_SLOW, signalperiod=configuracion.MACD_SIGNAL)
        atr = talib.ATR(df["high"], df["low"], close, timeperiod=configuracion.ATR_PERIOD)
        sma_20 = talib.SMA(close, timeperiod=configuracion.SMA_PERIOD_20)
        sma_50 = talib.SMA(close, timeperiod=configuracion.SMA_PERIOD_50)
        indicadores = {
            "rsi": round(rsi.iloc[-1], 2) if not rsi.empty else None,
            "macd": round(macd.iloc[-1], 4) if not macd.empty else None,
            "macd_signal": round(macd_signal.iloc[-1], 4) if not macd_signal.empty else None,
            "atr": round(atr.iloc[-1], 4) if not atr.empty else None,
            "sma_20": round(sma_20.iloc[-1], 4) if not sma_20.empty else None,
            "sma_50": round(sma_50.iloc[-1], 4) if not sma_50.empty else None,
        }
        return indicadores
    except Exception as e:
        logging.error(f"Error calculando indicadores técnicos: {e}")
        return {}

def calcular_cruce_ema_ma(df: pd.DataFrame) -> dict:
    close = df['close']
    if len(close) < 200:
        raise Exception("No hay suficientes datos para calcular EMA200/MA200.")
    ema200 = talib.EMA(close, timeperiod=200).iloc[-1]
    sma200 = talib.SMA(close, timeperiod=200).iloc[-1]
    pct_diff = ((ema200 - sma200) / sma200 * 100) if sma200 != 0 else 0
    cruce_signal = "Cruzando" if abs(pct_diff) <= 0.1 else ("Cruzando (Alcista)" if pct_diff > 0 else "Cruzando (Bajista)")
    return {'ema200': round(ema200, 4), 'sma200': round(sma200, 4), 'pct_diff': round(pct_diff, 2), 'cruce': cruce_signal}

def calcular_niveles_clave(df: pd.DataFrame) -> dict:
    high = df['high'].values
    low = df['low'].values
    maxima = argrelextrema(high, np.greater, order=configuracion.PIVOT_WINDOW)[0]
    minima = argrelextrema(low, np.less, order=configuracion.PIVOT_WINDOW)[0]
    resistencias = high[maxima][-3:] if len(maxima) >= 3 else high[-3:]
    soportes = low[minima][-3:] if len(minima) >= 3 else low[-3:]
    pivot = (df['high'].iloc[-1] + df['low'].iloc[-1] + df['close'].iloc[-1]) / 3
    return {'soporte': round(np.mean(soportes), 4), 'resistencia': round(np.mean(resistencias), 4), 'pivot': round(pivot, 4)}

def determinar_fuerza_tendencia(rsi: float, macd: float, macd_signal: float) -> str:
    diff = macd - macd_signal
    if rsi > 70 and diff > 0.05:
        return "Fuerte Alcista"
    elif rsi < 30 and diff < -0.05:
        return "Fuerte Bajista"
    elif rsi >= 50 and diff > 0:
        return "Alcista"
    elif rsi <= 50 and diff < 0:
        return "Bajista"
    else:
        return "Lateral"

def detectar_manipulacion_ballenas(df: pd.DataFrame) -> dict:
    accumPeriod = 10
    stableThreshold = 0.02
    volMultiplier = 1.5
    reversalThreshold = 0.02
    if len(df) < accumPeriod:
        return {}
    avgPrice = df['close'].rolling(window=accumPeriod).mean().iloc[-1]
    priceStd = df['close'].rolling(window=accumPeriod).std().iloc[-1]
    stableCondition = (priceStd / avgPrice) < stableThreshold
    avgVolume = df['volume'].rolling(window=accumPeriod).mean().iloc[-1]
    current_volume = df['volume'].iloc[-1]
    lowVolumeCond = current_volume < avgVolume
    inAccumulation = stableCondition and lowVolumeCond
    accumSignal = False
    if inAccumulation and (current_volume > avgVolume * volMultiplier) and (df['close'].iloc[-1] > df['open'].iloc[-1]):
        accumSignal = True
        inAccumulation = False
    distReference = df['close'].rolling(window=accumPeriod).max().iloc[-1]
    distSignal = False
    if (df['close'].iloc[-1] >= distReference * (1 - stableThreshold)) and (current_volume > avgVolume * volMultiplier) and (df['close'].iloc[-1] < df['open'].iloc[-1]):
        distSignal = True
    falseBreakoutSignal = False
    if len(df) > accumPeriod + 1:
        prev_high = df['high'].iloc[-2]
        highest_prev = df['high'].rolling(window=accumPeriod).max().shift(1).iloc[-1]
        prev_close = df['close'].iloc[-2]
        prev_open = df['open'].iloc[-2]
        if (prev_high > highest_prev) and (prev_close > prev_open) and (df['close'].iloc[-1] < prev_close * (1 - reversalThreshold)):
            falseBreakoutSignal = True
    return {
        "accumSignal": accumSignal,
        "distSignal": distSignal,
        "falseBreakoutSignal": falseBreakoutSignal,
        "inAccumulation": inAccumulation
    }

def analizar_tendencia(df: pd.DataFrame) -> dict:
    if len(df) < 100:
        raise Exception("Datos insuficientes para análisis.")
    precio_actual = df['close'].iloc[-1]
    indicadores = calcular_indicadores(df)
    niveles = calcular_niveles_clave(df)
    fuerza = determinar_fuerza_tendencia(indicadores['rsi'], indicadores['macd'], indicadores['macd_signal'])
    cruce_info = calcular_cruce_ema_ma(df)
    trade_info = calcular_entrada_tp_sl(precio_actual, cruce_info)
    whale_data = detectar_manipulacion_ballenas(df)
    whale_count = sum(1 for key in ["accumSignal", "distSignal", "falseBreakoutSignal"] if whale_data.get(key))
    if whale_count > 0:
        whale_status = f"Detectado 🐋 ({whale_count})"
    else:
        whale_status = "No detectado 🐋 (0)"
    if 49 <= indicadores['rsi'] <= 51:
        dominancia = f"Sin dominancia significativa: RSI: {indicadores['rsi']:.2f}% / {(100 - indicadores['rsi']):.2f}%"
    elif indicadores['rsi'] > 50:
        dominancia = f"🐂 Bulls dominan: {indicadores['rsi']:.2f}% | 🐻 Bears: {(100 - indicadores['rsi']):.2f}%"
    else:
        dominancia = f"🐻 Bears dominan: {(100 - indicadores['rsi']):.2f}% | 🐂 Bulls: {indicadores['rsi']:.2f}%"
    if indicadores['sma_20'] > indicadores['sma_50'] and precio_actual > indicadores['sma_20']:
        tendencia = "Alcista"
        senal = "Señal de compra"
    elif indicadores['sma_20'] < indicadores['sma_50'] and precio_actual < indicadores['sma_20']:
        tendencia = "Bajista"
        senal = "Señal de venta"
    else:
        tendencia = "Lateral"
        senal = "Sin señal clara"
    return {
        'precio_actual': round(precio_actual, 4),
        'tendencia': tendencia,
        'fuerza': fuerza,
        'senal': senal,
        **indicadores,
        **niveles,
        'ema200': cruce_info['ema200'],
        'ma200': cruce_info['sma200'],
        'ema_ma_diff_pct': cruce_info['pct_diff'],
        'cruce_signal': cruce_info['cruce'],
        'dominancia': dominancia,
        'entrada': trade_info["entrada"],
        'tp_levels': trade_info["tp_levels"],
        'stop_loss': trade_info["stop_loss"],
        'trade_direction': trade_info["direction"],
        'whale': whale_status,
        'whale_count': whale_count,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def convertir_a_nativo(dic: dict) -> dict:
    nuevo_dic = {}
    for clave, valor in dic.items():
        nuevo_dic[clave] = float(valor) if isinstance(valor, np.float64) else valor
    return nuevo_dic

def backtest_strategy():
    crypto = input("Ingrese el símbolo de la criptomoneda para Backtesting (ej. BTC): ").strip().upper() or "BTC"
    folder = crypto
    filename = f"{crypto}_backtest.csv"
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(Fore.GREEN + f"Carpeta '{folder}' creada." + Style.RESET_ALL)
    filepath = os.path.join(folder, filename)
    try:
        if os.path.isfile(filepath):
            df_existing = pd.read_csv(filepath, index_col=0, parse_dates=True)
            print(Fore.GREEN + f"Archivo existente '{filename}' cargado. Actualizando información..." + Style.RESET_ALL)
        else:
            df_existing = pd.DataFrame()
            print(Fore.GREEN + f"No se encontró archivo '{filename}'. Se creará uno nuevo." + Style.RESET_ALL)
        df_new = obtener_datos_mercado(crypto, '1d', "1")
        if not df_existing.empty:
            df_combined = pd.concat([df_existing, df_new])
            df_combined = df_combined[~df_combined.index.duplicated(keep='last')]
        else:
            df_combined = df_new
        df_combined.to_csv(filepath)
        print(Fore.GREEN + f"Backtesting iniciado. Archivo actualizado: {filepath}" + Style.RESET_ALL)
        print(df_combined.describe())
    except Exception as e:
        print(Fore.RED + f"Error en backtesting: {e}" + Style.RESET_ALL)
        logging.error(f"Error en backtesting: {e}")
    input("Presione Enter para volver al menú principal...")

def mostrar_resultados(analisis: dict, timeframe: str, monto: float, apalancamiento: int, crypto: str, modo_salida: str, riesgo: float, tipo_operacion: str):
    symbol = f"{crypto.upper()}USDT"
    futures_mode = True if tipo_operacion=='2' else False
    ticker_info = datos_mercado.obtener_ticker_info(symbol, futures_mode=futures_mode)
    if not ticker_info:
        print(Fore.RED + "No se pudo obtener información del ticker en tiempo real." + Style.RESET_ALL)
        return
    print(Fore.CYAN + f"\n📊 Análisis {timeframe} - {analisis.get('timestamp', '')}" + Style.RESET_ALL)
    print("-" * 60)
    print(Fore.YELLOW + "Estadísticas 24h:" + Style.RESET_ALL)
    print(f"  🏔 Máximo 24h: {ticker_info.get('highPrice')}")
    print(f"  🔻 Mínimo 24h: {ticker_info.get('lowPrice')}")
    print(f"  💰 Volumen 24h: {ticker_info.get('volume')}")
    print(f"  📉 Cambio 24h: {ticker_info.get('priceChange')} ({ticker_info.get('priceChangePercent')}%)\n")
    precio_actual = ticker_info.get("lastPrice") or ticker_info.get("closePrice")
    print(Fore.CYAN + f"💰 Precio Actual: {precio_actual}" + Style.RESET_ALL)
    print(Fore.GREEN + f"📈 Tendencia: {analisis.get('tendencia')} ({analisis.get('senal')})" + Style.RESET_ALL)
    print(Fore.MAGENTA + f"Fuerza de la Tendencia: {analisis.get('fuerza')}" + Style.RESET_ALL)
    print(Fore.BLUE + "\nIndicadores Técnicos:" + Style.RESET_ALL)
    for key in ['rsi', 'macd', 'macd_signal', 'atr', 'sma_20', 'sma_50']:
        print(f"  {key.upper()}: {analisis.get(key)}")
    print(Fore.BLUE + f"\nDominancia: {analisis.get('dominancia')}" + Style.RESET_ALL)
    print(Fore.CYAN + f"Cruce EMA200/MA200: {analisis.get('cruce_signal')} (Dif. %: {analisis.get('ema_ma_diff_pct')}%)" + Style.RESET_ALL)
    print(Fore.WHITE + f"\n🚀 Entrada: {analisis.get('entrada')}" + Style.RESET_ALL)
    tp_levels = analisis.get("tp_levels", [])
    if tp_levels and None not in tp_levels:
        print(Fore.GREEN + f"💰 Take Profit (niveles): {tp_levels[0]}, {tp_levels[1]}, {tp_levels[2]}" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "💰 Take Profit: No definido" + Style.RESET_ALL)
    sl = analisis.get("stop_loss")
    if sl:
        print(Fore.RED + f"🔴 Stop Loss: {sl}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "🔴 Stop Loss: No definido" + Style.RESET_ALL)
    print(Fore.YELLOW + "\n💹 Resumen del Mercado:" + Style.RESET_ALL)
    print(f"  Precio Actual ({crypto.upper()}/USDT): {precio_actual}")
    cmc_info = datos_mercado.obtener_info_cmc(crypto)
    print(f"  Flujo de efectivo neto: {cmc_info.get('net_cash_flow')}")
    print(f"  Índice de Miedo y Codicia: {cmc_info.get('fear_and_greed')}")
    print(Fore.YELLOW + "\n🔰 Soporte y Resistencia:" + Style.RESET_ALL)
    print(f"  Soporte: {analisis.get('soporte')}")
    print(f"  Resistencia: {analisis.get('resistencia')}")
    print(Fore.YELLOW + "\n📊 Conclusión:" + Style.RESET_ALL)
    print(f"  El análisis indica que {crypto.upper()} se encuentra en una tendencia {analisis.get('tendencia').lower()} con dominancia {analisis.get('dominancia')}.")
    print(f"  Detección de Ballenas: {analisis.get('whale')}") 
    print("-" * 60)
    modo = "Binance Futuros" if tipo_operacion=='2' else "Binance Spot"
    print(Fore.WHITE + f"Datos obtenidos de {modo} usando un endpoint seleccionado." + Style.RESET_ALL)
    print(Fore.MAGENTA + f"\n💡 Frase del día: {utils.frase_motivadora()}" + Style.RESET_ALL)
    print("\nOpciones:")
    print("  R - Refrescar/Actualizar resultados del trading")
    print("  S - Detener actualización y volver al menú de selección")
    print("  E - Salir del programa")
    opcion_final = utils.input_con_timeout("Seleccione opción (R/S/E): ", configuracion.REFRESH_INTERVAL).strip().lower()
    if opcion_final == 'r':
        print(Fore.GREEN + "\nActualizando resultados..." + Style.RESET_ALL)
        return "refrescar"
    elif opcion_final == 's':
        print(Fore.YELLOW + "\nDeteniendo actualización y volviendo al menú principal." + Style.RESET_ALL)
        return "detener"
    elif opcion_final == 'e':
        conf = input("¿Está seguro que desea salir? (S/N): ").strip().lower()
        if conf == 's':
            print(Fore.RED + "\nSaliendo del programa." + Style.RESET_ALL)
            sys.exit(0)
        else:
            return "detener"
    else:
        print(Fore.YELLOW + "\nOpción no válida. Volviendo al menú principal." + Style.RESET_ALL)
        return "detener"
