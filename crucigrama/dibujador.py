import tkinter as tk

TAMANO_CELDA = 40

def dibujar_crucigrama(tablero, posiciones, palabras_con_pistas):
    filas = len(tablero)
    columnas = len(tablero[0])

    ventana = tk.Tk()
    ventana.title("Crucigrama Interactivo")

    canvas = tk.Canvas(ventana, width=columnas * TAMANO_CELDA, height=filas * TAMANO_CELDA, bg="#d3d3d3")
    canvas.pack(side=tk.LEFT)

    pista_frame = tk.Frame(ventana, padx=10)
    pista_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Contadores separados
    pistas_horizontales = []
    pistas_verticales = []
    numeracion_map = {}

    num_h = 1
    num_v = 1

    for pos in posiciones:
        idx = pos["numero"] - 1  # corresponde al índice en el JSON
        pista = palabras_con_pistas[idx]["pista"]
        direccion = pos["direccion"]

        if direccion == "H":
            numeracion_map[(pos["fila"], pos["col"], "H")] = num_h
            pistas_horizontales.append((num_h, pista))
            num_h += 1
        else:
            numeracion_map[(pos["fila"], pos["col"], "V")] = num_v
            pistas_verticales.append((num_v, pista))
            num_v += 1

    # Mostrar pistas
    tk.Label(pista_frame, text="Horizontales", font=("Arial", 12, "bold")).pack(anchor="w")
    for num, pista in pistas_horizontales:
        tk.Label(pista_frame, text=f"{num}. {pista}", wraplength=300, anchor="w", justify="left").pack(anchor="w")

    tk.Label(pista_frame, text="Verticales", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 0))
    for num, pista in pistas_verticales:
        tk.Label(pista_frame, text=f"{num}. {pista}", wraplength=300, anchor="w", justify="left").pack(anchor="w")

    tablero_usado = [[False for _ in range(columnas)] for _ in range(filas)]
    celdas = {}

    for pos in posiciones:
        palabra = pos["palabra"]
        f = pos["fila"]
        c = pos["col"]
        d = pos["direccion"]

        for i in range(len(palabra)):
            ff = f + (i if d == "V" else 0)
            cc = c + (i if d == "H" else 0)
            tablero_usado[ff][cc] = True

    for pos in posiciones:
        palabra = pos["palabra"]
        fila = pos["fila"]
        col = pos["col"]
        direccion = pos["direccion"]
        numero = numeracion_map.get((fila, col, direccion), None)

        # Dibujar número fuera de la celda si hay espacio
        if numero:
            if direccion == "H" and col > 0 and not tablero_usado[fila][col - 1]:
                x = (col - 1) * TAMANO_CELDA
                y = fila * TAMANO_CELDA
                canvas.create_text(x + 5, y + 5, anchor="nw", text=str(numero), font=("Arial", 10, "bold"))
            elif direccion == "V" and fila > 0 and not tablero_usado[fila - 1][col]:
                x = col * TAMANO_CELDA
                y = (fila - 1) * TAMANO_CELDA
                canvas.create_text(x + 5, y + 5, anchor="nw", text=str(numero), font=("Arial", 10, "bold"))

        for i in range(len(palabra)):
            f = fila + (i if direccion == "V" else 0)
            c = col + (i if direccion == "H" else 0)
            x0 = c * TAMANO_CELDA
            y0 = f * TAMANO_CELDA
            x1 = x0 + TAMANO_CELDA
            y1 = y0 + TAMANO_CELDA

            canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")

            entry = tk.Entry(ventana, width=1, font=("Consolas", 18), justify="center", bg="white", relief="flat")
            entry.place(x=x0 + 1, y=y0 + 1, width=TAMANO_CELDA - 2, height=TAMANO_CELDA - 2)

            def limitar_entrada(event, e=entry):
                texto = e.get().upper()
                if len(texto) > 1 or not texto.isalpha():
                    e.delete(0, tk.END)

            entry.bind("<KeyRelease>", limitar_entrada)
            celdas[(f, c)] = (entry, palabra[i])

    def verificar():
        for (f, c), (entry, correcta) in celdas.items():
            ingresada = entry.get().upper()
            if ingresada == correcta:
                entry.config(bg="#c8facc")
            else:
                entry.config(bg="#fbb")

    tk.Button(pista_frame, text="Verificar", command=verificar).pack(pady=20)
    ventana.mainloop()
