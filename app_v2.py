import streamlit as st
from ia_motor import clasificar_mano, recomendar_accion, recomendar_accion_flop, recomendar_accion_turn, recomendar_accion_river

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

if 'step' not in st.session_state:
    st.session_state.step = 1

# === Paso 1: Tipo de mesa ===
if st.session_state.step == 1:
    st.title("♠️ Paso 1: Tipo de mesa")
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

# === Paso 4: Stacks ===
elif st.session_state.step == 4:
    if 'stack_index' not in st.session_state:
        st.session_state.stack_index = 0
        st.session_state.stacks = {}

    posiciones = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
    st.title(f"Paso 4: Stack de {posiciones[st.session_state.stack_index]}")
    stack = st.number_input(f"Stack de {posiciones[st.session_state.stack_index]} ($)", min_value=0.01, step=0.01, format="%.2f")
    if st.button("Confirmar stack"):
        st.session_state.stacks[posiciones[st.session_state.stack_index]] = stack
        st.session_state.stack_index += 1
        if st.session_state.stack_index >= len(posiciones):
            st.session_state.step = 5

# === Paso 5: Acciones Preflop ===
elif st.session_state.step == 5:
    if 'action_index' not in st.session_state:
        st.session_state.action_index = 0
        st.session_state.acciones = {}

    posiciones = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
    st.title("♠️ Paso 5: Acciones Preflop")

    if st.session_state.action_index < len(posiciones):
        pos_actual = posiciones[st.session_state.action_index]

        if pos_actual == st.session_state.posicion:
            st.session_state.step = 6
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

# === Paso 6: Recomendación IA Preflop ===
elif st.session_state.step == 6:
    st.title("♠️ Tu Turno Preflop - Recomendación IA")
    resultado = recomendar_accion(st.session_state.carta1, st.session_state.carta2, list(st.session_state.acciones.values()), st.session_state.mesa, st.session_state.stacks[st.session_state.posicion])
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
        st.session_state.step = 8

# === Paso 8: Acciones en el Flop ===
elif st.session_state.step == 8:
    st.title("🃏 Paso 8: Acciones de rivales en el Flop")

    if 'flop_action_index' not in st.session_state:
        st.session_state.flop_action_index = 0
        st.session_state.flop_acciones = {}
        st.session_state.activos_flop = []
        posiciones = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
        for pos in posiciones:
            if pos in st.session_state.acciones:
                if st.session_state.acciones[pos]['accion'] != "Fold":
                    st.session_state.activos_flop.append(pos)

    posiciones_flop = st.session_state.activos_flop
    if st.session_state.flop_action_index < len(posiciones_flop):
        pos_actual = posiciones_flop[st.session_state.flop_action_index]

        if pos_actual == st.session_state.posicion:
            st.session_state.step = 9
        else:
            st.subheader(f"Acción de {pos_actual} en el Flop")
            accion = st.radio(f"¿Qué hizo {pos_actual}?", ["Check", "Bet pequeño", "Bet medio", "Bet pot", "All-in"], horizontal=True, key=f"flop_action_{pos_actual}")

            if st.button("Confirmar acción Flop"):
                st.session_state.flop_acciones[pos_actual] = accion
                st.session_state.flop_action_index += 1
    else:
        st.session_state.step = 9

# === Paso 9: Tu turno en el Flop - Recomendación IA ===
elif st.session_state.step == 9:
    st.title("♠️ Tu Turno en el Flop - Recomendación IA")

    resultado_flop = recomendar_accion_flop(
        st.session_state.carta1,
        st.session_state.carta2,
        st.session_state.flop,
        st.session_state.flop_acciones,
        st.session_state.mesa,
        st.session_state.stacks[st.session_state.posicion]
    )

    st.write(f"Flop: {st.session_state.flop[0]}, {st.session_state.flop[1]}, {st.session_state.flop[2]}")
    st.write(f"Bote estimado: ${resultado_flop['bote_estimado']:.2f}")

    if resultado_flop['accion'].startswith("Bet"):
        st.success(f"👉 Acción: {resultado_flop['accion']}")
        st.info(f"👉 Apostar: ${resultado_flop['monto']:.2f}")
    else:
        st.error(f"👉 Acción: {resultado_flop['accion']}")

