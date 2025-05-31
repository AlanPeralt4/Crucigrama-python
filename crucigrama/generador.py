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
    palabra = palabra.upper()
    for i, letra in enumerate(palabra):
        if letra == "Ñ":
            continue

        for f in range(TAMANO_TABLERO):
            for c in range(TAMANO_TABLERO):
                if tablero[f][c] == letra:
                    fila = f - (i if direccion == "V" else 0)
                    col = c - (i if direccion == "H" else 0)
                    if puede_colocar(palabra, tablero, fila, col, direccion):
                        return fila, col
    return None

def hay_espacio_para_numero(fila, col, direccion, tablero):
    if direccion == "H":
        return col > 0 and tablero[fila][col - 1] == ""
    elif direccion == "V":
        return fila > 0 and tablero[fila - 1][col] == ""
    return False

def generar_crucigrama(palabras_con_pistas):
    tablero = crear_tablero()
    posiciones = []

    for idx, entrada in enumerate(palabras_con_pistas):
        palabra = entrada["respuesta"].upper()
        direccion = entrada.get("direccion", "H")

        colocada = False

        if idx == 0:
            fila = TAMANO_TABLERO // 2
            col = (TAMANO_TABLERO - len(palabra)) // 2
            if not hay_espacio_para_numero(fila, col, direccion, tablero):
                if direccion == "H":
                    col += 1
                else:
                    fila += 1
            if puede_colocar(palabra, tablero, fila, col, direccion):
                colocar_palabra(palabra, tablero, fila, col, direccion)
                posiciones.append({
                    "palabra": palabra,
                    "fila": fila,
                    "col": col,
                    "direccion": direccion,
                    "numero": idx + 1
                })
                colocada = True
        else:
            cruce = buscar_cruce(palabra, tablero, direccion)
            if cruce:
                fila, col = cruce
                if not hay_espacio_para_numero(fila, col, direccion, tablero):
                    if direccion == "H":
                        col += 1
                    else:
                        fila += 1
                if puede_colocar(palabra, tablero, fila, col, direccion):
                    colocar_palabra(palabra, tablero, fila, col, direccion)
                    posiciones.append({
                        "palabra": palabra,
                        "fila": fila,
                        "col": col,
                        "direccion": direccion,
                        "numero": idx + 1
                    })
                    colocada = True

        if not colocada:
            print(f"❌ No se pudo colocar: {palabra}")

    return tablero, posiciones
