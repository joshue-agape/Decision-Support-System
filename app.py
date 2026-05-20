import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Decision Support System", layout="wide", initial_sidebar_state="expanded")

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
        color: #0F172A !important;
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

st.title("Outil de simulation pour la notation des projets")
st.markdown("Outil décisionnel mêlant la méthode géométrique TOPSIS et la méthode prudente Min-Max.")
st.markdown("---")

# ============================
# PANNEAU LATÉRAL
# ============================
st.sidebar.markdown("### Ajustement des Dimensions")
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

# ============================
# ZONE CENTRALE
# ============================
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

# ============================
# FORMULAIRE
# ============================
st.markdown("### Support de collecte des données")
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
        nom_alt = st.text_input(f"Variante de projet {j+1}", value=f"Projet A{j+1}", key=f"alt_name_{j}")
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

# ==========================================
# TRAITEMENT ALGORITHMIQUE
# ==========================================
if st.button("Évaluer le score de performance", type="primary"):
    X = df_brut.to_numpy(dtype=float)
    
    norm_denominator = np.sqrt((X**2).sum(axis=0))
    norm_denominator[norm_denominator == 0] = 1e-9 
    X_norm = X / norm_denominator
    
    # CALCULS ANALYTIQUES MÉTHODE MIN-MAX
    X_minmax_prep = np.zeros_like(X_norm)
    for col in range(int(nb_criteres)):
        if objectifs_criteres[col]:
            X_minmax_prep[:, col] = X_norm[:, col]
        else:
            X_minmax_prep[:, col] = 1.0 - X_norm[:, col]
            
    # Identifier la pire performance (le minimum) pour chaque alternative
    pires_scores_alternatives = np.min(X_minmax_prep, axis=1)
    
    df_minmax = pd.DataFrame({
        "Alternative": noms_alternatives,
        "Score Sécurité (Min-Max)": pires_scores_alternatives
    }).sort_values(by="Score Sécurité (Min-Max)", ascending=True)
    
    meilleur_projet_mm = df_minmax.iloc[-1]['Alternative']
    meilleur_score_mm = df_minmax.iloc[-1]["Score Sécurité (Min-Max)"]

    # ================================================
    # CALCULS ANALYTIQUES MÉTHODE TOPSIS
    # ================================================
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
    
    df_topsis = pd.DataFrame({
        "Alternative": noms_alternatives,
        "Score TOPSIS": scores_topsis
    }).sort_values(by="Score TOPSIS", ascending=True)
    
    meilleur_projet_top = df_topsis.iloc[-1]['Alternative']
    meilleur_score_top = df_topsis.iloc[-1]["Score TOPSIS"]

    # ========================================================
    # RESTITUTION DES RÉSULTATS : MODULE MIN-MAX
    # ========================================================
    st.markdown("## 1. Résultats obtenus par la méthode prudente Min-Max")
    st.markdown(f"""
        <div class="recommendation-box" style="border-left-color: #10B981;">
            <div class="recommendation-title" style="color: #34D399 !important;">Recommandation Min-Max (Profil prudent)</div>
            <div class="recommendation-text">
                En renforçant au maximum les points faibles, l’alternative la plus adaptée est <strong>{meilleur_projet_mm}</strong> avec un score de sécurité minimal de <strong>{meilleur_score_mm:.3f}</strong>.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_table_mm, col_chart_mm = st.columns([2, 3])
    with col_table_mm:
        st.markdown("##### Classement Min-Max")
        df_aff_mm = df_minmax.iloc[::-1].copy().reset_index(drop=True)
        df_aff_mm.index += 1
        df_aff_mm.index.name = "Rang"
        st.dataframe(df_aff_mm, width='stretch')
        
    with col_chart_mm:
        couleurs_mm = {alt: '#A7F3D0' if alt != meilleur_projet_mm else '#34D399' for alt in df_minmax['Alternative']}
        fig_bar_mm = px.bar(df_minmax, x="Score Sécurité (Min-Max)", y="Alternative", orientation='h', text_auto='.3f', color="Alternative", color_discrete_map=couleurs_mm)
        fig_bar_mm.update_layout(showlegend=False, xaxis_title="Indice de Sécurité Minimal", yaxis_title=None, height=240, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig_bar_mm.update_traces(textposition='outside', cliponaxis=False)
        st.plotly_chart(fig_bar_mm, width='stretch', config={'displayModeBar': False})

    st.markdown("---")

    # ========================================================
    # RESTITUTION DES RÉSULTATS : MODULE TOPSIS
    # ========================================================
    st.markdown("## 2. Résultats obtenus par la méthode de compromis TOPSIS")
    st.markdown(f"""
        <div class="recommendation-box">
            <div class="recommendation-title">Recommandation TOPSIS (Profil Équilibré)</div>
            <div class="recommendation-text">
                En mesurant le compromis global idéal, l'alternative optimale est <strong>{meilleur_projet_top}</strong> avec un score d'adéquation de <strong>{meilleur_score_top:.3f}</strong>.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_table_top, col_chart_top = st.columns([2, 3])
    with col_table_top:
        st.markdown("##### Classement TOPSIS")
        df_aff_top = df_topsis.iloc[::-1].copy().reset_index(drop=True)
        df_aff_top.index += 1
        df_aff_top.index.name = "Rang"
        st.dataframe(df_aff_top, width='stretch')
        
    with col_chart_top:
        couleurs_top = {alt: '#4ADE80' if alt != meilleur_projet_top else '#93C5FD' for alt in df_topsis['Alternative']}
        fig_bar_top = px.bar(df_topsis, x="Score TOPSIS", y="Alternative", orientation='h', text_auto='.3f', color="Alternative", color_discrete_map=couleurs_top)
        fig_bar_top.update_layout(showlegend=False, xaxis_title="Score de Proximité Idéale", yaxis_title=None, height=240, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig_bar_top.update_traces(textposition='outside', cliponaxis=False)
        st.plotly_chart(fig_bar_top, width='stretch', config={'displayModeBar': False})

    # ==========================================
    # ANALYSES FINALES ET AVANCÉES
    # ==========================================
    st.markdown("---")
    st.markdown("### Analyse approfondie de décision basée sur des données brutes normalisées")
    
    col_radar, col_stack = st.columns(2)
    
    with col_radar:
        st.markdown("#### Représentation comparative des alternatives en radar")
        fig_radar = go.Figure()
        for idx, name in enumerate(noms_alternatives):
            fig_radar.add_trace(go.Scatterpolar(
                r=X_norm[idx].tolist() + [X_norm[idx][0]],
                theta=noms_criteres + [noms_criteres[0]],
                fill='toself',
                name=name,
                line=dict(width=2 if name != meilleur_projet_top else 3)
            ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True, height=350, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_radar, width='stretch')

    with col_stack:
        st.markdown("#### Apport de chaque critère dans le profil pondéré")
        df_stack = pd.DataFrame(X_pond, columns=noms_criteres, index=noms_alternatives).reset_index().rename(columns={'index': 'Alternative'})
        fig_stack = px.bar(df_stack, x="Alternative", y=noms_criteres, barmode="stack", color_discrete_sequence=px.colors.qualitative.Safe)
        fig_stack.update_layout(xaxis_title=None, yaxis_title="Valeur Pondérée Cumulée", height=350, margin=dict(t=20, b=20, l=20, r=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_stack, width='stretch')