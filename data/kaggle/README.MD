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


<!--
## 3. Limitações e Considerações
Para a utilização correta deste dataset em ambientes de produção ou pesquisa acadêmica, as seguintes limitações devem ser observadas:

* **Vazamento de Dados (Data Leakage):** A variável `duration` é altamente correlacionada com o target, pois chamadas mais longas geralmente indicam maior interesse. Contudo, sua duração só é conhecida após o término da interação, tornando-a inviável para modelos de predição em tempo real.
* **Dados Faltantes Ocultos:** Embora não existam valores nulos (`NaN`), o rótulo `unknown` deve ser tratado como dado faltante durante a fase de limpeza e imputação.
* **Desbalanceamento de Classes:** O dataset apresenta um desbalanceamento significativo entre as classes "yes" e "no". Técnicas de reamostragem (SMOTE, Undersampling) ou ajuste de pesos de classe são recomendadas.
* **Contexto Geográfico e Temporal:** Os dados refletem a realidade de um banco em Portugal entre 2008 e 2010. Modelos treinados aqui podem não generalizar para outros países ou períodos econômicos distintos (ex: pós-pandemia).
* **Indicadores Econômicos:** Os valores de indicadores como a Euribor e índices de confiança são históricos e podem não refletir a volatilidade dos mercados financeiros atuais.

---

## 4. Citação Recomendada
Caso utilize este dataset em trabalhos acadêmicos ou publicações, utilize a seguinte referência:

> [Moro et al., 2014] S. Moro, P. Cortez and P. Rita. *A Data-Driven Approach to Predict the Success of Bank Telemarketing*. Decision Support Systems, In press, http://dx.doi.org/10.1016/j.dss.2014.03.001

---

## 5. Referências
* [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/datasets/Bank+Marketing)
* [Banco de Portugal (Estatísticas)](https://www.bportugal.pt/estatisticasweb)
* [Artigo Original](http://dx.doi.org/10.1016/j.dss.2014.03.001)

---

