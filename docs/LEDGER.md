# Regras de dinheiro

- `ledger` e append-only. Nenhum `UPDATE` em saldo em lugar nenhum.
- Saldo = `SUM(amount)` da conta. A view `v_balance` da isso.
- `balance_after` e gravado em cada linha e serve de conferencia.
- `idempotency_key` impede dobro em retry de rede: `bet:<id>`, `settle:<id>`, `dep:<id>`.
- Aposta faz `reserve -> settle -> release`. Sem duas apostas no mesmo saldo.
- Saque so sai do ledger depois de aprovado no backoffice.
