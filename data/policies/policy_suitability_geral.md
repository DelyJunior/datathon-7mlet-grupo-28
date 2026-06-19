# Política de Suitability — Term Deposit (SINTÉTICA)

> Documento fictício criado para fins de demonstração técnica do datathon.
> Não reflete política comercial real de nenhuma instituição.

## Regras de adequação (suitability)

1. Clientes com `default=yes` (crédito em situação de inadimplência) não devem
   receber abordagem via CALL consultivo — risco de mensagem inadequada sobre
   produto de investimento para perfil de risco elevado.

2. Clientes classificados como `age_senior` (>= 55 anos) E com `housing=no`
   E `loan=no` têm prioridade para abordagem CALL consultiva — perfil compatível
   com produto de longo prazo e maior disponibilidade para atendimento humano.

3. O braço SMS_URGENTE não deve ser usado mais de 2 vezes para o mesmo cliente
   em um intervalo de 30 dias — risco de percepção de pressão excessiva.

4. Clientes em segmento `student__young` não devem receber abordagem CALL —
   canal desproporcional ao perfil e ticket esperado do produto.
