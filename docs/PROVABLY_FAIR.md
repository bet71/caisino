# Como o jogador audita

1. Antes de apostar, a API devolve `server_seed_hash`.
2. Voce aposta com seu `client_seed` e `nonce`.
3. No fim da rodada a API devolve o `server_seed` cru.
4. Confira: `sha256(server_seed) == server_seed_hash` recebido no passo 1.
5. Recalcule: `HMAC_SHA256(server_seed, client_seed:nonce:dominio)`.

Se o hash bater no passo 4, o resultado do passo 5 nao podia ser mudado depois.
