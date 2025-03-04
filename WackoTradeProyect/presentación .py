#!/usr/bin/env python3
"""
presentacion.py: BLOQUE 1 - Presentación con logo y términos de uso.
"""

import os
import sys
import time
import random
from colorama import Fore, Style, init
import pyfiglet
import utils

# Inicializar colorama
init(autoreset=True)

def centrar_texto(texto: str, ancho: int = 80) -> str:
    return "\n".join(line.center(ancho) for line in texto.splitlines())

def solicitar_sn(prompt: str) -> str:
    while True:
        respuesta = input(prompt).strip().lower()
        if respuesta in ["s", "n"]:
            return respuesta
        print(Fore.RED + "Error: Debe ingresar S o N." + Style.RESET_ALL)

def imprimir_logo():
    # Limpiar pantalla
    os.system('cls' if os.name == 'nt' else 'clear')
    ancho_terminal = 80
    # Banner principal
    banner_title = pyfiglet.figlet_format("WACKO", font="slant")
    color = random.choice([Fore.RED, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])
    print(centrar_texto(color + banner_title + Style.RESET_ALL, ancho_terminal))
    time.sleep(0.2)
    banner_title2 = pyfiglet.figlet_format("TRADING", font="slant")
    color2 = random.choice([Fore.RED, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])
    print(centrar_texto(color2 + banner_title2 + Style.RESET_ALL, ancho_terminal))
    time.sleep(0.2)
    tagline = "Donde la Inteligencia se Encuentra con el Mercado"
    print(random.choice([Fore.MAGENTA, Fore.CYAN, Fore.GREEN, Fore.YELLOW]) + tagline.center(ancho_terminal) + Style.RESET_ALL)
    time.sleep(0.2)
    dev_info = "Developer ING. Juan Carlos M. N."
    print(random.choice([Fore.GREEN, Fore.BLUE, Fore.CYAN]) + dev_info.center(ancho_terminal) + Style.RESET_ALL)
    time.sleep(0.2)
    # Mostrar términos de uso
    terminos = (
        "TÉRMINOS DE USO Y CONDICIONES:\n"
        "El uso de este software es bajo su propia responsabilidad.\n"
        "El desarrollador no se hace responsable por ninguna pérdida monetaria.\n"
        "Se distribuye sin garantía de ningún tipo. Utilízalo bajo tu propio riesgo.\n"
        "Responsabilidad y deslinde: El usuario acepta que el desarrollador no asume responsabilidad\n"
        "por cualquier daño o pérdida derivada del uso de este software.\n\n"
        "Al presionar S, aceptas estos términos. Si presionas N, el programa se cerrará."
    )
    borde = "*" * ancho_terminal
    print("\n" + random.choice([Fore.WHITE, Fore.YELLOW, Fore.CYAN]) + borde)
    print(centrar_texto(terminos, ancho_terminal))
    print(borde + Style.RESET_ALL)
    # Solicitar aceptación de términos
    if solicitar_sn("\n¿Acepta los Términos de Uso y Condiciones? (S/N): ") != "s":
        print(Fore.RED + "No se aceptaron los términos. Saliendo..." + Style.RESET_ALL)
        sys.exit(0)
    # Datos adicionales
    print("\n" + Fore.CYAN + "Datos obtenidos de: Binance, Coinbase, Kraken, Bybit y OKX.".center(ancho_terminal) + Style.RESET_ALL)
    print("\n" + Fore.MAGENTA + "« Plataforma de Análisis de Mercado en Tiempo Real »".center(ancho_terminal) + Style.RESET_ALL)
    # Se utiliza la función de frase motivadora desde utils
    frase = f"Frase del día: {utils.frase_motivadora()}"
    print(random.choice([Fore.LIGHTMAGENTA_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTGREEN_EX]) + centrar_texto(frase, ancho_terminal) + Style.RESET_ALL)
