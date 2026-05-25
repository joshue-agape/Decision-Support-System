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
        border-left: 4px solid #10B981;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1.2rem;
        border-radius: 0px 8px 8px 0px;
        margin-top: 1.2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.3);
        color: #FFFFFF !important;
    }
    .recommendation-title {
        color: #34D399 !important;
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
st.markdown("Outil décisionnel basé exclusivement sur la méthode prudente Min-Max (Analyse du Regret).")
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
noms_defaut = ["Rentabilité", "Coût", "Risque", "Responsabilité Sociale", "Délai"]

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
st.markdown("### Configuration de l'importance relative des critères")
poids_criteres = []
cols_sliders = st.columns(2)
poids_initiaux = [0.30, 0.25, 0.20, 0.15, 0.10]

for i, nom_crit in enumerate(noms_criteres):
    col_cible = cols_sliders[0] if i % 2 == 0 else cols_sliders[1]
    with col_cible:
        val_init = poids_initiaux[i] if i < len(poids_initiaux) else 0.10
        val_poids = col_cible.slider(
            f"Poids {nom_crit}", 
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
    st.markdown("**Variantes**")
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
# TRAITEMENT ALGORITHMIQUE PAR ÉTAPE
# ==========================================
if st.button("Évaluer le score de performance", type="primary"):
    X = df_brut.to_numpy(dtype=float)
    
    min_globaux = X.min(axis=0)
    max_globaux = X.max(axis=0)
    diffs = max_globaux - min_globaux
    diffs[diffs == 0] = 1e-9 
    
    # --------------------------------------------------------
    # NORMALISATION (0 À 1)
    # --------------------------------------------------------
    st.markdown("### Normalsation des données (Échelle 0 à 1)")
    
    X_norm = np.zeros_like(X)
    for col in range(int(nb_criteres)):
        if objectifs_criteres[col]:
            X_norm[:, col] = (X[:, col] - min_globaux[col]) / diffs[col]
        else:
            X_norm[:, col] = (max_globaux[col] - X[:, col]) / diffs[col]
            
    df_norm = pd.DataFrame(X_norm, columns=[f"{c} (norm)" for c in noms_criteres], index=noms_alternatives)
    st.dataframe(df_norm.round(3), width='stretch')
    st.markdown("---")
    
    # --------------------------------------------------------
    # CALCUL DES REGRETS
    # --------------------------------------------------------
    st.markdown("### Calcul des Regrets Pondérés")
    
    X_regrets = np.zeros_like(X_norm)
    criteres_bloquants = []
    
    for row in range(len(noms_alternatives)):
        regrets_ligne = []
        for col in range(int(nb_criteres)):
            regret_val = poids_normalises[col] * (1.0 - X_norm[row, col])
            X_regrets[row, col] = regret_val
            regrets_ligne.append(regret_val)
            
        idx_pire = np.argmax(regrets_ligne)
        criteres_bloquants.append(noms_criteres[idx_pire])
        
    scores_minmax = np.max(X_regrets, axis=1)
    
    df_regrets = pd.DataFrame(X_regrets, columns=[f"Regret {c}" for c in noms_criteres], index=noms_alternatives)
    df_regrets["Score Min-Max (Pire Regret)"] = scores_minmax
    df_regrets["Critère Bloquant"] = criteres_bloquants
    
    st.dataframe(df_regrets.round(3), width='stretch')
    st.markdown("---")
    
    # --------------------------------------------------------
    # CONCLUSION ET CLASSEMENT
    # --------------------------------------------------------
    st.markdown("### Conclusion et Classement Final")
    
    df_minmax = pd.DataFrame({
        "Alternative": noms_alternatives,
        "Score Min-Max": scores_minmax,
        "Critère bloquant": criteres_bloquants
    }).sort_values(by="Score Min-Max", ascending=True)
    
    meilleur_projet_mm = df_minmax.iloc[0]['Alternative']
    meilleur_score_mm = df_minmax.iloc[0]["Score Min-Max"]
    raison_bloquante = df_minmax.iloc[0]["Critère bloquant"]
    
    st.markdown(f"""
        <div class="recommendation-box">
            <div class="recommendation-title">Recommandation Min-Max (Profil prudent)</div>
            <div class="recommendation-text">
                En minimisant le regret maximal vis-à-vis du scénario idéal, l’alternative optimale est <strong>{meilleur_projet_mm}</strong> avec un score de regret minimal de <strong>{meilleur_score_mm:.3f}</strong> (généré par le critère : <em>{raison_bloquante}</em>).
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_table_mm, col_chart_mm = st.columns([2, 3])
    with col_table_mm:
        st.markdown("##### Classement de Robustesse")
        df_aff_mm = df_minmax.copy().reset_index(drop=True)
        df_aff_mm.index += 1
        df_aff_mm.index.name = "Rang"
        st.dataframe(df_aff_mm, width='stretch')
        
    with col_chart_mm:
        st.markdown("##### Score de risque du projet (Plus bas = Plus sûr)")
        df_graph = df_minmax.iloc[::-1].copy()
        couleurs_mm = {alt: '#94A3B8' if alt != meilleur_projet_mm else '#34D399' for alt in df_graph['Alternative']}
        
        fig_bar_mm = px.bar(df_graph, x="Score Min-Max", y="Alternative", orientation='h', text_auto='.3f', color="Alternative", color_discrete_map=couleurs_mm)
        fig_bar_mm.update_layout(showlegend=False, xaxis_title="Regret Maximal Éprouvé", yaxis_title=None, height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig_bar_mm.update_traces(textposition='outside', cliponaxis=False)
        st.plotly_chart(fig_bar_mm, width='stretch', config={'displayModeBar': False})

    # ==========================================
    # GRAPHES ET ANALYSES AVANCÉES
    # ==========================================
    st.markdown("---")
    st.markdown("### Évaluation de la robustesse des projets face au pire scénario")
    
    col_radar, col_stack = st.columns(2)
    
    with col_radar:
        st.markdown("#### Visualisation radar des forces et faiblesses des alternatives")
        fig_radar = go.Figure()
        for idx, name in enumerate(noms_alternatives):
            epaisseur = 3.5 if name == meilleur_projet_mm else 1.5
            fig_radar.add_trace(go.Scatterpolar(
                r=X_norm[idx].tolist() + [X_norm[idx][0]],
                theta=noms_criteres + [noms_criteres[0]],
                fill='toself' if name == meilleur_projet_mm else None,
                name=name,
                line=dict(width=epaisseur)
            ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True, height=350, margin=dict(t=20, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_radar, width='stretch')

    with col_stack:
        st.markdown("#### Détail des facteurs de risque de déception")
        df_stack = pd.DataFrame(X_regrets, columns=noms_criteres, index=noms_alternatives).reset_index().rename(columns={'index': 'Alternative'})
        fig_stack = px.bar(df_stack, x="Alternative", y=noms_criteres, barmode="stack", color_discrete_sequence=px.colors.qualitative.Safe)
        fig_stack.update_layout(xaxis_title=None, yaxis_title="Regret cumulé des dimensions", height=350, margin=dict(t=20, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_stack, width='stretch')