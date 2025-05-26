TAMANO_TABLERO = 15

def crear_tablero():
    return [["" for _ in range(TAMANO_TABLERO)] for _ in range(TAMANO_TABLERO)]

def puede_colocar(palabra, tablero, fila, col, direccion):
    for i, letra in enumerate(palabra):
        f = fila + (i if direccion == "V" else 0)
        c = col + (i if direccion == "H" else 0)

        if f < 0 or c < 0 or f >= TAMANO_TABLERO or c >= TAMANO_TABLERO:
            return False

        actual = tablero[f][c]
        if actual != "" and actual != letra:
            return False
    return True

def colocar_palabra(palabra, tablero, fila, col, direccion):
    for i, letra in enumerate(palabra):
        f = fila + (i if direccion == "V" else 0)
        c = col + (i if direccion == "H" else 0)
        tablero[f][c] = letra

def buscar_cruce(palabra, tablero, direccion):
    for i, letra in enumerate(palabra):
        for f in range(TAMANO_TABLERO):
            for c in range(TAMANO_TABLERO):
                if tablero[f][c] == letra:
                    fila = f - (i if direccion == "V" else 0)
                    col = c - (i if direccion == "H" else 0)
                    if puede_colocar(palabra, tablero, fila, col, direccion):
                        return fila, col
    return None

def generar_crucigrama(palabras_con_pistas):
    tablero = crear_tablero()
    posiciones = []

    for idx, entrada in enumerate(palabras_con_pistas):
        palabra = entrada["respuesta"].upper()
        direccion = entrada.get("direccion", "H")

        colocada = False

        if idx == 0:
            # Primera palabra va al centro
            fila = TAMANO_TABLERO // 2
            col = (TAMANO_TABLERO - len(palabra)) // 2
            if puede_colocar(palabra, tablero, fila, col, direccion):
                colocar_palabra(palabra, tablero, fila, col, direccion)
                posiciones.append({
                    "palabra": palabra,
                    "fila": fila,
                    "col": col,
                    "direccion": direccion
                })
                colocada = True
        else:
            cruce = buscar_cruce(palabra, tablero, direccion)
            if cruce:
                fila, col = cruce
                colocar_palabra(palabra, tablero, fila, col, direccion)
                posiciones.append({
                    "palabra": palabra,
                    "fila": fila,
                    "col": col,
                    "direccion": direccion
                })
                colocada = True

        if not colocada:
            print(f"❌ No se pudo colocar: {palabra}")

    return tablero, posiciones
