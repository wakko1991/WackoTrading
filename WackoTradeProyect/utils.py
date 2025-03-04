#!/usr/bin/env python3
"""
utils.py: Funciones utilitarias comunes a todo el proyecto.
"""

import os
import time
from datetime import timedelta
from colorama import Fore, Style
import random
from inputimeout import inputimeout, TimeoutOccurred

def centrar_texto(texto: str, ancho: int = 80) -> str:
    return "\n".join(line.center(ancho) for line in texto.splitlines())

def limpiar_pantalla():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        pass

def input_con_timeout(prompt: str, timeout: int) -> str:
    try:
        return inputimeout(prompt, timeout=timeout)
    except TimeoutOccurred:
        return 'r'

def iniciar_cuenta_regresiva(total_seconds: int):
    while total_seconds:
        hrs, rem = divmod(total_seconds, 3600)
        mins, secs = divmod(rem, 60)
        timer = f"⏳ Trading restante: {hrs:02d}:{mins:02d}:{secs:02d}"
        print(Fore.WHITE + timer + Style.RESET_ALL, end="\r")
        time.sleep(1)
        total_seconds -= 1

def frase_motivadora():
    frases = [
        "El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
        "Cada operación es una lección, no un fracaso.",
        "La perseverancia es la clave del éxito en el trading.",
        "Confía en tu estrategia y sigue adelante.",
        "El riesgo es parte del juego, pero la constancia te lleva a la victoria.",
        "Aprende de cada error y conviértelo en una oportunidad.",
        "El mercado recompensa a los que se preparan.",
        "La disciplina es el puente entre tus metas y tus logros.",
        "Mantente enfocado y evita distracciones en tu camino al éxito.",
        "La paciencia es una virtud que se forja con el tiempo."
    ]
    return random.choice(frases)
