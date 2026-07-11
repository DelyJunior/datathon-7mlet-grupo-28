"""
API de Decisão de Ofertas — Datathon 7-MLET Grupo 28
Etapa 5: Serviço demonstrável com Thompson Sampling Contextual

Endpoints:
  GET  /health   → Status da API e do modelo carregado
  GET  /offers   → Catálogo das 5 ofertas
  POST /decide   → Recebe contexto do cliente → retorna oferta recomendada
  POST /reward   → Registra feedback de conversão (aprendizado online)
  GET  /docs     → Swagger UI interativo
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.bandit import (
    CATALOG,
    OFFER_IDS,
    OFFER_MAP,
    POLICY_VERSION,
    TRAINED_AT,
    apply_suitability,
    build_segment,
    estimate,
    n_segments,
    thompson_sample,
    update_bandit,
)
from api.audit_log import log_decision
from api.schemas import (
    DecideRequest,
    DecideResponse,
    HealthResponse,
    RewardRequest,
)

# --------------------------------------------------------------------------- #
# App
# --------------------------------------------------------------------------- #

app = FastAPI(
    title="Datathon 7-MLET — API de Decisão de Ofertas",
    description=(
        "Plataforma de experimentação adaptativa (multi-armed bandit contextual) "
        "para recomendação de ofertas financeiras.\n\n"
        "**Grupo 28 | Datathon 7-MLET | POS TECH**\n\n"
        "O modelo Thompson Sampling Contextual foi treinado sobre dados sintéticos "
        "derivados do Bank Marketing Dataset (Kaggle). "
        "Filtros de suitability são aplicados pós-bandit, conforme "
        "`data/policies/policy_suitability_geral.md`."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------------- #
# GET /health
# --------------------------------------------------------------------------- #

@app.get("/health", response_model=HealthResponse, tags=["Operacional"])
def health():
    """Verifica status da API e do modelo carregado."""
    return HealthResponse(
        status="ok",
        policy_version=POLICY_VERSION,
        trained_at=TRAINED_AT,
        n_segments_learned=n_segments(),
        total_offers=len(OFFER_IDS),
    )


# --------------------------------------------------------------------------- #
# GET /offers
# --------------------------------------------------------------------------- #

@app.get("/offers", tags=["Catálogo"])
def list_offers():
    """Retorna o catálogo completo das 5 ofertas com boosts e canais."""
    return {
        "total": len(CATALOG),
        "offers": [
            {
                "offer_id": o["offer_id"],
                "name": o["name"],
                "canal": o["canal"],
                "base_rate": o["base_rate"],
                "reward_val": o["reward_val"],
                "boosts": o["boosts"],
            }
            for o in CATALOG
        ],
    }


# --------------------------------------------------------------------------- #
# POST /decide
# --------------------------------------------------------------------------- #

@app.post("/decide", response_model=DecideResponse, tags=["Decisão"])
def decide(req: DecideRequest):
    """
    Recebe o contexto do cliente e retorna a oferta recomendada.

    **Fluxo:**
    1. Determina o segmento do cliente (`job__faixa_etaria__escolaridade`).
    2. Executa Thompson Sampling: amostra distribuições Beta por segmento × oferta.
    3. Aplica filtro de suitability pós-bandit.
    4. Grava log auditável em `logs/decisions.jsonl`.
    5. Retorna oferta, canal, reason_code e policy_version.

    **Reason codes:**
    - `SUCCESS_CONTEXTUAL` — braço vencedor aprovado pelo suitability.
    - `SUITABILITY_REVERTED` — braço ótimo violava política; alternativa aplicada.
    """
    ctx = req.model_dump()

    segment = build_segment(
        age=ctx["age"],
        job=ctx["job"],
        education=ctx["education"],
    )

    winner, scores = thompson_sample(segment, OFFER_IDS)
    final_offer_id, reason_code = apply_suitability(ctx, winner, scores, OFFER_IDS)

    offer = OFFER_MAP[final_offer_id]
    est_prob = estimate(segment, final_offer_id)

    event_id = log_decision(
        context=ctx,
        offer_id=final_offer_id,
        offer_name=offer["name"],
        canal=offer["canal"],
        reason_code=reason_code,
        segment=segment,
        scores=scores,
        policy_version=POLICY_VERSION,
        estimated_prob=est_prob,
    )

    return DecideResponse(
        event_id=event_id,
        offer_id=final_offer_id,
        offer_name=offer["name"],
        canal=offer["canal"],
        reason_code=reason_code,
        segment=segment,
        policy_version=POLICY_VERSION,
        estimated_conversion_prob=round(est_prob, 4),
    )


# --------------------------------------------------------------------------- #
# POST /reward
# --------------------------------------------------------------------------- #

@app.post("/reward", tags=["Decisão"])
def reward(req: RewardRequest):
    """
    Registra feedback de conversão para atualização online do bandit.

    - `reward = 1` → incrementa `alpha` (sucesso).
    - `reward = 0` → incrementa `beta` (sem conversão).

    Representa o ciclo de feedback de delayed rewards descrito na Etapa 2.
    """
    if req.offer_id not in OFFER_IDS:
        raise HTTPException(
            status_code=400,
            detail=f"offer_id inválido: '{req.offer_id}'. Válidos: {OFFER_IDS}",
        )

    new_est = update_bandit(req.segment, req.offer_id, req.reward)

    return {
        "status": "updated",
        "event_id": req.event_id,
        "offer_id": req.offer_id,
        "segment": req.segment,
        "reward": req.reward,
        "new_estimate": round(new_est, 4),
    }
