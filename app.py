import streamlit as st
from datetime import datetime, date
import math

# ==============================================================================
# CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Papstone Clinic",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# MOTEUR DE DONNÉES
# ==============================================================================
TRANSLATION_PSY = {
    "TSD": "Besoin de retour au calme / Saturation mentale",
    "Passage 1-2": "Conflit de dualité / Difficulté à choisir",
    "Blastocyste": "Potentiel latent bloqué / Problème d'incarnation",
    "Placenta": "Dépendance affective / Besoin de sécurité",
    "Féminin Sacré": "Rapport au maternel / Créativité",
    "Péricarde": "Protection émotionnelle excessive / Blindage",
    "Croisement": "Crise de transition / Rupture",
    "Archives": "Mémoires transgénérationnelles / Charge mentale",
    "Cœur": "Régulation émotionnelle / Ouverture aux autres",
    "Singularité": "Centrage / Besoin de solitude",
    "LCR": "Rigidité psychique / Besoin de fluidité",
    "Œil Gauche": "Introspection / Mélancolie",
    "Rate": "Angoisse profonde / Rumination",
    "Œil Droit": "Projection vers l'action / Stress d'anticipation",
    "NSC (Horloge)": "Troubles des rythmes (Sommeil/Veille)",
    "Épiphyse": "Manque de clarté / Confusion mentale",
    "Cerveau": "Surchauffe cognitive / Besoin de sens",
    "Saut Quantique": "Urgence de changement radical",
    "Microtubules": "Hypersensibilité sensorielle",
    "Qi": "Épuisement vital / Fatigue chronique",
    "Fascias": "Douleurs psychosomatiques diffuses",
    "Visage": "Problème d'image de soi / Masque social",
    "Dissolution": "Perte de repères / Deuil symbolique"
}

ZONES_SOMATIQUES = {
    1: "Zone Lombaire / Reins", 2: "Thorax / Cœur", 3: "Hépatobiliaire",
    4: "Respiratoire / Épaules", 5: "Surrénales / Jambes", 6: "Sternum / Thymus",
    7: "Base du Crâne / Hypophyse", 8: "Sommet du Crâne / Épiphyse", 9: "Bassin / Périnée"
}

ANCHOR_AN_1 = datetime(1, 1, 1, 0, 0)
ANCHOR_2012 = datetime(2012, 12, 21, 0, 0)

def get_raw_signature(dt):
    start_year = dt.year if (dt.month == 12 and dt.day >= 21) else dt.year - 1
    start_date = datetime(start_year, 12, 21)
    offset = -5 if dt >= datetime(dt.year, 7, 19) else 0
    days = max((dt - start_date).days + offset, 0)
    frac = (dt.hour * 3600 + dt.minute * 60) / 86400.0
    val = days + frac
    macro = val % 360.0
    micro_f = ((val % 2.288) / 2.288) * 360.0
    delta_h = (dt - ANCHOR_AN_1).total_seconds() / 86400.0
    micro_h = ((delta_h % 2.288) / 2.288) * 360.0
    delta_c = (dt - ANCHOR_2012).total_seconds() / 86400.0
    micro_c = ((delta_c % 2.288) / 2.288) * 360.0
    if micro_c < 0: micro_c += 360.0
    return macro, micro_f, micro_h, micro_c

def get_closest_portal_key(angle):
    PORTAILS_DEG = {
        0: "TSD", 16: "Blastocyste", 35: "Placenta", 52: "Féminin Sacré", 72: "Péricarde",
        90: "Croisement", 108: "Archives", 137: "Cœur", 144: "Singularité", 153: "LCR",
        166: "Œil Gauche", 180: "Rate", 194: "Œil Droit", 206: "NSC (Horloge)", 216: "Épiphyse",
        222: "Cerveau", 270: "Saut Quantique", 288: "Microtubules", 309: "Qi", 325: "Fascias",
        343: "Visage", 360: "Dissolution"
    }
    closest_deg = min(PORTAILS_DEG.keys(), key=lambda x: abs(x - angle))
    return PORTAILS_DEG[closest_deg]

def analyse_manques(prenom, nom):
    import unicodedata
    full = f"{prenom}{nom}".upper()
    clean = ''.join(c for c in unicodedata.normalize('NFD', full) if c.isalpha())
    grid = {i: 0 for i in range(1, 10)}
    for c in clean: grid[(ord(c)-65)%9 + 1] += 1
    return [k for k, v in grid.items() if v == 0]

# ==============================================================================
# INTERFACE
# ==============================================================================
st.markdown("""
<style>
    .block-container {padding-top: 1rem;}
    h1 {color: #2c3e50;}
    .stMetric {background-color: #f0f2f6; padding: 10px; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚕️ Papstone Clinic")
    st.info("Version Pro B2B")
    
    with st.form("patient_form"):
        prenom = st.text_input("Prénom Patient")
        nom = st.text_input("Nom Patient")
        d_naiss = st.date_input("Date de Naissance", value=date(1980, 1, 1), min_value=date(1900, 1, 1))
        h_naiss = st.time_input("Heure", value=datetime.strptime("12:00", "%H:%M"))
        submit = st.form_submit_button("LANCER LE DIAGNOSTIC", type="primary")

if submit and prenom and nom:
    dt = datetime.combine(d_naiss, h_naiss)
    macro, micro_f, micro_h, micro_c = get_raw_signature(dt)
    manques = analyse_manques(prenom, nom)
    
    p_macro = get_closest_portal_key(macro)
    p_micro_f = get_closest_portal_key(micro_f)
    diag_macro = TRANSLATION_PSY.get(p_macro, "Non défini")
    diag_micro = TRANSLATION_PSY.get(p_micro_f, "Non défini")
    
    secteur = int(micro_f // 40) + 1
    zone = ZONES_SOMATIQUES.get(secteur if secteur <=9 else 9, "Global")

    st.header(f"Dossier : {prenom.upper()} {nom.upper()}")
    st.caption(f"Calculé le {datetime.now().strftime('%d/%m/%Y')}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Structure de Fond")
        st.info(f"**{p_macro}**")
        st.markdown(f"**Piste Psy :** {diag_macro}")
        
    with col2:
        st.subheader("2. Cycle Actuel")
        st.warning(f"**{p_micro_f}**")
        st.markdown(f"**Somatisation :** {diag_micro}")

    st.markdown("---")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Zone Corporelle", zone)
    c2.metric("Marqueur Trauma", f"{micro_h:.1f}°")
    c3.metric("Marqueur Éveil", f"{micro_c:.1f}°")
    
    st.markdown("---")
    if manques:
        st.error(f"⚠️ Failles Identitaires détectées (Manques) : {', '.join(map(str, manques))}")
    else:
        st.success("✅ Aucune faille majeure détectée.")

elif submit:
    st.error("Veuillez remplir le nom et le prénom.")
else:
    st.info("👈 Entrez les données du patient dans le menu de gauche.")
