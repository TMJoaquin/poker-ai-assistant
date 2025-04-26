import streamlit as st

# Configuración visual
st.set_page_config(page_title="Poker AI Assistant V2", layout="centered")
st.markdown(
    """
    <style>
        .stApp { background-color: #0e1117; color: white; }
        .css-18e3th9 { background-color: #0e1117; }
    </style>
    """,
    unsafe_allow_html=True
)

# === Paso 1: Tipo de mesa ===
if 'step' not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    st.title("♠️ Poker AI Assistant V2 — Paso 1: Tipo de mesa")
    mesa = st.radio("¿Qué tipo de mesa estás jugando?", ["NL2", "NL5", "NL10", "NL25"], horizontal=True)
    if st.button("Siguiente ➝"):
        st.session_state.mesa = mesa
        st.session_state.step = 2

# === Paso 2: Tu posición ===
elif st.session_state.step == 2:
    st.title("Paso 2: Tu posición")
    posicion = st.radio("¿Dónde estás sentado?", ["UTG", "MP", "CO", "BTN", "SB", "BB"], horizontal=True)
    if st.button("Siguiente ➝"):
        st.session_state.posicion = posicion
        st.session_state.step = 3

# === Paso 3: Tus cartas ===
elif st.session_state.step == 3:
    st.title("Paso 3: Tus Cartas")
    col1, col2 = st.columns(2)
    with col1:
        carta1 = st.selectbox("Carta 1", ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"])
        palo1 = st.selectbox("Palo 1", ["♠", "♥", "♦", "♣"])
    with col2:
        carta2 = st.selectbox("Carta 2", ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"])
        palo2 = st.selectbox("Palo 2", ["♠", "♥", "♦", "♣"])
    if st.button("Siguiente ➝"):
        st.session_state.carta1 = carta1 + palo1
        st.session_state.carta2 = carta2 + palo2
        st.session_state.step = 4

# === Paso 4: Stack por jugador (uno a uno) ===
elif st.session_state.step == 4:
    if 'stack_index' not in st.session_state:
        st.session_state.stack_index = 0
        st.session_state.stacks = {}

    posiciones = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
    st.title(f"Paso 4: Stack de {posiciones[st.session_state.stack_index]}")
    stack = st.number_input(f"¿Cuánto stack tiene {posiciones[st.session_state.stack_index]}?", min_value=0.01, step=0.01, format="%.2f")
    if st.button("Confirmar stack"):
        st.session_state.stacks[posiciones[st.session_state.stack_index]] = stack
        st.session_state.stack_index += 1
        if st.session_state.stack_index >= len(posiciones):
            st.session_state.step = 5

# === Paso 5: Acciones preflop uno por uno (corregido para tu turno) ===
elif st.session_state.step == 5:
    if 'action_index' not in st.session_state:
        st.session_state.action_index = 0
        st.session_state.acciones = {}

    posiciones = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
    st.title("♠️ Paso 5: Acciones Preflop")

    if st.session_state.action_index < len(posiciones):
        pos_actual = posiciones[st.session_state.action_index]

        # Aquí corregimos:
        if pos_actual == st.session_state.posicion:
            st.session_state.step = 6  # Es tu turno, salta a la recomendación preflop
        else:
            st.subheader(f"Acción de {pos_actual}")
            accion = st.radio(f"¿Qué hace {pos_actual}?", ["Fold", "Limp", "Raise"], horizontal=True, key=f"preflop_action_{pos_actual}")

            if accion == "Raise":
                size = st.number_input(f"Tamaño Raise {pos_actual} (en bb)", min_value=1.0, step=0.5, format="%.1f", key=f"preflop_size_{pos_actual}")
            else:
                size = None

            if st.button("Confirmar acción Preflop"):
                st.session_state.acciones[pos_actual] = {'accion': accion, 'size': size}
                st.session_state.action_index += 1
    else:
        st.session_state.step = 6


# === Paso 6: Recomendación IA REAL ===
elif st.session_state.step == 6:
    st.title("♠️ Tu turno - Recomendación IA Inteligente")

    nivel_mesa = st.session_state.mesa
    posicion_usuario = st.session_state.posicion
    carta1 = st.session_state.carta1
    carta2 = st.session_state.carta2
    acciones_previas = []
    
    posiciones = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
    for pos in posiciones:
        if pos == posicion_usuario:
            break
        acciones_previas.append(st.session_state.acciones[pos])

    stack_propio = st.session_state.stacks[posicion_usuario]

    # Llamar a la función de recomendación
    resultado = recomendar_accion(carta1, carta2, acciones_previas, nivel_mesa, stack_propio)

    # Mostrar recomendación
    if resultado['accion'] == "Raise":
        st.success(f"👉 Acción: Raise")
        st.info(f"👉 Tamaño: {resultado['tamaño_bb']}bb")
        st.info(f"👉 Monto: ${resultado['monto']:.2f}")
    elif resultado['accion'] == "Call":
        st.success(f"👉 Acción: Call")
        st.info(f"👉 Monto: ${resultado['monto']:.2f}")
    else:
        st.error(f"👉 Acción: Fold")

# === Paso 7: Ingresar Flop ===
elif st.session_state.step == 7:
    st.title("🃏 Paso 7: Flop")

    col1, col2, col3 = st.columns(3)
    with col1:
        carta_flop1 = st.selectbox("Carta 1 del Flop", ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"], key="flop1")
        palo_flop1 = st.selectbox("Palo 1", ["♠", "♥", "♦", "♣"], key="palo_flop1")
    with col2:
        carta_flop2 = st.selectbox("Carta 2 del Flop", ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"], key="flop2")
        palo_flop2 = st.selectbox("Palo 2", ["♠", "♥", "♦", "♣"], key="palo_flop2")
    with col3:
        carta_flop3 = st.selectbox("Carta 3 del Flop", ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"], key="flop3")
        palo_flop3 = st.selectbox("Palo 3", ["♠", "♥", "♦", "♣"], key="palo_flop3")

    if st.button("Confirmar Flop ➝"):
        st.session_state.flop = [
            carta_flop1 + palo_flop1,
            carta_flop2 + palo_flop2,
            carta_flop3 + palo_flop3
        ]
        st.session_state.step = 8  # Avanza a acciones en Flop

# === Paso 8: Acciones en el Flop (corregido para parar en tu turno) ===
elif st.session_state.step == 8:
    st.title("🃏 Paso 8: Acciones de rivales en el Flop")

    if 'flop_action_index' not in st.session_state:
        st.session_state.flop_action_index = 0
        st.session_state.flop_acciones = {}

        # Determinar quienes siguen activos preflop
        st.session_state.activos_flop = []
        posiciones = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
        for pos in posiciones:
            if pos in st.session_state.acciones:
                if st.session_state.acciones[pos]['accion'] != "Fold":
                    st.session_state.activos_flop.append(pos)

    posiciones_flop = st.session_state.activos_flop
    if st.session_state.flop_action_index < len(posiciones_flop):
        pos_actual = posiciones_flop[st.session_state.flop_action_index]

        # Aquí la corrección:
        if pos_actual == st.session_state.posicion:
            st.session_state.step = 9  # Es tu turno, saltamos a la recomendación IA
        else:
            st.subheader(f"Acción de {pos_actual} en el Flop")
            accion = st.radio(f"¿Qué hizo {pos_actual}?", ["Check", "Bet pequeño", "Bet medio", "Bet pot", "All-in"], horizontal=True, key=f"flop_action_{pos_actual}")

            if st.button("Confirmar acción Flop"):
                st.session_state.flop_acciones[pos_actual] = accion
                st.session_state.flop_action_index += 1
    else:
        st.session_state.step = 9

# === Paso 9: Tu turno en el Flop - Ahora usando ia_motor.py ===
elif st.session_state.step == 9:
    st.title("♠️ Tu Turno en el Flop - Recomendación IA Mejorada")

    nivel_mesa = st.session_state.mesa
    carta1 = st.session_state.carta1
    carta2 = st.session_state.carta2
    flop = st.session_state.flop
    acciones_flop = st.session_state.flop_acciones
    stack_propio = st.session_state.stacks[st.session_state.posicion]

    # Llamamos a la función nueva
    resultado_flop = recomendar_accion_flop(carta1, carta2, flop, acciones_flop, nivel_mesa, stack_propio)

    st.write(f"Flop: {flop[0]}, {flop[1]}, {flop[2]}")
    st.write(f"Bote estimado: ${resultado_flop['bote_estimado']:.2f}")

    if resultado_flop['accion'].startswith(\"Bet\"):
        st.success(f\"👉 Acción: {resultado_flop['accion']}\")
        st.info(f\"👉 Apostar: ${resultado_flop['monto']:.2f}\")
    else:
        st.error(f\"👉 Acción: {resultado_flop['accion']}\")

# === Paso 10: Ingresar carta del Turn ===
elif st.session_state.step == 10:
    st.title("🃏 Paso 10: Turn")

    col1 = st.columns(1)
    with col1[0]:
        carta_turn = st.selectbox("Carta del Turn", ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"], key="turn_carta")
        palo_turn = st.selectbox("Palo del Turn", ["♠", "♥", "♦", "♣"], key="turn_palo")

    if st.button("Confirmar Turn ➝"):
        st.session_state.turn = carta_turn + palo_turn
        st.session_state.step = 11  # Luego pasamos a acciones en el Turn

# === Paso 11: Acciones en el Turn ===
elif st.session_state.step == 11:
    st.title("🃏 Paso 11: Acciones de rivales en el Turn")

    if 'turn_action_index' not in st.session_state:
        st.session_state.turn_action_index = 0
        st.session_state.turn_acciones = {}

        # Determinar quienes siguen activos desde el Flop
        st.session_state.activos_turn = []
        for pos in st.session_state.activos_flop:
            if pos not in st.session_state.flop_acciones or st.session_state.flop_acciones[pos] != "Fold":
                st.session_state.activos_turn.append(pos)

    posiciones_turn = st.session_state.activos_turn
    if st.session_state.turn_action_index < len(posiciones_turn):
        pos_actual = posiciones_turn[st.session_state.turn_action_index]

        # Corrección igual que en Flop:
        if pos_actual == st.session_state.posicion:
            st.session_state.step = 12  # Es tu turno en Turn
        else:
            st.subheader(f"Acción de {pos_actual} en el Turn")
            accion = st.radio(f"¿Qué hizo {pos_actual}?", ["Check", "Bet pequeño", "Bet medio", "Bet pot", "All-in"], horizontal=True, key=f"turn_action_{pos_actual}")

            if st.button("Confirmar acción Turn"):
                st.session_state.turn_acciones[pos_actual] = accion
                st.session_state.turn_action_index += 1
    else:
        st.session_state.step = 12  # Pasamos a tu turno

# === Paso 12: Tu turno en el Turn - Ahora usando ia_motor.py ===
elif st.session_state.step == 12:
    st.title("♠️ Tu Turno en el Turn - Recomendación IA Inteligente")

    nivel_mesa = st.session_state.mesa
    carta1 = st.session_state.carta1
    carta2 = st.session_state.carta2
    flop = st.session_state.flop
    turn = st.session_state.turn
    acciones_flop = st.session_state.flop_acciones
    acciones_turn = st.session_state.turn_acciones
    stack_propio = st.session_state.stacks[st.session_state.posicion]

    # Llamar a la función nueva del motor
    resultado_turn = recomendar_accion_turn(carta1, carta2, flop, turn, acciones_flop, acciones_turn, nivel_mesa, stack_propio)

    st.write(f"Flop: {flop[0]}, {flop[1]}, {flop[2]}")
    st.write(f"Turn: {turn}")
    st.write(f"Bote actual estimado: ${resultado_turn['bote_estimado']:.2f}")

    if resultado_turn['accion'].startswith(\"Bet\"):
        st.success(f\"👉 Acción: {resultado_turn['accion']}\")
        st.info(f\"👉 Apostar: ${resultado_turn['monto']:.2f}\")
    else:
        st.error(f\"👉 Acción: {resultado_turn['accion']}\")

# === Paso 13: Ingresar carta del River ===
elif st.session_state.step == 13:
    st.title("🃏 Paso 13: River")

    col1 = st.columns(1)
    with col1[0]:
        carta_river = st.selectbox("Carta del River", ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"], key="river_carta")
        palo_river = st.selectbox("Palo del River", ["♠", "♥", "♦", "♣"], key="river_palo")

    if st.button("Confirmar River ➝"):
        st.session_state.river = carta_river + palo_river
        st.session_state.step = 14  # Luego pasamos a acciones en el River

# === Paso 14: Acciones en el River ===
elif st.session_state.step == 14:
    st.title("🃏 Paso 14: Acciones de rivales en el River")

    if 'river_action_index' not in st.session_state:
        st.session_state.river_action_index = 0
        st.session_state.river_acciones = {}

        # Determinar quienes siguen activos desde el Turn
        st.session_state.activos_river = []
        for pos in st.session_state.activos_turn:
            if pos not in st.session_state.turn_acciones or st.session_state.turn_acciones[pos] != "Fold":
                st.session_state.activos_river.append(pos)

    posiciones_river = st.session_state.activos_river
    if st.session_state.river_action_index < len(posiciones_river):
        pos_actual = posiciones_river[st.session_state.river_action_index]

        # Corrección igual que en Flop y Turn:
        if pos_actual == st.session_state.posicion:
            st.session_state.step = 15  # Es tu turno en River
        else:
            st.subheader(f"Acción de {pos_actual} en el River")
            accion = st.radio(f"¿Qué hizo {pos_actual}?", ["Check", "Bet pequeño", "Bet medio", "Bet pot", "All-in"], horizontal=True, key=f"river_action_{pos_actual}")

            if st.button("Confirmar acción River"):
                st.session_state.river_acciones[pos_actual] = accion
                st.session_state.river_action_index += 1
    else:
        st.session_state.step = 15


# === Paso 15: Tu turno en el River - Recomendación IA ===
elif st.session_state.step == 15:
    st.title("♠️ Tu Turno en el River - Recomendación IA Inteligente")

    nivel_mesa = st.session_state.mesa
    carta1 = st.session_state.carta1
    carta2 = st.session_state.carta2
    flop = st.session_state.flop
    turn = st.session_state.turn
    river = st.session_state.river
    acciones_flop = st.session_state.flop_acciones
    acciones_turn = st.session_state.turn_acciones
    acciones_river = st.session_state.river_acciones
    stack_propio = st.session_state.stacks[st.session_state.posicion]

    # Llamar a la función del motor IA
    resultado_river = recomendar_accion_river(carta1, carta2, flop, turn, river, acciones_flop, acciones_turn, acciones_river, nivel_mesa, stack_propio)

    st.write(f"Flop: {flop[0]}, {flop[1]}, {flop[2]}")
    st.write(f"Turn: {turn}")
    st.write(f"River: {river}")
    st.write(f"Bote actual estimado: ${resultado_river['bote_estimado']:.2f}")

    if resultado_river['accion'].startswith(\"Bet\"):
        st.success(f\"👉 Acción: {resultado_river['accion']}\")
        st.info(f\"👉 Apostar: ${resultado_river['monto']:.2f}\")
    else:
        st.error(f\"👉 Acción: {resultado_river['accion']}\")

