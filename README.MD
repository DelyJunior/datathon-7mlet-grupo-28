# Machine Learning Repository - BANK MARKETING DATASET
## Documentação Técnica e Dicionário de Dados para Modelagem Preditiva
**Data de Elaboração:** 18 de junho de 2026

---

## 1. Informações Gerais
Este documento fornece as especificações técnicas e a descrição detalhada do **Bank Marketing Dataset**, um conjunto de dados amplamente utilizado para o desenvolvimento de modelos de classificação em Machine Learning. O dataset contém informações sobre campanhas de marketing direto (chamadas telefônicas) de uma instituição bancária portuguesa.

* **Link de Acesso:** [Kaggle - Bank Marketing](https://www.kaggle.com/datasets/henriqueyamahata/bank-marketing)
* **Versão Utilizada:** `bank-additional-full.csv` (versão completa incluindo indicadores sociais e econômicos)
* **Licença:** CC0 1.0 Universal (Public Domain)
* **Criadores:** Sérgio Moro (ISCTE-IUL), Paulo Cortez (Univ. Minho), Paulo Rita (ISCTE-IUL)
* **Ano de Publicação:** 2014

---

## 2. Descrição do Dataset
O objetivo principal deste conjunto de dados é permitir a construção de modelos preditivos que determinem se um cliente irá subscrever (aderir) a um depósito a prazo bancário (variável target `y`). O sucesso da campanha é definido pela adesão do cliente ao produto oferecido durante o contato telefônico.

* **Número de Instâncias:** 41.188 registros
* **Número de Atributos:** 20 variáveis preditivas (features) + 1 variável alvo (target)
* **Período dos Dados:** Coletados entre maio de 2008 e novembro de 2010
* **Valores Faltantes:** Não existem valores nulos no dataset. No entanto, em diversas variáveis categóricas, os dados ausentes foram codificados com o rótulo `"unknown"`.
* **Qualidade dos Dados:** Considerada excelente para fins de treinamento de modelos, dada a ausência de valores nulos e a inclusão de variáveis de contexto macroeconômico.

---

## 3. Atributos e Features

### 3.1. Dados do Cliente Bancário
| Atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| **age** | Idade do cliente | Numérico |
| **job** | Tipo de profissão (12 categorias: admin, blue-collar, etc.) | Categórico |
| **marital** | Estado civil (divorced, married, single, unknown) | Categórico |
| **education** | Nível educacional (8 categorias: basic.4y, high.school, etc.) | Categórico |
| **default** | Possui crédito em inadimplência (default)? | Categórico |
| **housing** | Possui empréstimo habitacional? | Categórico |
| **loan** | Possui empréstimo pessoal? | Categórico |

### 3.2. Dados do Contato Atual
| Atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| **contact** | Tipo de comunicação (cellular, telephone) | Categórico |
| **month** | Mês do último contato (jan a dec) | Categórico |
| **day_of_week** | Dia da semana do último contato (mon a fri) | Categórico |
| **duration** | Duração do último contato em segundos | Numérico |

> ⚠️ **Atenção:** O atributo `duration` afeta drasticamente o alvo de saída (se `duration=0`, então `y='no'`). Esta variável não é conhecida antes de uma chamada ser realizada. Para obter um modelo preditivo realista, **esta variável deve ser descartada**, sendo utilizada apenas para fins de benchmark.

### 3.3. Dados de Campanhas Anteriores
| Atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| **campaign** | Número de contatos realizados durante esta campanha para este cliente | Numérico |
| **pdays** | Número de dias desde o último contato de uma campanha anterior (999 significa que não foi contatado) | Numérico |
| **previous** | Número de contatos realizados antes desta campanha para este cliente | Numérico |
| **poutcome** | Resultado da campanha de marketing anterior (failure, nonexistent, success) | Categórico |

### 3.4. Indicadores Sociais e Econômicos
| Atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| **emp_var_rate** | Taxa de variação do emprego - indicador trimestral | Numérico |
| **cons_price_idx** | Índice de preços ao consumidor - indicador mensal | Numérico |
| **cons_conf_idx** | Índice de confiança do consumidor - indicador mensal | Numérico |
| **euribor3m** | Taxa Euribor a 3 meses - indicador diário | Numérico |
| **nr_employed** | Número de empregados no mercado - indicador trimestral | Numérico |

### 3.5. Variável Target
| Atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| **y** | O cliente subscreveu o depósito a prazo? (yes, no) | Binário |

---

## 4. Enriquecimento Sintético, Baseline e Estratégia Algorítmica

### 4.1. Objetivo da Camada de Experimentação Adaptativa
O objetivo desta camada é simular um ambiente de produção dinâmico e realista (sistema de recomendação em tempo real) sobreposto ao dataset estático do Banco de Portugal (*Kaggle*). Em vez de apenas prever passivamente se um cliente aceitaria um depósito a prazo, o sistema adota uma postura ativa: ele precisa decidir, de forma adaptativa e a cada interação, qual é a melhor oferta/canal para maximizar a taxa de conversão global (recompensa acumulada), equilibrando a exploração de novas estratégias (*exploration*) e a aplicação do conhecimento já adquirido (*exploitation*).

### 4.2. Catálogo Sintético de Braços e Ofertas
Para desatrelar a decisão do contexto original rígido, foi estruturado um catálogo de ofertas independente, onde cada opção atua como um "braço" (*arm*) no ecossistema do Bandit. O catálogo mapeia as ações disponíveis para o algoritmo:

* **Braço 0 (Targeted Call - Premium):** Abordagem telefônica personalizada com foco em investidores de alta renda.
* **Braço 1 (Digital Banner - App):** Oferta contextual integrada diretamente no aplicativo do banco, com custo operacional quase zero.
* **Braço 2 (Email Marketing - Flex):** Comunicação massiva por e-mail com condições de resgate flexíveis.
* **Braço 3 (SMS Urgent - Escalonado):** Mensagem curta focada em gatilhos de escassez ou taxas promocionais de curto prazo.

### 4.3. Geração de Eventos e Ambiente de Simulação (Sementes Controladas)
Para garantir a reprodutibilidade dos experimentos científicos do Datathon, todo o fluxo gerador de dados foi blindado com sementes aleatórias estritas (`numpy.random.default_rng(seed=42)`). O ambiente gera deterministicamente:
1.  **Eventos de Impressão (Decision Context):** Características demográficas e macroeconômicas extraídas do cliente são expostas ao algoritmo.
2.  **Contexto de Decisão:** Vetores de características que influenciam as probabilidades latentes de conversão de cada braço.
3.  **Recompensas Intermediárias:** Sinais imediatos de engajamento (cliques ou interações preliminares) antes do desfecho final da recompensa.

### 4.4. Modelagem de Recompensas Atrasadas (Delayed Rewards) e Horizonte Temporal
Em campanhas de marketing bancário, a decisão de investimento raramente é instantânea. O projeto modela explicitamente esse comportamento:
* **Horizonte Temporal ($T$):** Simulação estruturada ao longo de rodadas sequenciais representando o fluxo contínuo de clientes.
* **Delayed Rewards:** O retorno definitivo do cliente (conversão em depósito) é indexado por uma função de atraso exponencial ou geométrica. O algoritmo toma a decisão no momento $t$, mas a confirmação da recompensa ($R_t \in \{0, 1\}$) pode ser computada muitas rodadas depois, simulando o efeito real de "janelas de conversão" bancárias.

### 4.5. Schema dos Arquivos Sintéticos Gerados
O processo de enriquecimento exporta os seguintes artefatos estruturados na pasta `data/synthetic_enrichment/`:

* `offer_catalog.json`: Estrutura de metadados, identificadores e restrições de elegibilidade dos braços operacionais.
* `offer_events.parquet`: Log de impressões contendo `timestamp`, `client_id`, `arm_allocated`, `context_features_vector` e `immediate_click`.
* `delayed_rewards.parquet`: Tabela de fechamento financeiro contendo `event_id`, `conversion_status` ($0$ ou $1$) e `delay_rounds_duration`.
* `bandit_snapshots.json`: Histórico do estado interno dos parâmetros dos algoritmos para fins de auditoria e explicabilidade.

### 4.6. Estratégia Algorítmica e Comparação com Políticas Simples

O ecossistema contrapõe abordagens tradicionais estáticas a modelos de aprendizado por reforço contextual:

[Contexto do Cliente] ──> ┌────────────────────────────────────────┐
│       Mecanismo de Decisão (Policy)    │
└────────────────────────────────────────┘
│
┌──────────────────────────┴──────────────────────────┐
▼                                                     ▼
┌───────────────────────────────┐                     ┌───────────────────────────────┐
│    Baseline Determinístico    │                     │    Thompson Sampling / UCB    │
│  (Sempre o mesmo canal / RTS) │                     │   (Escolha Bayesiana Dinâmica)│
└───────────────────────────────┘                     └───────────────────────────────┘
│                                                     │
▼                                                     ▼
Recompensa Estática (Baixa)                           Recompensa Otimizada (Alta)

#### I. Baseline Determinístico (Abordagem Simples)
Como linha de base competitiva, adota-se a política **Random/Static Allocation** ou **Greedy Fixo**:
* O sistema aloca sempre o canal tradicional telefônico padrão (ou distribui as ofertas uniformemente sem aprender com o histórico).
* **Limitação:** Ignora o contexto macroeconômico (como a taxa Euribor atual) e o perfil do cliente, gerando um custo de oportunidade massivo.

#### II. Thompson Sampling Contextual
A principal abordagem estocástica implementada baseia-se na formulação Bayesiana:
* Para cada braço, mantém-se uma distribuição de probabilidade a priori (Beta-Binomial para recompensas binárias ou regressão linear Bayesiana para o cenário contextual).
* A cada rodada, o algoritmo amostra parâmetros dessas distribuições e escolhe o braço que apresenta a maior recompensa esperada amostrada. Ao receber o feedback (mesmo que atrasado), as distribuições *posterioris* são atualizadas.

#### III. Justificativa Teórica do Nilos-UCB / Análise Algorítmica
Para contornar o problema severo de **recompensas atrasadas** (onde o Thompson Sampling padrão ou o UCB tradicional falham por atualizarem os pesos assumindo feedback instantâneo), introduz-se a lógica inspirada no **Nilos-UCB** (ou variantes de *Optimism under Delayed Feedback*):
* **Justificativa:** O algoritmo ajusta as fronteiras de exploração adicionando um termo de penalidade ou buffers temporais baseados no número de recompensas ainda pendentes (*instâncias em vôo*). Isso evita que um braço excelente seja temporariamente abandonado (sofra injustamente) apenas porque suas conversões reais demoram dias para serem processadas pelo sistema central do banco.

### 4.7. Métricas de Performance Avaliadas
O sucesso da estratégia algorítmica é mensurado através de quatro dimensões críticas:

1.  **Recompensa Acumulada (Cumulative Reward):** Total de conversões financeiras reais convertidas pelo banco ao longo do horizonte $T$.
2.  **Regret Acumulado (Regret Analysis):** Diferença teórica entre a receita obtida pela política ótima (oráculo que conhece as probabilidades reais) e a política implementada pelo algoritmo. O objetivo é obter um crescimento de *regret sublinear*.
3.  **Taxa de Conversão Simulada (Conversion Rate):** Proporção de vendas ganhas sobre o total de ofertas impressas ($\frac{\sum R_t}{T}$).
4.  **Perfil de Exploração vs. Explotação:** Gráfico de convergência indicando em qual rodada o algoritmo estabiliza a identificação dos braços ótimos para cada segmento de cliente.

### 4.8. Tratamento de Cold-Start e Recompensas Atrasadas
* **Cold-Start (Novos Clientes / Novos Braços):** O sistema inicializa os parâmetros com distribuições não informativas (Ex: $Beta(1,1)$). Nas primeiras rodadas, o componente de variância força uma exploração puramente uniforme para coletar dados iniciais rapidamente, mitigando o risco de rejeição precoce de novos canais de marketing.
* **Tratamento de Delays:** O algoritmo utiliza uma fila de atualização assíncrona baseada no identificador do evento. As atualizações de matrizes de covariância ou contadores de sucessos/falhas ocorrem em lotes ou de forma tardia no exato momento do recebimento do sinal de conversão do Parquet, sem bloquear a tomada de decisão em tempo real dos novos clientes entrantes.

---


<!--
## 4. Limitações e Considerações
Para a utilização correta deste dataset em ambientes de produção ou pesquisa acadêmica, as seguintes limitações devem ser observadas:

* **Vazamento de Dados (Data Leakage):** A variável `duration` é altamente correlacionada com o target, pois chamadas mais longas geralmente indicam maior interesse. Contudo, sua duração só é conhecida após o término da interação, tornando-a inviável para modelos de predição em tempo real.
* **Dados Faltantes Ocultos:** Embora não existam valores nulos (`NaN`), o rótulo `unknown` deve ser tratado como dado faltante durante a fase de limpeza e imputação.
* **Desbalanceamento de Classes:** O dataset apresenta um desbalanceamento significativo entre as classes "yes" e "no". Técnicas de reamostragem (SMOTE, Undersampling) ou ajuste de pesos de classe são recomendadas.
* **Contexto Geográfico e Temporal:** Os dados refletem a realidade de um banco em Portugal entre 2008 e 2010. Modelos treinados aqui podem não generalizar para outros países ou períodos econômicos distintos (ex: pós-pandemia).
* **Indicadores Econômicos:** Os valores de indicadores como a Euribor e índices de confiança são históricos e podem não refletir a volatilidade dos mercados financeiros atuais.

---

## 5. Citação Recomendada
Caso utilize este dataset em trabalhos acadêmicos ou publicações, utilize a seguinte referência:

> [Moro et al., 2014] S. Moro, P. Cortez and P. Rita. *A Data-Driven Approach to Predict the Success of Bank Telemarketing*. Decision Support Systems, In press, http://dx.doi.org/10.1016/j.dss.2014.03.001

---

## 6. Referências
* [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/datasets/Bank+Marketing)
* [Banco de Portugal (Estatísticas)](https://www.bportugal.pt/estatisticasweb)
* [Artigo Original](http://dx.doi.org/10.1016/j.dss.2014.03.001)

---

[c## 7. Estrutura de Arquivos
```text
data/kaggle/
├── README.md (este arquivo)
└── bank-additional-full.csv (dataset completo)
-->
