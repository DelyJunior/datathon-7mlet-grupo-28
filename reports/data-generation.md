# Relatório de Geração de Dados Sintéticos

Gerado em: 2026-06-29T18:40:55.426394
Seed: 42

---

## 1. Visão geral

Este relatório documenta o processo de geração da camada sintética de
experimentação adaptativa construída sobre o dataset **Bank Marketing (Kaggle)**.
O objetivo é criar evidência rastreável e reproduzível de que o mecanismo
de aprendizado adaptativo (Thompson Sampling Contextual) supera uma política
de controle determinística em termos de conversão e regret.

---

## 2. Fonte de dados

- **Dataset:** Bank Marketing (Kaggle — henriqueyamahata/bank-marketing)
- **Arquivo usado:** `bank-additional-full.csv` (separador `;`)
- **Clientes carregados:** 41,188
- **Colunas de contexto:** age, job, marital, education, default, housing, loan

### Colunas descartadas por vazamento temporal
As colunas abaixo só existem *após* o contato com o cliente e não podem ser
usadas em decisões tomadas antes do contato:

`duration`, `pdays`, `previous`, `poutcome`, `emp.var.rate`, `cons.price.idx`,
`cons.conf.idx`, `euribor3m`, `nr.employed`, `contact`, `month`, `day_of_week`

---

## 3. Catálogo de braços (ofertas)

O dataset original possui apenas um produto (depósito a prazo). Para o experimento
adaptativo, foram criados **5 braços sintéticos** com probabilidades
de conversão baseadas em hipóteses de domínio financeiro:

  - **OFF_001** Cartão de crédito sem anuidade (base_rate=10%, canal=app_mobile, reward_val=1.0)
  - **OFF_002** CDB 120% CDI (base_rate=7%, canal=internet_banking, reward_val=2.0)
  - **OFF_003** Seguro de vida (base_rate=6%, canal=app_mobile, reward_val=2.5)
  - **OFF_004** Empréstimo pessoal pré-aprovado (base_rate=13%, canal=sms, reward_val=1.2)
  - **OFF_005** Previdência privada PGBL (base_rate=5%, canal=internet_banking, reward_val=3.0)

### Boosts por segmento de cliente

Cada braço recebe ajustes positivos ou negativos na probabilidade base
conforme o perfil do cliente:

  **OFF_001 — Cartão de crédito sem anuidade**
    - `job_admin.`: ++0.06
    - `job_management`: ++0.04
    - `job_student`: ++0.05
    - `edu_university`: ++0.04
    - `marital_single`: ++0.03
    - `no_loan`: ++0.03

  **OFF_002 — CDB 120% CDI**
    - `job_management`: ++0.10
    - `job_retired`: ++0.06
    - `edu_university`: ++0.08
    - `age_senior`: ++0.05
    - `no_default`: ++0.04

  **OFF_003 — Seguro de vida**
    - `job_retired`: ++0.12
    - `age_senior`: ++0.08
    - `marital_married`: ++0.04
    - `has_housing`: ++0.03

  **OFF_004 — Empréstimo pessoal pré-aprovado**
    - `job_blue-collar`: ++0.08
    - `job_services`: ++0.06
    - `job_housemaid`: ++0.05
    - `edu_basic`: ++0.04
    - `has_loan`: -0.05

  **OFF_005 — Previdência privada PGBL**
    - `job_management`: ++0.10
    - `job_self-employed`: ++0.07
    - `edu_university`: ++0.09
    - `age_senior`: ++0.06
    - `no_default`: ++0.04


**Hipótese geral:** `P(conversão | cliente, braço) = base_rate + Σ boosts_ativos`
limitada entre 2% e 95%.

---

## 4. Parâmetros da simulação

| Parâmetro | Valor |
|-----------|-------|
| Eventos simulados | 5,000 |
| Braços (ofertas) | 5 |
| Algoritmos comparados | Baseline fixo, Thompson Simples, Thompson Contextual |
| Lag máximo de recompensa | 14 dias |
| Taxa de recompensas pendentes | 12% |
| Segmentos descobertos pelo Contextual | 97 |
| Seed aleatória | 42 |

---

## 5. Resultados comparativos

### Conversões observadas

