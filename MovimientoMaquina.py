def MovimientoMaquina(movimientos,especiales):
    movimiento = (movimientos[0])
    for i in especiales:
        for y in especiales[i]:
            for n in movimientos:
                if n == y:
                    movimiento = n
    return(movimiento)