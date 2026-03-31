import streamlit as st

# Configuration de l'interface
st.set_page_config(page_title="HiLo Predictor Madagascar", page_icon="🃏")

st.title("📊 HiLo Predictor Pro")
st.write("Optimisez vos chances en suivant les cartes restantes dans le jeu.")

# Initialisation du jeu de 52 cartes dans la mémoire de l'application
if 'deck' not in st.session_state:
    # 4 exemplaires de chaque valeur (1 à 13)
    st.session_state.deck = {
        "As": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, 
        "7": 4, "8": 4, "9": 4, "10": 4, "Valet": 4, "Dame": 4, "Roi": 4
    }

# Valeurs numériques pour les calculs
values = {
    "As": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, 
    "7": 7, "8": 8, "9": 9, "10": 10, "Valet": 11, "Dame": 12, "Roi": 13
}

# Barre latérale pour la gestion
with st.sidebar:
    if st.button("🔄 Réinitialiser le jeu (Nouveau sabot)"):
        st.session_state.deck = {k: 4 for k in values.keys()}
        st.success("Le jeu a été mélangé !")
    
    st.write("---")
    st.write("**Cartes restantes :**")
    st.json(st.session_state.deck)

# Sélection de la carte actuelle
current_card = st.selectbox("Quelle carte est affichée à l'écran ?", list(values.keys()))

if st.button("Calculer et Retirer du jeu"):
    val = values[current_card]
    
    # On retire la carte actuelle du comptage
    if st.session_state.deck[current_card] > 0:
        st.session_state.deck[current_card] -= 1
    
    # Calcul des cartes restantes
    total_remaining = sum(st.session_state.deck.values())
    
    if total_remaining > 0:
        low_cards = sum(count for card, count in st.session_state.deck.items() if values[card] < val)
        high_cards = sum(count for card, count in st.session_state.deck.items() if values[card] > val)
        same_cards = st.session_state.deck[current_card]

        # Calcul des pourcentages
        p_low = (low_cards / total_remaining) * 100
        p_high = (high_cards / total_remaining) * 100

        # Affichage des résultats
        st.subheader("Prédictions statistiques :")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("INFÉRIEUR", f"{p_low:.1f}%")
            if p_low > p_high: st.success("Meilleur choix")
            
        with col2:
            st.metric("SUPÉRIEUR", f"{p_high:.1f}%")
            if p_high > p_low: st.success("Meilleur choix")
            
        st.write(f"ℹ️ Il reste **{total_remaining}** cartes dans le paquet.")
    else:
        st.error("Plus de cartes dans le paquet ! Veuillez réinitialiser.")

st.markdown("---")
st.caption("Attention : Le hasard reste imprévisible. Ne misez que ce que vous pouvez perdre.")
