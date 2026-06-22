# Política de Canais e Distribuição de Ofertas

> Diretrizes operacionais para distribuição do catálogo de produtos financeiros via canais digitais e assistidos.

## Canais e Custos Operacionais
As decisões do modelo de Bandit Contextual devem considerar o impacto financeiro do canal atrelado à oferta. Os custos relativos (`custo_rel`) definidos no catálogo servem como penalizadores ou balizadores de margem:

* **App Mobile (`app_mobile`):** Canal de custo marginal zero. Indicado para volumetria alta e ofertas massificadas (ex: Cartão de Crédito).
* **Internet Banking (`internet_banking`):** Canal digital focado em ambiente logado desktop. Custo operacional nulo, com alta propensão a produtos de investimento.
* **Call Center (`call`):** Canal humano de altíssimo custo operacional. Deve ser priorizado estritamente onde o ganho esperado (`reward_val` * probabilidade) compense o acionamento da PA (Posição de Atendimento).

## Restrição de Orçamento e Volumetria
O braço ou combinação com canal `call` possui restrição de capacidade diária. Modelos de exploração (como Thompson Sampling) não devem alocar mais do que 20% do tráfego total do dia para interações telefônicas humanas em segmentos de baixa conversão.
