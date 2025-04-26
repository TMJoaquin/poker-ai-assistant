# === Clasificar fuerza de mano ===
def clasificar_mano(carta1, carta2):
    mano = {carta1, carta2}
    
    premium = [{"A♠", "A♥"}, {"K♠", "K♥"}, {"Q♠", "Q♥"}, {"A♠", "K♠"}, {"A♥", "K♥"}]
    fuerte = [{"J♠", "J♥"}, {"T♠", "T♥"}, {"A♠", "Q♠"}, {"A♥", "Q♥"}, {"A♠", "K♥"}, {"A♥", "K♠"}]
    medio = [{"9♠", "9♥"}, {"8♠", "8♥"}, {"A♠", "T♠"}, {"A♥", "T♥"}, {"K♠", "Q♠"}, {"K♥", "Q♥"}]
    
    if any(mano == combo for combo in premium):
        return "Premium"
    elif any(mano == combo for combo in fuerte):
        return "Fuerte"
    elif any(mano == combo for combo in medio):
        return "Medio"
    else:
        return "Débil"

# === Recomendación Preflop ===
def recomendar_accion(carta1, carta2, acciones_previas, nivel_mesa, stack_propio):
    fuerza = clasificar_mano(carta1, carta2)

    nivel_bb = {"NL2": 0.01, "NL5": 0.02, "NL10": 0.05, "NL25": 0.10}
    bb_value = nivel_bb.get(nivel_mesa, 0.05)

    bote = 1.5 * bb_value
    for accion in acciones_previas:
        if accion['accion'] == "Limp":
            bote += 1 * bb_value
        elif accion['accion'] == "Raise":
            bote += accion['size'] * bb_value

    if fuerza == "Premium":
        return {"accion": "Raise", "tamaño_bb": 3.0, "monto": 3.0 * bb_value}
    elif fuerza == "Fuerte":
        if any(a['accion'] == "Raise" for a in acciones_previas):
            return {"accion": "Call", "monto": bb_value * 3}
        else:
            return {"accion": "Raise", "tamaño_bb": 2.5, "monto": 2.5 * bb_value}
    elif fuerza == "Medio":
        if any(a['accion'] == "Raise" for a in acciones_previas):
            return {"accion": "Fold"}
        else:
            return {"accion": "Call", "monto": bb_value}
    else:
        return {"accion": "Fold"}

# === Recomendación Flop ===
def recomendar_accion_flop(carta1, carta2, flop, acciones_flop, nivel_mesa, stack_propio):
    nivel_bb = {"NL2": 0.01, "NL5": 0.02, "NL10": 0.05, "NL25": 0.10}
    bb_value = nivel_bb.get(nivel_mesa, 0.05)

    bote = 1.5 * bb_value
    for accion in acciones_flop.values():
        if accion == "Bet pequeño":
            bote += 0.3 * bote
        elif accion == "Bet medio":
            bote += 0.5 * bote
        elif accion == "Bet pot":
            bote += 1.0 * bote
        elif accion == "All-in":
            bote += stack_propio

    fuerza = clasificar_mano(carta1, carta2)

    if fuerza == "Premium":
        accion = "Bet fuerte"
        porcentaje_bote = 0.7
    elif fuerza == "Fuerte":
        accion = "Bet medio"
        porcentaje_bote = 0.5
    elif fuerza == "Medio":
        accion = "Bet pequeño o Check"
        porcentaje_bote = 0.3
    else:
        accion = "Check o Fold"
        porcentaje_bote = 0.0

    monto = porcentaje_bote * bote if porcentaje_bote > 0 else 0

    return {"accion": accion, "monto": monto, "bote_estimado": bote}

# === Recomendación Turn ===
def recomendar_accion_turn(carta1, carta2, flop, turn, acciones_flop, acciones_turn, nivel_mesa, stack_propio):
    nivel_bb = {"NL2": 0.01, "NL5": 0.02, "NL10": 0.05, "NL25": 0.10}
    bb_value = nivel_bb.get(nivel_mesa, 0.05)

    bote = 1.5 * bb_value
    for accion in acciones_flop.values():
        if accion == "Bet pequeño":
            bote += 0.3 * bote
        elif accion == "Bet medio":
            bote += 0.5 * bote
        elif accion == "Bet pot":
            bote += 1.0 * bote
        elif accion == "All-in":
            bote += stack_propio

    for accion in acciones_turn.values():
        if accion == "Bet pequeño":
            bote += 0.3 * bote
        elif accion == "Bet medio":
            bote += 0.5 * bote
        elif accion == "Bet pot":
            bote += 1.0 * bote
        elif accion == "All-in":
            bote += stack_propio

    fuerza = clasificar_mano(carta1, carta2)

    if fuerza == "Premium":
        accion = "Bet fuerte"
        porcentaje_bote = 0.7
    elif fuerza == "Fuerte":
        accion = "Bet medio"
        porcentaje_bote = 0.5
    elif fuerza == "Medio":
        accion = "Bet pequeño o Check"
        porcentaje_bote = 0.3
    else:
        accion = "Check o Fold"
        porcentaje_bote = 0.0

    monto = porcentaje_bote * bote if porcentaje_bote > 0 else 0

    return {"accion": accion, "monto": monto, "bote_estimado": bote}

# === Recomendación River ===
def recomendar_accion_river(carta1, carta2, flop, turn, river, acciones_flop, acciones_turn, acciones_river, nivel_mesa, stack_propio):
    nivel_bb = {"NL2": 0.01, "NL5": 0.02, "NL10": 0.05, "NL25": 0.10}
    bb_value = nivel_bb.get(nivel_mesa, 0.05)

    bote = 1.5 * bb_value
    for accion in acciones_flop.values():
        if accion == "Bet pequeño":
            bote += 0.3 * bote
        elif accion == "Bet medio":
            bote += 0.5 * bote
        elif accion == "Bet pot":
            bote += 1.0 * bote
        elif accion == "All-in":
            bote += stack_propio

    for accion in acciones_turn.values():
        if accion == "Bet pequeño":
            bote += 0.3 * bote
        elif accion == "Bet medio":
            bote += 0.5 * bote
        elif accion == "Bet pot":
            bote += 1.0 * bote
        elif accion == "All-in":
            bote += stack_propio

    for accion in acciones_river.values():
        if accion == "Bet pequeño":
            bote += 0.3 * bote
        elif accion == "Bet medio":
            bote += 0.5 * bote
        elif accion == "Bet pot":
            bote += 1.0 * bote
        elif accion == "All-in":
            bote += stack_propio

    fuerza = clasificar_mano(carta1, carta2)

    if fuerza == "Premium":
        accion = "Bet fuerte"
        porcentaje_bote = 0.7
    elif fuerza == "Fuerte":
        accion = "Bet medio"
        porcentaje_bote = 0.5
    elif fuerza == "Medio":
        accion = "Bet pequeño o Check"
        porcentaje_bote = 0.3
    else:
        accion = "Check o Fold"
        porcentaje_bote = 0.0

    monto = porcentaje_bote * bote if porcentaje_bote > 0 else 0

    return {"accion": accion, "monto": monto, "bote_estimado": bote}