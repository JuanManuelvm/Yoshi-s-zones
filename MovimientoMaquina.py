def generar_movimientos(yoshi_pos, painted_cells, otro_yoshi_pos):
    movimientos = []
    deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
              (1, -2), (1, 2), (2, -1), (2, 1)]
    
    for dx, dy in deltas:
        x, y = yoshi_pos[0] + dx, yoshi_pos[1] + dy
        if 0 <= x < 8 and 0 <= y < 8:
            # Verificar que no esté pintada y no sea la posición del otro Yoshi
            if (x, y) not in painted_cells and (x, y) != otro_yoshi_pos:
                movimientos.append((x, y))
    return movimientos

def distancia_caballo(pos1, pos2):
    """Estimación de distancia para movimiento de caballo"""
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])
    return max(dx/2, dy/2)  # aproximación

def obtener_celdas_especiales_no_pintadas(painted_cells, especiales):
    """
    Retorna las celdas de zonas especiales que no han sido pintadas.
    
    """
    celdas_no_pintadas = []
    
    # Iterar sobre todas las celdas de todas las zonas especiales
    for zona in especiales.values():
        for celda in zona:
            if celda not in painted_cells:
                celdas_no_pintadas.append(celda)
    
    return celdas_no_pintadas

def evaluar_estado(painted_cells, especiales, green_pos, red_pos):
    """
    Heurística mejorada que considera:
    - Control de zonas especiales
    - Movilidad de cada jugador
    - Distancia a zonas no controladas
    """
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
    
    # 3. Distancia a celdas especiales no pintadas (menor peso)
    for celda in obtener_celdas_especiales_no_pintadas(painted_cells, especiales):
        dist_verde = distancia_caballo(green_pos, celda)
        dist_rojo = distancia_caballo(red_pos, celda)
        puntaje += 0.01 * (dist_rojo - dist_verde)  # favorece menor distancia verde
    
    return puntaje

def minimax(especiales, painted_cells, green_pos, red_pos, profundidad, es_maximizador, alpha=-float('inf'), beta=float('inf')):
    # Condición de terminación mejorada
    movimientos = generar_movimientos(green_pos if es_maximizador else red_pos, painted_cells, red_pos if es_maximizador else green_pos)
    
    if profundidad == 0 or not movimientos:
        return evaluar_estado(painted_cells, especiales, green_pos, red_pos), None

    if es_maximizador:  # Turno del Yoshi verde (Maximiza)
        mejor_valor = -float('inf')
        mejor_movimiento = None
        
        for mov in movimientos:
            # Copia el diccionario de celdas pintadas
            nuevo_painted = painted_cells.copy()
            
            # Si el movimiento es a una zona especial, píntala
            for zona in especiales.values():
                if mov in zona:
                    nuevo_painted[mov] = "green"
            
            # Llama recursivamente a minimax
            valor, _ = minimax(especiales, nuevo_painted, mov, red_pos, profundidad - 1, False, alpha, beta)
            
            # Actualiza el mejor movimiento
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = mov
                alpha = max(alpha, mejor_valor)
            
            # Poda alfa-beta
            if beta <= alpha:
                break
                
        return mejor_valor, mejor_movimiento

    else:  # Turno del Yoshi rojo (Minimiza)
        mejor_valor = float('inf')
        mejor_movimiento = None
        
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
    """
    Decide el mejor movimiento para el Yoshi verde usando Minimax con profundidad 2.
    """
  
    # --- Ejecutar Minimax ---
    print(green_pos)
    mejor_valor, mejor_movimiento = minimax(especiales,painted_cells, green_pos, red_pos, depth, es_maximizador=True)
    print(mejor_movimiento)
    print(mejor_valor)
    return mejor_movimiento
    
""""
MovimientoMaquina({'top_left': [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)], 
                   'top_right': [(0, 7), (0, 6), (0, 5), (1, 7), (2, 7)], 
                   'bottom_left': [(7, 0), (7, 1), (7, 2), (6, 0), (5, 0)], 
                   'bottom_right': [(7, 7), (7, 6), (7, 5), (6, 7), (5, 7)]},
                   {},(1, 6),(4, 5))
"""