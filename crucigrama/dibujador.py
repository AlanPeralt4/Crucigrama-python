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

    # Separar pistas y numerarlas individualmente
    horizontales = []
    verticales = []
    num_horizontal = 1
    num_vertical = 1
    numeracion = {}

    for i, entrada in enumerate(palabras_con_pistas):
        direccion = entrada["direccion"]
        if direccion == "H":
            numeracion[i] = num_horizontal
            horizontales.append((num_horizontal, entrada["pista"]))
            num_horizontal += 1
        else:
            numeracion[i] = num_vertical
            verticales.append((num_vertical, entrada["pista"]))
            num_vertical += 1

    # Mostrar pistas
    tk.Label(pista_frame, text="Horizontales", font=("Arial", 12, "bold")).pack(anchor="w")
    for num, pista in horizontales:
        tk.Label(pista_frame, text=f"{num}. {pista}", wraplength=300, anchor="w", justify="left").pack(anchor="w")

    tk.Label(pista_frame, text="Verticales", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 0))
    for num, pista in verticales:
        tk.Label(pista_frame, text=f"{num}. {pista}", wraplength=300, anchor="w", justify="left").pack(anchor="w")

    # Matriz de uso
    tablero_usado = [[False for _ in range(columnas)] for _ in range(filas)]
    celdas = {}

    # Marcar celdas ocupadas
    for pos in posiciones:
        palabra = pos["palabra"]
        f, c = pos["fila"], pos["col"]
        d = pos["direccion"]
        for i in range(len(palabra)):
            ff = f + (i if d == "V" else 0)
            cc = c + (i if d == "H" else 0)
            tablero_usado[ff][cc] = True

    # Dibujar palabras
    for idx, pos in enumerate(posiciones):
        palabra = pos["palabra"]
        fila = pos["fila"]
        col = pos["col"]
        direccion = pos["direccion"]
        num = numeracion[idx]

        # Determinar dónde dibujar el número (si se puede)
        if direccion == "H" and col > 0 and not tablero_usado[fila][col - 1]:
            x = (col - 1) * TAMANO_CELDA
            y = fila * TAMANO_CELDA
            canvas.create_text(x + 5, y + 5, anchor="nw", text=str(num), font=("Arial", 10, "bold"))
        elif direccion == "V" and fila > 0 and not tablero_usado[fila - 1][col]:
            x = col * TAMANO_CELDA
            y = (fila - 1) * TAMANO_CELDA
            canvas.create_text(x + 5, y + 5, anchor="nw", text=str(num), font=("Arial", 10, "bold"))

        # Dibujar la palabra
        for i in range(len(palabra)):
            f = fila + (i if direccion == "V" else 0)
            c = col + (i if direccion == "H" else 0)
            x0 = c * TAMANO_CELDA
            y0 = f * TAMANO_CELDA
            x1 = x0 + TAMANO_CELDA
            y1 = y0 + TAMANO_CELDA

            # Dibujar cuadrado blanco con borde negro
            canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")

            # Crear campo de entrada
            entry = tk.Entry(ventana, width=1, font=("Consolas", 18), justify="center", bg="white", relief="flat")
            entry.place(x=x0 + 1, y=y0 + 1, width=TAMANO_CELDA - 2, height=TAMANO_CELDA - 2)

            def limitar_entrada(event, e=entry):
                texto = e.get().upper()
                if len(texto) > 1 or not texto.isalpha():
                    e.delete(0, tk.END)

            entry.bind("<KeyRelease>", limitar_entrada)
            celdas[(f, c)] = (entry, palabra[i])

    # Verificación
    def verificar():
        for (f, c), (entry, correcta) in celdas.items():
            ingresada = entry.get().upper()
            if ingresada == correcta:
                entry.config(bg="#c8facc")
            else:
                entry.config(bg="#fbb")

    tk.Button(pista_frame, text="Verificar", command=verificar).pack(pady=20)

    ventana.mainloop()
