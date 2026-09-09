# Casino

Plataforma de casino online: wallet com ledger imutavel, RNG provably fair e 5 jogos.

## Subir em um comando
```bash
cp .env.example .env
docker compose up -d --build
```
App: http://localhost:8080 · Admin: http://localhost:8080/admin

## Regras de dinheiro
- Saldo nunca e `UPDATE`. Todo movimento e um lancamento no ledger.
- Saldo = `SUM(ledger.amount)`. Invariante testada em `tests/test_ledger.py`.
- Aposta passa por `reserve -> settle -> release`.

## Regras de justo
- `server_seed` gerado no servidor, hash SHA-256 revelado antes da aposta (commit/reveal).
- Resultado = HMAC_SHA256(server_seed, client_seed:nonce). O jogador reproduce e confere.
- RTP verificado em simulacao de 200.000 rodadas em `tests/test_rtp.py`.

Veja `docs/PROVABLY_FAIR.md` e `docs/LEDGER.md`.
