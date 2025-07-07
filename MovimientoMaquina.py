# Funcion para generar los movimientos posibles para el yoshi
def generar_movimientos(yoshi_pos, painted_cells, otro_yoshi_pos):
    movimientos = []
    deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
              (1, -2), (1, 2), (2, -1), (2, 1)]
    
    for dx, dy in deltas:
        x = yoshi_pos[0] + dx
        y = yoshi_pos[1] + dy
        # Verifica que el movimiento posible este dentro del tablero de juego 
        if 0 <= x < 8 and 0 <= y < 8:
            # Verifica que no esté pintada y no sea la posición del otro Yoshi
            if (x, y) not in painted_cells and (x, y) != otro_yoshi_pos:
                movimientos.append((x, y))
    return movimientos

# Estimación de distancia para movimiento de caballo
def distancia_caballo(pos1, pos2):
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])
    return max(dx/2, dy/2)

# Retorna las celdas de zonas especiales que no han sido pintadas
def obtener_celdas_especiales_no_pintadas(painted_cells, especiales):
    celdas_no_pintadas = []
    for zona in especiales.values():
        for celda in zona:
            if celda not in painted_cells:
                celdas_no_pintadas.append(celda)
    
    return celdas_no_pintadas

# Heuristica del programa
def evaluar_estado(painted_cells, especiales, green_pos, red_pos):

    puntaje = 0
    # 1. Puntos por control de zonas (mayor peso)
    for zona in especiales.values():
        verde = 0
        rojo = 0
        for celda in zona:
            if celda in painted_cells:
                if painted_cells[celda] == "green":
                    verde += 1
                else:
                    rojo += 1
        
        if verde > rojo:
            puntaje += 2
        elif rojo > verde:
            puntaje -= 2
    
    # 2. Movilidad (número de movimientos posibles)
    mov_verde = len(generar_movimientos(green_pos, painted_cells, red_pos))
    mov_rojo = len(generar_movimientos(red_pos, painted_cells, green_pos))
    puntaje += 0.1 * (mov_verde - mov_rojo)
    
    # 3. Distancia a celdas especiales no pintadas
    for celda in obtener_celdas_especiales_no_pintadas(painted_cells, especiales):
        dist_verde = distancia_caballo(green_pos, celda)
        dist_rojo = distancia_caballo(red_pos, celda)
        puntaje += 0.3 * (dist_rojo - dist_verde)
    
    return puntaje

def minimax(especiales, painted_cells, green_pos, red_pos, profundidad, es_maximizador, alpha=-float('inf'), beta=float('inf')):
    # Condición de terminación mejorada
    if es_maximizador:
        yoshi_active = green_pos
        yoshi_desactive = red_pos
    else: 
        yoshi_active = red_pos
        yoshi_desactive = green_pos

    movimientos = generar_movimientos(yoshi_active, painted_cells, yoshi_desactive )
    
    if profundidad < 0 or not movimientos:
        return evaluar_estado(painted_cells, especiales, green_pos, red_pos), None

    if es_maximizador:  # Turno del Yoshi verde (Maximiza)
        mejor_valor = -float('inf')
        mejor_movimiento = None
        print("Verde: " + str(movimientos))

        for mov in movimientos:
            nuevo_painted = painted_cells.copy()
            for zona in especiales.values():
                if mov in zona:
                    nuevo_painted[mov] = "green"
            
            valor, _ = minimax(especiales, nuevo_painted, mov, red_pos, profundidad - 1, False, alpha, beta)

            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = mov
                alpha = max(alpha, mejor_valor)

            if beta <= alpha:
                break
                
        return mejor_valor, mejor_movimiento

    else:  # Turno del Yoshi rojo (Minimiza)
        mejor_valor = float('inf')
        mejor_movimiento = None
        print("Rojo: " + str(movimientos)+ '\n')

        for mov in movimientos:
            nuevo_painted = painted_cells.copy()
            
            for zona in especiales.values():
                if mov in zona:
                    nuevo_painted[mov] = "red"
            
            valor, _ = minimax(especiales, nuevo_painted, green_pos, mov, profundidad - 1, True, alpha, beta)

            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = mov
                beta = min(beta, mejor_valor)
            
            if beta <= alpha:
                break
                
        return mejor_valor, mejor_movimiento


def MovimientoMaquina(especiales, painted_cells, green_pos, red_pos, depth):
    # --- Ejecutar Minimax ---
    print(green_pos)
    mejor_valor, mejor_movimiento = minimax(especiales,painted_cells, green_pos, red_pos, depth, es_maximizador=True)
    print(mejor_movimiento)
    print(mejor_valor)
    return mejor_movimiento
    

#Ejemplos
MovimientoMaquina({'top_left': [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)], 
                   'top_right': [(0, 7), (0, 6), (0, 5), (1, 7), (2, 7)], 
                   'bottom_left': [(7, 0), (7, 1), (7, 2), (6, 0), (5, 0)], 
                   'bottom_right': [(7, 7), (7, 6), (7, 5), (6, 7), (5, 7)]},
                   {},(7, 5),(1, 1),2)