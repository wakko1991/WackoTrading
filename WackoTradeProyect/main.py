#!/usr/bin/env python3
"""
main.py: Módulo principal que integra todos los módulos del proyecto y muestra el menú.
"""

import sys
import time
from colorama import Fore, Style
import presentacion
import configuracion
import datos_mercado
import analisis
import trading
import soporte
import utils
import estrategias  # Módulo de estrategias inspiradas en CryptoSignal

def main():
    # BLOQUE 1: Presentación y aceptación de términos
    presentacion.imprimir_logo()
    
    # BLOQUE 6: Configuración de API
    exchange_api_key, exchange_api_secret, cmc_api_key = configuracion.obtener_configuracion_api()
    if exchange_api_key and exchange_api_secret:
        configuracion.PERSONAL_API_KEY = exchange_api_key
        configuracion.PERSONAL_API_SECRET = exchange_api_secret
        configuracion.PERSONAL_EXCHANGE = "binance"
    if cmc_api_key:
        configuracion.CMC_API_KEY = cmc_api_key

    while True:
        print(Fore.CYAN + "\n📋 MENU PRINCIPAL:" + Style.RESET_ALL)
        print("  1. Análisis en tiempo real")
        print("  2. Noticias Actualizadas (stub)")
        print("  3. Información / Glosario (stub)")
        print("  4. Agregar API personalizada")
        print("  5. Trading Automatizado")
        print("  6. Backtesting (CSV)")
        print("  7. Soporte y Apoyo")
        print("  8. Tendencias del Mercado (stub)")
        print("  9. Salir")
        print(" 10. Estrategia CryptoSignal (integrada)")  # NUEVA opción
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '1':
            analisis.analizar_mercado_tiempo_real()
        elif opcion == '2':
            print(Fore.CYAN + "\nNoticias Actualizadas (stub)." + Style.RESET_ALL)
            input("\nPresione Enter para volver al menú principal...")
        elif opcion == '3':
            print("\nInformación / Glosario (stub).")
            input("\nPresione Enter para volver al menú principal...")
        elif opcion == '4':
            configuracion.obtener_configuracion_api()
            input("Presione Enter para volver al menú principal...")
        elif opcion == '5':
            trading.trading_automatizado()
            input("Presione Enter para volver al menú principal...")
        elif opcion == '6':
            analisis.backtest_strategy()
        elif opcion == '7':
            soporte.mostrar_soporte_y_apoyo()
            input("\nPresione Enter para volver al menú principal...")
        elif opcion == '8':
            analisis.imprimir_banner_tendencias()
            input("\nPresione Enter para volver al menú principal...")
        elif opcion == '9':
            print(Fore.RED + "Saliendo..." + Style.RESET_ALL)
            sys.exit(0)
        elif opcion == '10':
            # NUEVA: Ejecutar estrategia inspirada en CryptoSignal
            crypto = input("Ingrese el símbolo de la criptomoneda (ej. BTC): ").strip().upper() or "BTC"
            try:
                df = datos_mercado.obtener_datos_mercado(crypto, '1h', "1")
                resultado = estrategias.estrategia_cryptosignal(df)
                print(Fore.GREEN + "\nResultado de la Estrategia CryptoSignal:" + Style.RESET_ALL)
                for key, value in resultado.items():
                    print(f"  {key}: {value}")
            except Exception as e:
                print(Fore.RED + f"Error al ejecutar la estrategia: {e}" + Style.RESET_ALL)
            input("\nPresione Enter para volver al menú principal...")
        else:
            print(Fore.RED + "Opción inválida." + Style.RESET_ALL)
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupción por el usuario. Cerrando el programa...")
        sys.exit(0)

# Archivo: presentacion.py
# Contiene el BLOQUE 1: Presentación y términos.
# Se recomienda no modificar las secciones marcadas como "NO MODIFICAR".