| Algoritmo | Conversões | Taxa | Regret total | Regret últimos 10% |
|-----------|-----------|------|-------------|-------------------|
| Baseline fixo | 793 | 15.86% | 258.9 | 0.0536 |
| Thompson Simples | 764 | 15.28% | 276.4 | 0.0508 |
| Thompson Contextual | 845 | 16.90% | 217.7 | 0.0335 |

### Ganho do Thompson Contextual

- Sobre o **Baseline fixo**: +52 conversões (+6.6%)
- Sobre o **Thompson Simples**: +81 conversões (+10.6%)

**Interpretação do "Regret últimos 10%":**
- Baseline fixo: `0.0536` — constante, não aprende
- Thompson Simples: `0.0508` — menor, mas estabilizou
- Thompson Contextual: `0.0335` — o menor, aprendizado contínuo

---

## 6. Arquivos gerados

### data/synthetic_enrichment/

| Arquivo | Registros | Descrição |
|---------|-----------|-----------|
| `offer_catalog.json` | 5 | Catálogo de braços com boosts por perfil |
| `offer_events.parquet` | 5,000 | Impressões com contexto e ação imediata |
| `delayed_rewards.parquet` | 5,000 | Recompensas com lag e status |

### Distribuição de rewards

| Status | Registros | Percentual |
|--------|-----------|-----------|
| observed_positive | 736 | 14.7% |
| observed_negative | 4,155 | 83.1% |
| pending | 109 | 2.2% |

### reports/

| Arquivo | Descrição |
|---------|-----------|
| `comparacao_algoritmos.png` | Regret, conversões e taxa móvel dos 3 algoritmos |
| `heatmap_segmentos.png` | Estimativas do Thompson Contextual por segmento × oferta |
| `betas_por_segmento.png` | Distribuições Beta aprendidas por segmento |

---

## 7. Modelagem de delayed rewards

Cada evento de conversão recebe um atraso simulado antes de ser
observado pelo sistema:

- **Lag:** sorteado uniformemente entre 0 e 14 dias
- **Taxa de pendência:** 12% dos eventos positivos ficam com `reward_status=pending`
- **Regra de update:** o bandit só atualiza seus parâmetros Beta com
  rewards `observed_positive` ou `observed_negative` — eventos `pending`
  não entram no aprendizado até amadurecer

---

## 8. Declaração de honestidade

As probabilidades de conversão são **hipóteses de domínio**, não observações
reais de um banco em produção. Os boosts por segmento foram estimados com base
em conhecimento do setor financeiro e calibrados para produzir diferenciação
realista entre perfis.

Os números de conversão e regret apresentados **não representam uplift real
de negócio** — são evidência de que o mecanismo de aprendizado adaptativo
funciona corretamente dentro do simulador construído, com calibração
documentada e rastreável ao dataset original do Kaggle.

Em produção real, as probabilidades sintéticas seriam substituídas por
observações reais coletadas durante a fase de experimentação controlada.

---

## 9. Limitações conhecidas

1. **Boosts aditivos e independentes:** a função de probabilidade não captura
   interações entre features (ex.: `management + senior` pode ter efeito
   diferente de `management` e `senior` separados).
2. **Lag uniforme:** a distribuição de atraso das recompensas é uniforme
   entre 0 e 14 dias. Na prática, a maioria das conversões ocorre
   nos primeiros dias após o contato.
3. **Ambiente estacionário:** as probabilidades não variam ao longo do tempo.
   Em produção, seria necessário monitorar drift e retreinar periodicamente.
4. **Amostragem com reposição:** clientes são amostrados com reposição do
   dataset — um mesmo perfil pode aparecer múltiplas vezes na simulação.
5. **Golden set anotado com ground truth:** na prática, anotação humana
   cega seria necessária para avaliar os casos de forma independente.

---

## 10. Reprodutibilidade

Para reproduzir exatamente esses resultados:

```bash
# Instalar dependências
pip install pandas numpy pyarrow scipy matplotlib

# Rodar o notebook
jupyter notebook dados_sinteticos_bandit_contextual.ipynb
```

Todos os sorteios usam `RANDOM_SEED = 42` via `np.random.default_rng(42)`
e `random.seed(42)`. Os clientes são amostrados com `random_state` derivado
do gerador principal para garantir reprodutibilidade.
