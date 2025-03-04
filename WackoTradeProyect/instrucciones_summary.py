#!/usr/bin/env python3
"""
instructions_summary.py: Instrucciones y Resumen del Proyecto Modularizado

Estructura del Proyecto:
------------------------
wt_proyecto/                   <- Carpeta principal del proyecto
│
├── main.py                  <- Menú principal e integración de módulos
├── presentacion.py          <- BLOQUE 1: Presentación con logo y términos
├── configuracion.py         <- BLOQUE 2 y 6: Variables globales y configuración de APIs
├── datos_mercado.py         <- BLOQUES 3, 4, 5, 7, 8 y 9: Obtención y validación de datos de mercado
├── analisis.py              <- BLOQUES 10, 11, 13, 16, 18, 19, 21 y 23: Análisis técnico, backtesting y selección de criptomonedas
├── trading.py               <- BLOQUE 14: Funciones de trading automatizado y órdenes
├── soporte.py               <- BLOQUE 22: Soporte y mensajes de ayuda
├── utils.py                 <- Funciones utilitarias comunes (limpiar pantalla, cuenta regresiva, frases motivadoras, etc.)
├── estrategias.py           <- NUEVO: Estrategias de trading inspiradas en CryptoSignal/Crypto-Signal
└── instructions_summary.py  <- Este documento: resumen e instrucciones detalladas del proyecto

Cómo Funciona:
--------------
1. **main.py** actúa como controlador central: muestra el menú principal y llama a funciones de cada módulo.
2. **presentacion.py** muestra el logo, términos de uso y solicita la aceptación (BLOQUE 1).
3. **configuracion.py** define variables globales y gestiona la configuración de APIs (BLOQUES 2 y 6).
4. **datos_mercado.py** se encarga de obtener y procesar datos de mercado (BLOQUES 3, 4, 5, 7, 8 y 9).
5. **analisis.py** contiene funciones de análisis técnico, cálculo de indicadores, backtesting y análisis de tendencias (BLOQUES 10, 11, 13, 16, 18, 19, 21 y 23).
6. **trading.py** implementa el trading automatizado y la creación de órdenes (BLOQUE 14).
7. **soporte.py** muestra mensajes de soporte y ayuda (BLOQUE 22).
8. **utils.py** incluye funciones comunes utilizadas en varios módulos.
9. **estrategias.py** integra estrategias de trading inspiradas en CryptoSignal/Crypto-Signal, permitiendo generar señales basadas en indicadores técnicos.

Instrucciones para Modificaciones:
-----------------------------------
- Cada módulo conserva los comentarios y numeración de bloques del código original.
- Si se realiza un cambio en el nombre de un módulo o función, actualizar las importaciones en **main.py** y en los módulos dependientes.
- Para agregar nuevas estrategias, se puede ampliar **estrategias.py** o crear nuevos módulos según convenga.
- Se recomienda utilizar un sistema de control de versiones (p.ej., Git) para rastrear cambios y revertir en caso de errores.

Ejemplo de Ejecución:
---------------------
Desde la carpeta principal (wt_proyecto), ejecutar:

    python main.py

Esto iniciará el menú principal, desde el cual se pueden seleccionar las diferentes opciones (análisis en tiempo real, trading automatizado, backtesting, integración de estrategias, etc.).

Fin del Resumen e Instrucciones.
"""

def main():
    print("Consulta este archivo 'instructions_summary.py' para ver la documentación completa del proyecto modularizado.")

if __name__ == "__main__":
    main()
