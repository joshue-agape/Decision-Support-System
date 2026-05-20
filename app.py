import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Système d'Aide à la Décision", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    h1 {
        font-weight: 700;
        color: #0F172A;
        font-size: 2.4rem;
        margin-bottom: 0.2rem;
    }
    h2, h3 {
        color: #1E293B;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    .stButton>button {
        background-color: #0284C7;
        color: white;
        border-radius: 6px;
        padding: 0.6rem 2.5rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    .stButton>button:hover {
        background-color: #0369A1;
        color: white;
    }
    .recommendation-box {
        background-color: rgba(30, 41, 59, 0.7);
        border-left: 4px solid #3B82F6;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1.2rem;
        border-radius: 0px 8px 8px 0px;
        margin-top: 1.2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.3);
    }
    .recommendation-title {
        color: #60A5FA !important;
        font-weight: 700;
        font-size: 1.15rem;
        margin-bottom: 0.5rem;
        letter-spacing: 0.02em;
    }
    .recommendation-text {
        color: #E2E8F0 !important;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Project Scoring Simulator")
st.markdown("Système d'aide à la décision basé sur la méthode d'analyse multicritère TOPSIS.")
st.markdown("---")

# PANNEAU LATÉRAL
st.sidebar.markdown("### Configuration des Dimensions")
nb_criteres = st.sidebar.number_input("Nombre de critères", min_value=2, max_value=10, value=5, step=1)
nb_alternatives = st.sidebar.number_input("Nombre d'alternatives", min_value=2, max_value=15, value=4, step=1)

st.sidebar.markdown("---")
st.sidebar.markdown("### Objectifs des Critères")

noms_criteres = []
objectifs_criteres = []
noms_defaut = ["ROI", "Cost", "Risk", "CSR", "Time"]

for i in range(int(nb_criteres)):
    if i > 0:
        st.sidebar.markdown("---")
        
    st.sidebar.markdown(f"**Configuration du Critère {i+1}**")
    
    nom_suggere = noms_defaut[i] if i < len(noms_defaut) else f"C{i+1}"
    nom = st.sidebar.text_input(f"Nom du critère {i+1}", value=nom_suggere, key=f"name_{i}")
    obj = st.sidebar.selectbox(f"Direction pour {nom}", options=["Maximiser", "Minimiser"], key=f"obj_{i}")
    
    noms_criteres.append(nom)
    objectifs_criteres.append(True if obj == "Maximiser" else False)

st.sidebar.markdown("---")


# ZONE CENTRALE
st.markdown("### Project Weight Configuration")
poids_criteres = []
cols_sliders = st.columns(2)
poids_initiaux = [0.30, 0.25, 0.20, 0.15, 0.10]

for i, nom_crit in enumerate(noms_criteres):
    col_cible = cols_sliders[0] if i % 2 == 0 else cols_sliders[1]
    with col_cible:
        val_init = poids_initiaux[i] if i < len(poids_initiaux) else 0.10
        val_poids = col_cible.slider(
            f"Weight {nom_crit}", 
            min_value=0.0, 
            max_value=1.0, 
            value=val_init, 
            step=0.01, 
            key=f"slider_{i}"
        )
        poids_criteres.append(val_poids)

somme_poids = sum(poids_criteres)
poids_normalises = [p / somme_poids for p in poids_criteres] if somme_poids > 0 else [1.0 / nb_criteres] * int(nb_criteres)

st.markdown("---")

# FORMULAIRE
st.markdown("### Matrice de Saisie des Données")
form_data = {}
noms_alternatives = []
col_alt, *cols_crit = st.columns([2] + [1] * int(nb_criteres))

valeurs_defaut = [
    [25.0, 150.0, 40.0, 3.0, 12.0],
    [8.0, 400.0, 10.0, 5.0, 18.0],
    [45.0, 300.0, 65.0, 2.0, 24.0],
    [15.0, 120.0, 15.0, 3.0, 6.0]
]

with col_alt:
    st.markdown("**Alternative**")
    for j in range(int(nb_alternatives)):
        nom_alt = st.text_input(f"Ligne {j+1}", value=f"Projet A{j+1}", key=f"alt_name_{j}")
        noms_alternatives.append(nom_alt)

for c_idx, c_nom in enumerate(noms_criteres):
    with cols_crit[c_idx]:
        st.markdown(f"**{c_nom}**")
        valeurs_critere = []
        for a_idx in range(int(nb_alternatives)):
            val_init = valeurs_defaut[a_idx][c_idx] if (a_idx < len(valeurs_defaut) and c_idx < len(valeurs_defaut[0])) else 10.0
            val = st.number_input(f"Val_{a_idx}_{c_idx}", value=val_init, key=f"cell_{a_idx}_{c_idx}", label_visibility="collapsed")
            valeurs_critere.append(val)
        form_data[c_nom] = valeurs_critere

df_brut = pd.DataFrame(form_data, index=noms_alternatives)
st.dataframe(df_brut, width='stretch')
st.markdown("---")

# CALCULS ET GRAPHIQUES
if st.button("Calculer le score de performance", type="primary"):
    X = df_brut.to_numpy(dtype=float)
    
    # Algorithme TOPSIS
    norm_denominator = np.sqrt((X**2).sum(axis=0))
    norm_denominator[norm_denominator == 0] = 1e-9 
    X_norm = X / norm_denominator
    X_pond = X_norm * np.array(poids_normalises)
    
    v_ideal_positive, v_ideal_negative = [], []
    for col in range(int(nb_criteres)):
        if objectifs_criteres[col]:
            v_ideal_positive.append(np.max(X_pond[:, col]))
            v_ideal_negative.append(np.min(X_pond[:, col]))
        else:
            v_ideal_positive.append(np.min(X_pond[:, col]))
            v_ideal_negative.append(np.max(X_pond[:, col]))
            
    v_ideal_positive, v_ideal_negative = np.array(v_ideal_positive), np.array(v_ideal_negative)
    d_positive = np.sqrt(((X_pond - v_ideal_positive)**2).sum(axis=1))
    d_negative = np.sqrt(((X_pond - v_ideal_negative)**2).sum(axis=1))
    
    scores_denom = d_positive + d_negative
    scores_denom[scores_denom == 0] = 1e-9
    scores_topsis = d_negative / scores_denom
    
    df_final = pd.DataFrame({
        "Alternative": noms_alternatives,
        "Score Pondéré": scores_topsis
    }).sort_values(by="Score Pondéré", ascending=True)
    
    meilleur_projet = df_final.iloc[-1]['Alternative']
    meilleur_score = df_final.iloc[-1]["Score Pondéré"]
    
    st.markdown(f"""
        <div class="recommendation-box">
            <div class="recommendation-title">Solution Recommandée</div>
            <div class="recommendation-text">
                L'alternative optimale identifiée par l'algorithme est <strong>{meilleur_projet}</strong> avec un score d'adéquation de <strong>{meilleur_score:.3f}</strong>.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Disposition des tableaux et graphiques principaux
    col_table, col_chart = st.columns([2, 3])
    with col_table:
        st.markdown("### Tableau de Classement")
        df_affichage = df_final.iloc[::-1].copy().reset_index(drop=True)
        df_affichage.index += 1
        df_affichage.index.name = "Rang"
        st.dataframe(df_affichage, width='stretch')
        
    with col_chart:
        st.markdown("### Classement des Performances Réduites")
        couleurs_map = {alt: '#4ADE80' if alt != meilleur_projet else '#93C5FD' for alt in df_final['Alternative']}
        fig_bar = px.bar(df_final, x="Score Pondéré", y="Alternative", orientation='h', text_auto='.3f', color="Alternative", color_discrete_map=couleurs_map)
        fig_bar.update_layout(showlegend=False, xaxis_title="Score Performance", yaxis_title=None, height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig_bar.update_traces(textposition='outside', cliponaxis=False)
        st.plotly_chart(fig_bar, width='stretch', config={'displayModeBar': False})

    st.markdown("---")
    st.markdown("### Analyses Décisionnelles Approfondies")
    
    col_radar, col_stack = st.columns(2)
    
    # Radar Chart
    with col_radar:
        st.markdown("#### Profil Comparatif des Alternatives (Radar)")
        fig_radar = go.Figure()
        for idx, name in enumerate(noms_alternatives):
            fig_radar.add_trace(go.Scatterpolar(
                r=X_norm[idx].tolist() + [X_norm[idx][0]],
                theta=noms_criteres + [noms_criteres[0]],
                fill='toself',
                name=name,
                line=dict(width=2 if name != meilleur_projet else 3)
            ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True, height=350, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_radar, width='stretch')

    # Barres empilées
    with col_stack:
        st.markdown("#### Contribution de chaque critère au profil")
        df_stack = pd.DataFrame(X_pond, columns=noms_criteres, index=noms_alternatives).reset_index().rename(columns={'index': 'Alternative'})
        fig_stack = px.bar(df_stack, x="Alternative", y=noms_criteres, barmode="stack", color_discrete_sequence=px.colors.qualitative.Safe)
        fig_stack.update_layout(xaxis_title=None, yaxis_title="Valeur Pondérée Cumulée", height=350, margin=dict(t=20, b=20, l=20, r=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_stack, width='stretch')