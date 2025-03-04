#!/usr/bin/env python3
"""
Instrucciones y Resumen del Proyecto Modularizado

Este proyecto ha sido reorganizado en varios módulos para facilitar su mantenimiento y escalabilidad.
A continuación, se detalla la estructura de carpetas y la función de cada módulo:

Estructura de Carpetas:
------------------------
wt_proyecto/                   <- Carpeta principal del proyecto
│
├── main.py                  <- Menú principal e integración de módulos
├── presentacion.py          <- BLOQUE 1: Presentación con logo y términos de uso
├── configuracion.py         <- BLOQUE 2 y 6: Variables globales y configuración de APIs
├── datos_mercado.py         <- BLOQUES 3, 4, 5, 7, 8 y 9: Funciones de obtención y validación de datos de mercado
├── analisis.py              <- BLOQUES 10, 11, 13, 16, 18, 19, 21 y 23: Análisis, indicadores, backtesting y selección de criptomonedas
├── trading.py               <- BLOQUE 14: Funciones de trading automatizado y creación de órdenes
├── soporte.py               <- BLOQUE 22: Soporte, FAQ y mensajes de ayuda
└── utils.py                 <- Funciones utilitarias comunes (limpiar pantalla, cuenta regresiva, frases motivadoras, etc.)

Cómo Funciona:
--------------
1. **main.py** actúa como controlador central. Muestra el menú principal y, según la opción seleccionada, llama a las funciones de los demás módulos.
2. **presentacion.py** muestra el logo, términos de uso y solicita la aceptación al inicio (BLOQUE 1).
3. **configuracion.py** define variables globales y gestiona la configuración de APIs (BLOQUES 2 y 6).
4. **datos_mercado.py** se encarga de la obtención y procesamiento de datos de mercado (BLOQUES 3, 4, 5, 7, 8 y 9).
5. **analisis.py** contiene las funciones de análisis técnico, backtesting y obtención de datos del usuario (BLOQUES 10, 11, 13, 16, 18, 19, 21 y 23).
6. **trading.py** implementa las funciones para realizar operaciones de trading automatizado (BLOQUE 14).
7. **soporte.py** muestra mensajes de soporte y ayuda al usuario (BLOQUE 22).
8. **utils.py** incluye funciones comunes utilizadas en varios módulos.

Instrucciones para Modificaciones:
-----------------------------------
- Cada módulo conserva los comentarios y la numeración de bloques tal como en el código original (por ejemplo, "# BLOQUE 1", "# BLOQUE 2", etc.).
- Si realizas cambios en nombres o funciones, actualiza las importaciones correspondientes en **main.py** y en el módulo afectado.
- Para agregar nuevas estrategias o funcionalidades, puedes crear nuevos bloques dentro del módulo correspondiente (por ejemplo, en **analisis.py** para nuevos análisis).
- Se recomienda utilizar un sistema de control de versiones (como Git) para poder revertir cambios en caso de errores.
- Asegúrate de que la comunicación entre módulos se mantenga a través de las funciones definidas.

Ejemplo de Ejecución:
---------------------
Para ejecutar el proyecto, desde la carpeta principal (wt_proyecto) ejecuta:

    python main.py

Este comando iniciará el menú principal, donde podrás seleccionar las diferentes opciones (análisis, trading, backtesting, etc.).

Este archivo sirve como guía y documentación interna para el mantenimiento y extensión del proyecto.

Fin del Resumen y las Instrucciones.
"""

def main():
    print("Consulta el archivo 'instructions_summary.py' para ver la documentación completa del proyecto modularizado.")

if __name__ == "__main__":
    main()
