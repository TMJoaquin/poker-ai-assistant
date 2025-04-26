# === Función para clasificar fuerza de tu mano ===
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

# === Función de análisis de contexto y recomendación IA ===
def recomendar_accion(carta1, carta2, acciones_previas, nivel_mesa, stack_propio):
    fuerza = clasificar_mano(carta1, carta2)

    nivel_bb = {
        "NL2": 0.01,
        "NL5": 0.02,
        "NL10": 0.05,
        "NL25": 0.10
    }
    bb_value = nivel_bb.get(nivel_mesa, 0.05)

    # Calcular tamaño del bote
    bote = 1.5 * bb_value  # Blinds iniciales
    for accion in acciones_previas:
        if accion['accion'] == "Limp":
            bote += 1 * bb_value
        elif accion['accion'] == "Raise":
            bote += accion['size'] * bb_value

    # Calcular stack efectivo (simplificado ahora como tu propio stack)
    stack_efectivo = stack_propio

    # Lógica de recomendación basada en fuerza de mano
    if fuerza == "Premium":
        return {
            "accion": "Raise",
            "tamaño_bb": 3.0,
            "monto": 3.0 * bb_value
        }
    elif fuerza == "Fuerte":
        if any(a['accion'] == "Raise" for a in acciones_previas):
            return {
                "accion": "Call",
                "monto": bb_value * 3
            }
        else:
            return {
                "accion": "Raise",
                "tamaño_bb": 2.5,
                "monto": 2.5 * bb_value
            }
    elif fuerza == "Medio":
        if any(a['accion'] == "Raise" for a in acciones_previas):
            return {
                "accion": "Fold"
            }
        else:
            return {
                "accion": "Call",
                "monto": bb_value
            }
    else:  # Débil
        return {
            "accion": "Fold"
        }

# === Función para recomendar acción en el Flop ===
def recomendar_accion_flop(carta1, carta2, flop, acciones_flop, nivel_mesa, stack_propio):
    nivel_bb = {
        "NL2": 0.01,
        "NL5": 0.02,
        "NL10": 0.05,
        "NL25": 0.10
    }
    bb_value = nivel_bb.get(nivel_mesa, 0.05)

    # Calcular tamaño base del bote preflop (blinds)
    bote = 1.5 * bb_value

    # Agregar acciones de Flop
    for accion in acciones_flop.values():
        if accion == "Bet pequeño":
            bote += 0.3 * bote
        elif accion == "Bet medio":
            bote += 0.5 * bote
        elif accion == "Bet pot":
            bote += 1.0 * bote
        elif accion == "All-in":
            bote += stack_propio  # Simplificamos

    # Evaluar fuerza de mano en el Flop (por ahora basado en fuerza inicial)
    fuerza = clasificar_mano(carta1, carta2)

    # Recomendación basada en fuerza
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

    return {
        "accion": accion,
        "monto": monto,
        "bote_estimado": bote
    }


# === Función para recomendar acción en el Turn ===
def recomendar_accion_turn(carta1, carta2, flop, turn, acciones_flop, acciones_turn, nivel_mesa, stack_propio):
    nivel_bb = {
        "NL2": 0.01,
        "NL5": 0.02,
        "NL10": 0.05,
        "NL25": 0.10
    }
    bb_value = nivel_bb.get(nivel_mesa, 0.05)

    # Calcular bote real hasta el Turn
    bote = 1.5 * bb_value  # Blinds iniciales

    # Acciones preflop (simplificado ahora)
    # (Podríamos pasar también acciones_preflop si quieres hacerlo ultra preciso luego)

    # Acciones Flop
    for accion in acciones_flop.values():
        if accion == "Bet pequeño":
            bote += 0.3 * bote
        elif accion == "Bet medio":
            bote += 0.5 * bote
        elif accion == "Bet pot":
            bote += 1.0 * bote
        elif accion == "All-in":
            bote += stack_propio

    # Acciones Turn
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

    return {
        "accion": accion,
        "monto": monto,
        "bote_estimado": bote
    }

# === Función para recomendar acción en el River ===
def recomendar_accion_river(carta1, carta2, flop, turn, river, acciones_flop, acciones_turn, acciones_river, nivel_mesa, stack_propio):
    nivel_bb = {
        "NL2": 0.01,
        "NL5": 0.02,
        "NL10": 0.05,
        "NL25": 0.10
    }
    bb_value = nivel_bb.get(nivel_mesa, 0.05)

    # Calcular bote real hasta River
    bote = 1.5 * bb_value  # Blinds iniciales

    # Acciones Flop
    for accion in acciones_flop.values():
        if accion == "Bet pequeño":
            bote += 0.3 * bote
        elif accion == "Bet medio":
            bote += 0.5 * bote
        elif accion == "Bet pot":
            bote += 1.0 * bote
        elif accion == "All-in":
            bote += stack_propio

    # Acciones Turn
    for accion in acciones_turn.values():
        if accion == "Bet pequeño":
            bote += 0.3 * bote
        elif accion == "Bet medio":
            bote += 0.5 * bote
        elif accion == "Bet pot":
            bote += 1.0 * bote
        elif accion == "All-in":
            bote += stack_propio

    # Acciones River
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

    return {
        "accion": accion,
        "monto": monto,
        "bote_estimado": bote
    }
