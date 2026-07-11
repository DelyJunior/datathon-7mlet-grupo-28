"""
Log auditável de decisões (append-only JSONL).
Cada linha registra: event_id, timestamp, contexto, oferta, reason_code,
scores Thompson, policy_version — conforme Etapa 5 do datathon.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

LOG_PATH = Path(__file__).parent.parent / "logs" / "decisions.jsonl"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log_decision(
    context: dict,
    offer_id: str,
    offer_name: str,
    canal: str,
    reason_code: str,
    segment: str,
    scores: dict[str, float],
    policy_version: str,
    estimated_prob: Optional[float] = None,
) -> str:
    """Grava entrada auditável e devolve o event_id gerado."""
    event_id = f"DEC-{uuid.uuid4().hex[:12].upper()}"
    entry = {
        "event_id": event_id,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "policy_version": policy_version,
        "context": context,
        "segment": segment,
        "offer_id": offer_id,
        "offer_name": offer_name,
        "canal": canal,
        "reason_code": reason_code,
        "thompson_scores": {k: round(v, 4) for k, v in scores.items()},
        "estimated_conversion_prob": round(estimated_prob, 4) if estimated_prob is not None else None,
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return event_id
