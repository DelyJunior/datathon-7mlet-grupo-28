# Política Corpotativa de Suitability e Proteção ao Cliente

> Regras rígidas de elegibilidade e conformidade regulatória para oferta de produtos. Devem ser aplicadas como filtros pós-bandit (hard constraints).

## Regras de Adequação por Perfil de Risco

1.  **Proteção contra Superendividamento (Default Check):**
    * Clientes com restrição activa de crédito (`default == 'yes'`) estão **terminantemente proibidos** de receber ofertas de Crédito ou Cartões (`OFF_001`). 
    * *Fallback:* Em caso de seleção, reverter para conteúdo puramente informativo ou Seguro de Vida Básico (`OFF_003`).

2.  **Direcionamento de Investimentos Complexos (CDB 120%):**
    * A oferta `OFF_002` (CDB 120% CDI) exige um perfil de estabilidade financeira. Não deve ser ofertada para clientes no segmento `student` (estudantes) ou desempregados (`unemployed`), exceto se possuírem balanço em conta classificado como `high`.

3.  **Priorização de Canais por Faixa Etária:**
    * Clientes na faixa `age_senior` (>= 55 anos) que possuam baixa familiaridade com canais digitais (`housing == 'no'` ou interações baixas no app) devem ter o canal `call` priorizado para produtos complexos como Seguros (`OFF_003`), respeitando os limites da política de canais.