# === Paso 10: Ingresar carta del Turn ===
elif st.session_state.step == 10:
    st.title("🃏 Paso 10: Turn")

    carta_turn = st.selectbox("Carta del Turn", ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"], key="turn_carta")
    palo_turn = st.selectbox("Palo del Turn", ["♠", "♥", "♦", "♣"], key="turn_palo")
    
    if st.button("Confirmar Turn ➝"):
        st.session_state.turn = carta_turn + palo_turn
        st.session_state.step = 11

# === Paso 11: Acciones en el Turn ===
elif st.session_state.step == 11:
    st.title("🃏 Paso 11: Acciones de rivales en el Turn")

    if 'turn_action_index' not in st.session_state:
        st.session_state.turn_action_index = 0
        st.session_state.turn_acciones = {}
        st.session_state.activos_turn = []
        for pos in st.session_state.activos_flop:
            if pos not in st.session_state.flop_acciones or st.session_state.flop_acciones[pos] != "Fold":
                st.session_state.activos_turn.append(pos)

    posiciones_turn = st.session_state.activos_turn
    if st.session_state.turn_action_index < len(posiciones_turn):
        pos_actual = posiciones_turn[st.session_state.turn_action_index]

        if pos_actual == st.session_state.posicion:
            st.session_state.step = 12
        else:
            st.subheader(f"Acción de {pos_actual} en el Turn")
            accion = st.radio(f"¿Qué hizo {pos_actual}?", ["Check", "Bet pequeño", "Bet medio", "Bet pot", "All-in"], horizontal=True, key=f"turn_action_{pos_actual}")

            if st.button("Confirmar acción Turn"):
                st.session_state.turn_acciones[pos_actual] = accion
                st.session_state.turn_action_index += 1
    else:
        st.session_state.step = 12

# === Paso 12: Tu turno en el Turn - Recomendación IA ===
elif st.session_state.step == 12:
    st.title("♠️ Tu Turno en el Turn - Recomendación IA")

    resultado_turn = recomendar_accion_turn(
        st.session_state.carta1,
        st.session_state.carta2,
        st.session_state.flop,
        st.session_state.turn,
        st.session_state.flop_acciones,
        st.session_state.turn_acciones,
        st.session_state.mesa,
        st.session_state.stacks[st.session_state.posicion]
    )

    st.write(f"Turn: {st.session_state.turn}")
    st.write(f"Bote estimado: ${resultado_turn['bote_estimado']:.2f}")

    if resultado_turn['accion'].startswith("Bet"):
        st.success(f"👉 Acción: {resultado_turn['accion']}")
        st.info(f"👉 Apostar: ${resultado_turn['monto']:.2f}")
    else:
        st.error(f"👉 Acción: {resultado_turn['accion']}")

# === Paso 13: Ingresar carta del River ===
elif st.session_state.step == 13:
    st.title("🃏 Paso 13: River")

    carta_river = st.selectbox("Carta del River", ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"], key="river_carta")
    palo_river = st.selectbox("Palo del River", ["♠", "♥", "♦", "♣"], key="river_palo")
    
    if st.button("Confirmar River ➝"):
        st.session_state.river = carta_river + palo_river
        st.session_state.step = 14

# === Paso 14: Acciones en el River ===
elif st.session_state.step == 14:
    st.title("🃏 Paso 14: Acciones de rivales en el River")

    if 'river_action_index' not in st.session_state:
        st.session_state.river_action_index = 0
        st.session_state.river_acciones = {}
        st.session_state.activos_river = []
        for pos in st.session_state.activos_turn:
            if pos not in st.session_state.turn_acciones or st.session_state.turn_acciones[pos] != "Fold":
                st.session_state.activos_river.append(pos)

    posiciones_river = st.session_state.activos_river
    if st.session_state.river_action_index < len(posiciones_river):
        pos_actual = posiciones_river[st.session_state.river_action_index]

        if pos_actual == st.session_state.posicion:
            st.session_state.step = 15
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
    st.title("♠️ Tu Turno en el River - Recomendación IA")

    resultado_river = recomendar_accion_river(
        st.session_state.carta1,
        st.session_state.carta2,
        st.session_state.flop,
        st.session_state.turn,
        st.session_state.river,
        st.session_state.flop_acciones,
        st.session_state.turn_acciones,
        st.session_state.river_acciones,
        st.session_state.mesa,
        st.session_state.stacks[st.session_state.posicion]
    )

    st.write(f"River: {st.session_state.river}")
    st.write(f"Bote estimado: ${resultado_river['bote_estimado']:.2f}")

    if resultado_river['accion'].startswith("Bet"):
        st.success(f"👉 Acción: {resultado_river['accion']}")
        st.info(f"👉 Apostar: ${resultado_river['monto']:.2f}")
    else:
        st.error(f"👉 Acción: {resultado_river['accion']}")