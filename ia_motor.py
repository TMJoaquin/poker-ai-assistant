import streamlit as st

# Configuración visual
st.set_page_config(page_title="Poker AI Assistant", layout="centered")
st.markdown(
    """
    <style>
        .stApp { background-color: #0e1117; color: white; }
        .css-18e3th9 { background-color: #0e1117; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("♠️ Poker AI Assistant - Cash Game 6-Max ♠️")
st.markdown("Este asistente te guiará para tomar la mejor decisión en cada calle (Preflop → River) de forma inmediata.")

# Paso 1: Configuración inicial
st.subheader("1. Configura la mano")
mesa = st.selectbox("Tipo de mesa:", ['NL2', 'NL5', 'NL10', 'NL25'])
posiciones = ['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']
stacks = {}
for pos in posiciones:
    stacks[pos] = st.number_input(f"Stack de {pos} ($):", min_value=0.0, max_value=100.0, value=5.0, step=0.01)

mi_pos = st.selectbox("Tu posición:", posiciones)
col1, col2 = st.columns(2)
with col1:
    carta1 = st.selectbox("Carta 1:", ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"])
    palo1 = st.selectbox("Palo 1:", ["♠", "♥", "♦", "♣"])
with col2:
    carta2 = st.selectbox("Carta 2:", ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"])
    palo2 = st.selectbox("Palo 2:", ["♠", "♥", "♦", "♣"])

if st.button("Iniciar mano"):
    st.subheader("🔁 Preflop")
    acciones = {}
    for pos in posiciones:
        if pos == mi_pos:
            break
        acciones[pos] = st.selectbox(f"{pos}:", ["Fold", "Limp", "Raise"], key=f"{pos}_action")
        if acciones[pos] == "Raise":
            acciones[f"{pos}_size"] = st.number_input(f"Tamaño raise de {pos} (bb):", min_value=1.0, max_value=100.0, value=3.0, key=f"{pos}_size_input")
    st.write("→ Tu acción recomendada (preflop): Raise 3x")

    st.subheader("📉 Flop")
    flop_cards = st.text_input("Cartas del flop (ej. Ah Kd Tc):")
    accion_flop = st.selectbox("Acción del rival en flop:", ["Check", "Bet 1/3", "Bet 1/2", "Bet pot"])
    st.write("→ Tu acción recomendada (flop): Call")

    st.subheader("📉 Turn")
    turn_card = st.text_input("Carta del Turn (ej. 7h):")
    accion_turn = st.selectbox("Acción del rival en turn:", ["Check", "Bet 1/2", "All-in"])
    st.write("→ Tu acción recomendada (turn): Fold")

    st.subheader("📉 River")
    river_card = st.text_input("Carta del River (ej. 2c):")
    accion_river = st.selectbox("Acción del rival en river:", ["Check", "Bet pot", "Overbet"])
    st.write("→ Tu acción recomendada (river): Call")

