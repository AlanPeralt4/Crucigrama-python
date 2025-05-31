import json
from crucigrama.generador import generar_crucigrama
from crucigrama.dibujador import dibujar_crucigrama


def cargar_palabras(ruta):
    """Carga las palabras con sus pistas desde un archivo JSON."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def main():
    """Función principal del programa."""
    ruta_palabras = "palabras.json"
    palabras_con_pistas = cargar_palabras(ruta_palabras)

    matriz, posiciones = generar_crucigrama(palabras_con_pistas)
    dibujar_crucigrama(matriz, posiciones, palabras_con_pistas)


if __name__ == "__main__":
    main()

