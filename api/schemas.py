"""
Schemas Pydantic para os contratos de entrada/saída da API.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


# --------------------------------------------------------------------------- #
# POST /decide — entrada
# --------------------------------------------------------------------------- #

class DecideRequest(BaseModel):
    """Contexto do cliente para decisão de oferta."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 45,
                "job": "management",
                "marital": "married",
                "education": "university.degree",
                "default": "no",
                "housing": "yes",
                "loan": "no",
                "balance_group": "medium",
            }
        }
    )

    age: int = Field(..., ge=18, le=99, description="Idade do cliente (18–99).")
    job: str = Field(
        ...,
        description=(
            "Profissão: admin., blue-collar, entrepreneur, housemaid, "
            "management, retired, self-employed, services, student, "
            "technician, unemployed, unknown."
        ),
    )
    marital: str = Field(..., description="Estado civil: divorced, married, single, unknown.")
    education: str = Field(
        ...,
        description=(
            "Escolaridade: basic.4y, basic.6y, basic.9y, high.school, "
            "illiterate, professional.course, university.degree, unknown."
        ),
    )
    default: Literal["yes", "no", "unknown"] = Field(
        ..., description="Possui crédito em inadimplência?"
    )
    housing: Literal["yes", "no", "unknown"] = Field(
        ..., description="Possui empréstimo habitacional?"
    )
    loan: Literal["yes", "no", "unknown"] = Field(
        ..., description="Possui empréstimo pessoal?"
    )
    balance_group: Optional[Literal["low", "medium", "high"]] = Field(
        default=None,
        description=(
            "Faixa de saldo em conta (opcional). "
            "Usado nas regras de suitability para CDB."
        ),
    )


# --------------------------------------------------------------------------- #
# POST /decide — saída
# --------------------------------------------------------------------------- #

class DecideResponse(BaseModel):
    """Decisão de oferta retornada pela política adaptativa."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "event_id": "DEC-A1B2C3D4E5F6",
                "offer_id": "OFF_002",
                "offer_name": "CDB 120% CDI",
                "canal": "internet_banking",
                "reason_code": "SUCCESS_CONTEXTUAL",
                "segment": "management__mid__university",
                "policy_version": "v1.0-thompson-contextual",
                "estimated_conversion_prob": 0.21,
            }
        }
    )

    event_id: str = Field(..., description="ID único da decisão para auditoria.")
    offer_id: str = Field(..., description="Código da oferta selecionada (OFF_001–OFF_005).")
    offer_name: str = Field(..., description="Nome legível da oferta.")
    canal: str = Field(..., description="Canal de entrega recomendado.")
    reason_code: str = Field(
        ...,
        description=(
            "Motivo da decisão: "
            "SUCCESS_CONTEXTUAL | SUITABILITY_REVERTED | EXPLORATION_FORCE."
        ),
    )
    segment: str = Field(..., description="Segmento do cliente: job__faixa_etaria__escolaridade.")
    policy_version: str = Field(..., description="Versão da política aplicada.")
    estimated_conversion_prob: Optional[float] = Field(
        default=None,
        description="Estimativa de conversão (média Beta posterior) para o braço escolhido.",
    )


# --------------------------------------------------------------------------- #
# POST /reward — entrada
# --------------------------------------------------------------------------- #

class RewardRequest(BaseModel):
    """Feedback de conversão para atualização online do bandit."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "event_id": "DEC-A1B2C3D4E5F6",
                "offer_id": "OFF_002",
                "segment": "management__mid__university",
                "reward": 1,
            }
        }
    )

    event_id: str = Field(..., description="event_id retornado pelo /decide.")
    offer_id: str = Field(..., description="Oferta que recebeu o feedback.")
    segment: str = Field(..., description="Segmento do cliente (retornado pelo /decide).")
    reward: Literal[0, 1] = Field(..., description="0 = sem conversão | 1 = converteu.")


# --------------------------------------------------------------------------- #
# GET /health — saída
# --------------------------------------------------------------------------- #

class HealthResponse(BaseModel):
    status: str
    policy_version: str
    trained_at: str
    n_segments_learned: int
    total_offers: int
