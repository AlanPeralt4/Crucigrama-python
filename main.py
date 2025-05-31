import json
from crucigrama.generador import generar_crucigrama
from crucigrama.dibujador import dibujar_crucigrama

# Leer las palabras desde palabras.json
with open("palabras.json", "r", encoding="utf-8") as f:
    palabras_con_pistas = json.load(f)

# Generar tablero y posiciones
matriz, posiciones = generar_crucigrama(palabras_con_pistas)
#hola basuras
# Mostrar la GUI interactiva
dibujar_crucigrama(matriz, posiciones, palabras_con_pistas)
