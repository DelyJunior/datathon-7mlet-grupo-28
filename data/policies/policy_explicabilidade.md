# Diretrizes de Explicabilidade de Decisão de Ofertas

> Framework para auditoria e transparência das recomendações geradas pelo Bandit Contextual.

## Estrutura de Justificativa da Recomendação
Para cada oferta selecionada para o cliente, o sistema de logging deve registrar uma estrutura explicativa baseada em três pilares:

1.  **Variáveis Contextuais Chave (Context):** Identificar quais atributos do cliente (ex: `job`, `education`, `marital`, `balance_group`) mais pesaram para os parâmetros da distribuição Beta do segmento.
2.  **Métrica de Exploração/Explotação:** Gravar o valor do score amostrado que garantiu a vitória do braço vencedor versus os braços concorrentes no Thompson Sampling.
3.  **Filtro de Salvaguarda (Suitability Override):** Evidência explícita de que a recomendação passou pelo crivo de conformidade da instituição sem sofrer *fallback*.

## Códigos de Motivo (Reason Codes)
* `SUCCESS_CONTEXTUAL`: Oferta recomendada pelo maior score predito para o segmento.
* `SUITABILITY_REVERTED`: A oferta ótima do bandit violava suitability e o sistema aplicou o produto padrão/seguro.
* `EXPLORATION_FORCE`: Acionamento forçado de braço menos explorado para mitigação de *cold start*.
