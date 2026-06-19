# Diretrizes de Explicabilidade de Decisão (SINTÉTICA)

> Documento fictício para orientar o assistente LLM na geração de explicações.

## Estrutura esperada de uma explicação de decisão

Toda decisão do bandit deve ser explicável em 3 partes:
1. **Segmento do cliente**: a que grupo o cliente pertence e sua taxa de conversão
   histórica observada na base.
2. **Braço escolhido**: qual canal/CTA foi selecionado e por quê (estimativa do bandit).
3. **Verificação de suitability**: confirmação de que a escolha não viola nenhuma
   regra do documento de suitability.

Se uma decisão violar suitability, o sistema deve reverter para o braço de
referência (ARM_EMAIL_SOFT) e registrar reason_code='suitability_override'.
