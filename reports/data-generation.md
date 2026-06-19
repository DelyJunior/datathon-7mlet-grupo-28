# Relatório de geração de dados sintéticos — v2

Gerado em: 2026-06-19T17:48:41.424754
Seed: 42

## Mudanças em relação à v1 (alinhamento com orientação do coordenador)

1. **Braços redefinidos**: variações de canal/CTA do produto único do Kaggle
   (term deposit), não mais produtos financeiros inventados.
2. **Calibração por âncora**: a probabilidade de conversão de cada braço é
   `y_real_do_segmento × multiplicador_do_braço`. O braço de referência
   (ARM_EMAIL_SOFT) é o mais próximo do dado observado.
3. **Fila real de delayed rewards**: implementada com heap, eventos amadurecem
   em rounds futuros reais dentro do loop de simulação — não é mais um sorteio
   instantâneo de status.
4. **Documentos de política (RAG)**: criados em data/policies/, sintéticos e
   declarados como tal.
5. **Golden set**: expandido com categoria 'suitability' cobrindo tentativas
   de furar regras de adequação.

## Parâmetros
- Eventos simulados: 5,000
- Braços: 5
- Lag máximo: 14 rounds
- Segmentos distintos no Kaggle: 35
- Shrinkage aplicado para segmentos com < 15 amostras

## Declaração de honestidade (conforme orientação)

A recompensa é sintética e calibrada a partir do `y` real do Bank Marketing,
mas o multiplicador de cada braço (canal/CTA) é uma hipótese de domínio, não
um resultado de produção. Os números de conversão e regret apresentados neste
projeto **não representam uplift real de negócio** — são evidência de que o
mecanismo de aprendizado adaptativo funciona corretamente dentro do simulador
construído, com calibração defensável e rastreável ao dado original.

## Limitações
- O multiplicador de cada braço é fixo — não captura interação canal × segmento.
- Shrinkage para segmentos pequenos usa peso linear simples, não um modelo bayesiano completo.
- A fila de delayed rewards assume lag uniforme entre 1 e 14 rounds.
