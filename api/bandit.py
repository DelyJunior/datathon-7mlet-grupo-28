"""
Motor de decisão: Thompson Sampling Contextual.
Carrega o modelo treinado (thompson_contextual.pkl) e aplica filtros de suitability.

Formato das chaves no pkl: job__age_group__edu_group__offer_id
  age_group : young (<=30) | mid (31-54) | senior (>=55)
  edu_group : university | basic | other
"""

import pickle
from pathlib import Path
from typing import Optional

import numpy as np

# --------------------------------------------------------------------------- #
# Carregamento do modelo treinado
# --------------------------------------------------------------------------- #

MODEL_PATH = Path(__file__).parent.parent / "models" / "thompson_contextual.pkl"

with open(MODEL_PATH, "rb") as _f:
    _MODEL: dict = pickle.load(_f)

OFFER_IDS: list[str] = _MODEL["offer_ids"]
CATALOG: list[dict] = _MODEL["catalog"]
OFFER_MAP: dict[str, dict] = {o["offer_id"]: o for o in CATALOG}
POLICY_VERSION: str = _MODEL["policy_version"]
TRAINED_AT: str = _MODEL["trained_at"]

# Estado do bandit (mutável durante o runtime para aprendizado online)
_alpha: dict[str, float] = dict(_MODEL["alpha"])
_beta: dict[str, float] = dict(_MODEL["beta"])

_rng = np.random.default_rng(42)

# --------------------------------------------------------------------------- #
# Helpers de contexto → segmento
# --------------------------------------------------------------------------- #

def _age_group(age: int) -> str:
    if age <= 30:
        return "young"
    if age <= 54:
        return "mid"
    return "senior"


def _edu_group(education: str) -> str:
    edu = education.lower()
    if "university" in edu:
        return "university"
    if edu.startswith("basic"):
        return "basic"
    return "other"


def build_segment(age: int, job: str, education: str) -> str:
    """Retorna chave de segmento no formato job__age_group__edu_group."""
    return f"{job}__{_age_group(age)}__{_edu_group(education)}"


# --------------------------------------------------------------------------- #
# Thompson Sampling
# --------------------------------------------------------------------------- #

def _chave(segment: str, offer_id: str) -> str:
    return f"{segment}__{offer_id}"


def _garantir(segment: str) -> None:
    """Inicializa priors Beta(1,1) para segmento nunca visto."""
    for oid in OFFER_IDS:
        k = _chave(segment, oid)
        if k not in _alpha:
            _alpha[k] = 1.0
            _beta[k] = 1.0


def thompson_sample(segment: str, eligible: list[str]) -> tuple[str, dict[str, float]]:
    """
    Amostra distribuições Beta por segmento × oferta e devolve o braço vencedor.
    Retorna (offer_id_vencedor, dict de scores).
    """
    _garantir(segment)
    scores: dict[str, float] = {}
    for oid in eligible:
        k = _chave(segment, oid)
        a = _alpha.get(k, 1.0)
        b = _beta.get(k, 1.0)
        scores[oid] = float(_rng.beta(a, b))
    winner = max(scores, key=scores.__getitem__)
    return winner, scores


def update_bandit(segment: str, offer_id: str, reward: int) -> float:
    """Atualiza Beta com feedback e retorna nova estimativa pontual."""
    k = _chave(segment, offer_id)
    if k not in _alpha:
        _alpha[k] = 1.0
        _beta[k] = 1.0
    if reward == 1:
        _alpha[k] += 1
    else:
        _beta[k] += 1
    return _alpha[k] / (_alpha[k] + _beta[k])


def estimate(segment: str, offer_id: str) -> float:
    """Estimativa pontual (média da Beta posterior) para segmento × oferta."""
    k = _chave(segment, offer_id)
    a = _alpha.get(k, 1.0)
    b = _beta.get(k, 1.0)
    return a / (a + b)


def n_segments() -> int:
    return len({k.rsplit("__", 1)[0] for k in _alpha})


# --------------------------------------------------------------------------- #
# Filtro de suitability (policy_suitability_geral.md)
# --------------------------------------------------------------------------- #

def suitability_ok(ctx: dict, offer_id: str) -> tuple[bool, str]:
    """
    Retorna (aprovado, motivo).
    Implementa as regras de data/policies/policy_suitability_geral.md.
    """
    default = str(ctx.get("default", "no")).lower()
    job = str(ctx.get("job", "")).lower()
    balance_group = str(ctx.get("balance_group", "medium")).lower()

    # Regra 1 — default=yes bloqueia crédito/cartão (OFF_001) e empréstimo (OFF_004)
    if default == "yes" and offer_id in ("OFF_001", "OFF_004"):
        return False, f"BLOCK_DEFAULT_{offer_id}"

    # Regra 2 — CDB (OFF_002) vedado para estudante/desempregado sem saldo high
    if offer_id == "OFF_002" and job in ("student", "unemployed") and balance_group != "high":
        return False, "BLOCK_CDB_PROFILE"

    return True, "OK"


def apply_suitability(
    ctx: dict, winner: str, scores: dict, eligible: list[str]
) -> tuple[str, str]:
    """
    Verifica suitability no braço vencedor. Se bloqueado, escala para
    o próximo melhor braço elegível. Retorna (offer_id_final, reason_code).
    """
    ok, _ = suitability_ok(ctx, winner)
    if ok:
        return winner, "SUCCESS_CONTEXTUAL"

    # Tenta alternativas em ordem de score decrescente
    ranked = sorted(eligible, key=lambda o: scores.get(o, 0), reverse=True)
    for alt in ranked:
        if alt == winner:
            continue
        ok2, _ = suitability_ok(ctx, alt)
        if ok2:
            return alt, "SUITABILITY_REVERTED"

    # Fallback final: Seguro de Vida (menor risco regulatório)
    return "OFF_003", "SUITABILITY_REVERTED"
