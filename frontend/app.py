import streamlit as st
import requests

# --------------------------------------------------------------------------- #
# Configuração
# --------------------------------------------------------------------------- #

API_URL = "https://datathon-7mlet-grupo-28-1.onrender.com"

st.set_page_config(
    page_title="Datathon 7-MLET · Grupo 28",
    page_icon="🏦",
    layout="centered",
)

# --------------------------------------------------------------------------- #
# CSS
# --------------------------------------------------------------------------- #

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        color: white;
    }
    .hero h1 { font-size: 1.8rem; font-weight: 700; margin: 0 0 .3rem 0; }
    .hero p  { font-size: .95rem; opacity: .75; margin: 0; }

    .card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
    }
    .card h3 { margin: 0 0 .5rem 0; font-size: 1rem; color: #1e293b; }

    .badge {
        display: inline-block;
        font-size: .7rem;
        font-weight: 600;
        padding: .2rem .55rem;
        border-radius: 999px;
        margin-right: .4rem;
        letter-spacing: .04em;
    }
    .badge-get  { background:#dbeafe; color:#1d4ed8; }
    .badge-post { background:#dcfce7; color:#166534; }

    .result-box {
        background: #0f172a;
        color: #7dd3fc;
        border-radius: 10px;
        padding: 1.1rem 1.4rem;
        font-family: monospace;
        font-size: .82rem;
        white-space: pre-wrap;
        word-break: break-word;
        margin-top: .8rem;
    }

    .offer-card {
        border-left: 4px solid #3b82f6;
        background: #f0f9ff;
        border-radius: 0 10px 10px 0;
        padding: .8rem 1.1rem;
        margin-bottom: .6rem;
    }
    .offer-card b { color: #1e40af; }

    .status-ok  { color: #16a34a; font-weight: 600; }
    .status-err { color: #dc2626; font-weight: 600; }

    div[data-testid="stButton"] button {
        border-radius: 8px;
        font-weight: 600;
        padding: .45rem 1.3rem;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# Hero
# --------------------------------------------------------------------------- #

st.markdown("""
<div class="hero">
    <h1>🏦 Plataforma de Ofertas Adaptativas</h1>
    <p>Datathon 7-MLET · Grupo 28 · Thompson Sampling Contextual</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# Tabs
# --------------------------------------------------------------------------- #

tab_health, tab_offers, tab_decide, tab_reward = st.tabs([
    "🟢 Status da API",
    "📋 Catálogo de Ofertas",
    "🎯 Recomendar Oferta",
    "🔁 Registrar Conversão",
])

# ═══════════════════════════════════════════════════════════════════════════ #
# TAB 1 — HEALTH
# ═══════════════════════════════════════════════════════════════════════════ #

with tab_health:
    st.markdown('<span class="badge badge-get">GET</span> <code>/health</code>', unsafe_allow_html=True)
    st.caption("Verifica se a API está online e qual modelo está carregado.")
    st.markdown("")

    if st.button("Verificar status", key="btn_health"):
        with st.spinner("Consultando..."):
            try:
                r = requests.get(f"{API_URL}/health", timeout=15)
                data = r.json()
                status = data.get("status", "")
                cor = "status-ok" if status == "ok" else "status-err"
                icone = "✅" if status == "ok" else "❌"

                st.markdown(f"""
                <div class="card">
                    <h3>{icone} API <span class="{cor}">{status.upper()}</span></h3>
                    <table style="width:100%;font-size:.88rem;border-collapse:collapse">
                        <tr><td style="padding:.3rem .5rem;color:#64748b">Versão da política</td>
                            <td style="padding:.3rem .5rem;font-weight:600">{data.get('policy_version','—')}</td></tr>
                        <tr style="background:#f1f5f9"><td style="padding:.3rem .5rem;color:#64748b">Treinado em</td>
                            <td style="padding:.3rem .5rem">{data.get('trained_at','—')}</td></tr>
                        <tr><td style="padding:.3rem .5rem;color:#64748b">Segmentos aprendidos</td>
                            <td style="padding:.3rem .5rem;font-weight:600">{data.get('n_segments_learned','—')}</td></tr>
                        <tr style="background:#f1f5f9"><td style="padding:.3rem .5rem;color:#64748b">Total de ofertas</td>
                            <td style="padding:.3rem .5rem">{data.get('total_offers','—')}</td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro ao conectar: {e}")

# ═══════════════════════════════════════════════════════════════════════════ #
# TAB 2 — OFFERS
# ═══════════════════════════════════════════════════════════════════════════ #

with tab_offers:
    st.markdown('<span class="badge badge-get">GET</span> <code>/offers</code>', unsafe_allow_html=True)
    st.caption("Lista as 5 ofertas disponíveis com canais e taxa base.")
    st.markdown("")

    if st.button("Carregar catálogo", key="btn_offers"):
        with st.spinner("Buscando catálogo..."):
            try:
                r = requests.get(f"{API_URL}/offers", timeout=15)
                data = r.json()
                offers = data.get("offers", [])

                canal_icone = {
                    "app_mobile": "📱",
                    "internet_banking": "💻",
                    "sms": "💬",
                }

                for o in offers:
                    icone = canal_icone.get(o.get("canal", ""), "🏦")
                    st.markdown(f"""
                    <div class="offer-card">
                        <b>{o.get('offer_id')} — {o.get('name')}</b><br>
                        <span style="font-size:.82rem;color:#475569">
                            {icone} Canal: <b>{o.get('canal')}</b> &nbsp;|&nbsp;
                            Taxa base: <b>{round(o.get('base_rate',0)*100, 1)}%</b> &nbsp;|&nbsp;
                            Recompensa: <b>{o.get('reward_val')}</b>
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Erro ao conectar: {e}")

# ═══════════════════════════════════════════════════════════════════════════ #
# TAB 3 — DECIDE
# ═══════════════════════════════════════════════════════════════════════════ #

with tab_decide:
    st.markdown('<span class="badge badge-post">POST</span> <code>/decide</code>', unsafe_allow_html=True)
    st.caption("Preencha o perfil do cliente e receba a oferta recomendada pelo modelo.")
    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Idade", min_value=18, max_value=99, value=45)
        job = st.selectbox("Profissão", [
            "admin.", "blue-collar", "entrepreneur", "housemaid",
            "management", "retired", "self-employed", "services",
            "student", "technician", "unemployed", "unknown"
        ], index=4)
        marital = st.selectbox("Estado civil", ["married", "single", "divorced", "unknown"])
        education = st.selectbox("Escolaridade", [
            "basic.4y", "basic.6y", "basic.9y", "high.school",
            "illiterate", "professional.course", "university.degree", "unknown"
        ], index=6)

    with col2:
        default = st.selectbox("Inadimplente?", ["no", "yes", "unknown"])
        housing = st.selectbox("Empréstimo habitacional?", ["yes", "no", "unknown"])
        loan    = st.selectbox("Empréstimo pessoal?",      ["no", "yes", "unknown"])
        balance_group = st.selectbox("Faixa de saldo", ["medium", "low", "high"])

    st.markdown("")
    if st.button("🎯 Recomendar oferta", key="btn_decide"):
        payload = {
            "age": age, "job": job, "marital": marital,
            "education": education, "default": default,
            "housing": housing, "loan": loan,
            "balance_group": balance_group,
        }
        with st.spinner("Consultando modelo..."):
            try:
                r = requests.post(f"{API_URL}/decide", json=payload, timeout=15)
                data = r.json()

                reason_cor = {
                    "SUCCESS_CONTEXTUAL": "#16a34a",
                    "SUITABILITY_REVERTED": "#d97706",
                    "EXPLORATION_FORCE": "#7c3aed",
                }
                rc = data.get("reason_code", "")
                cor = reason_cor.get(rc, "#64748b")
                prob = data.get("estimated_conversion_prob")
                prob_txt = f"{round(prob*100,1)}%" if prob else "—"

                st.markdown(f"""
                <div class="card" style="border-left: 5px solid #3b82f6;">
                    <h3 style="font-size:1.2rem">
                        🏆 {data.get('offer_id')} — {data.get('offer_name')}
                    </h3>
                    <table style="width:100%;font-size:.88rem;border-collapse:collapse">
                        <tr><td style="padding:.3rem .5rem;color:#64748b">Canal</td>
                            <td style="padding:.3rem .5rem;font-weight:600">{data.get('canal')}</td></tr>
                        <tr style="background:#f1f5f9"><td style="padding:.3rem .5rem;color:#64748b">Segmento</td>
                            <td style="padding:.3rem .5rem">{data.get('segment')}</td></tr>
                        <tr><td style="padding:.3rem .5rem;color:#64748b">Motivo</td>
                            <td style="padding:.3rem .5rem;font-weight:600;color:{cor}">{rc}</td></tr>
                        <tr style="background:#f1f5f9"><td style="padding:.3rem .5rem;color:#64748b">Prob. de conversão</td>
                            <td style="padding:.3rem .5rem;font-weight:600">{prob_txt}</td></tr>
                        <tr><td style="padding:.3rem .5rem;color:#64748b">Versão da política</td>
                            <td style="padding:.3rem .5rem">{data.get('policy_version')}</td></tr>
                        <tr style="background:#f1f5f9"><td style="padding:.3rem .5rem;color:#64748b">Event ID</td>
                            <td style="padding:.3rem .5rem;font-family:monospace;font-size:.8rem">{data.get('event_id')}</td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)

                # Salva event_id e dados para usar na aba reward
                st.session_state["last_event_id"]  = data.get("event_id", "")
                st.session_state["last_offer_id"]  = data.get("offer_id", "")
                st.session_state["last_segment"]   = data.get("segment", "")

            except Exception as e:
                st.error(f"Erro ao conectar: {e}")

# ═══════════════════════════════════════════════════════════════════════════ #
# TAB 4 — REWARD
# ═══════════════════════════════════════════════════════════════════════════ #

with tab_reward:
    st.markdown('<span class="badge badge-post">POST</span> <code>/reward</code>', unsafe_allow_html=True)
    st.caption("Informe o resultado da oferta para atualizar o modelo (aprendizado online).")
    st.markdown("")

    # Pré-preenche com o último /decide se existir
    default_event  = st.session_state.get("last_event_id", "")
    default_offer  = st.session_state.get("last_offer_id", "OFF_001")
    default_seg    = st.session_state.get("last_segment", "")

    if default_event:
        st.info(f"✅ Usando dados da última decisão: **{default_event}**")

    event_id = st.text_input("Event ID", value=default_event,
                              placeholder="DEC-XXXXXXXXXXXX")
    offer_id = st.selectbox("Oferta", ["OFF_001","OFF_002","OFF_003","OFF_004","OFF_005"],
                             index=["OFF_001","OFF_002","OFF_003","OFF_004","OFF_005"].index(default_offer)
                             if default_offer in ["OFF_001","OFF_002","OFF_003","OFF_004","OFF_005"] else 0)
    segment  = st.text_input("Segmento", value=default_seg,
                              placeholder="management__mid__university")
    reward   = st.radio("Resultado", [1, 0],
                         format_func=lambda x: "✅ Converteu (1)" if x == 1 else "❌ Não converteu (0)")

    st.markdown("")
    if st.button("🔁 Registrar feedback", key="btn_reward"):
        if not event_id or not segment:
            st.warning("Preencha Event ID e Segmento.")
        else:
            payload = {
                "event_id": event_id,
                "offer_id": offer_id,
                "segment":  segment,
                "reward":   reward,
            }
            with st.spinner("Enviando feedback..."):
                try:
                    r = requests.post(f"{API_URL}/reward", json=payload, timeout=15)
                    data = r.json()

                    nova_est = data.get("new_estimate", 0)
                    st.markdown(f"""
                    <div class="card" style="border-left: 5px solid #16a34a;">
                        <h3>🔄 Modelo atualizado</h3>
                        <table style="width:100%;font-size:.88rem;border-collapse:collapse">
                            <tr><td style="padding:.3rem .5rem;color:#64748b">Event ID</td>
                                <td style="padding:.3rem .5rem;font-family:monospace;font-size:.8rem">{data.get('event_id')}</td></tr>
                            <tr style="background:#f1f5f9"><td style="padding:.3rem .5rem;color:#64748b">Oferta</td>
                                <td style="padding:.3rem .5rem;font-weight:600">{data.get('offer_id')}</td></tr>
                            <tr><td style="padding:.3rem .5rem;color:#64748b">Feedback</td>
                                <td style="padding:.3rem .5rem;font-weight:600">{"✅ Conversão" if data.get("reward")==1 else "❌ Sem conversão"}</td></tr>
                            <tr style="background:#f1f5f9"><td style="padding:.3rem .5rem;color:#64748b">Nova estimativa</td>
                                <td style="padding:.3rem .5rem;font-weight:600;color:#1d4ed8">{round(nova_est*100,2)}%</td></tr>
                        </table>
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Erro ao conectar: {e}")

# --------------------------------------------------------------------------- #
# Footer
# --------------------------------------------------------------------------- #

st.markdown("---")
st.markdown(
    "<p style='text-align:center;font-size:.8rem;color:#94a3b8'>"
    "Datathon 7-MLET · Grupo 28 · POS TECH · "
    "<a href='https://datathon-7mlet-grupo-28-1.onrender.com/docs' target='_blank'>Swagger API ↗</a>"
    "</p>",
    unsafe_allow_html=True,
)
