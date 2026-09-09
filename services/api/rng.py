"""RNG provably fair: commit/reveal + HMAC deterministico.

Fluxo:
1. Servidor gera server_seed e publica APENAS o hash (commit).
2. Jogador envia client_seed e nonce.
3. Resultado = HMAC_SHA256(server_seed, client_seed:nonce) -> float em [0,1).
4. No fim, server_seed e revelado; o jogador reproduz o calculo e confere.
"""
from __future__ import annotations
import hashlib, hmac, secrets


def new_server_seed() -> str:
    return secrets.token_hex(32)


def commit(seed: str) -> str:
    return hashlib.sha256(seed.encode()).hexdigest()


def verify_commit(seed: str, commit_hash: str) -> bool:
    return hmac.compare_digest(commit(seed), commit_hash)


def rand_float(server_seed: str, client_seed: str, nonce: int, domain: str = "") -> float:
    """Deterministico: mesma entrada, mesmo resultado. Base de todo jogo."""
    msg = f"{client_seed}:{nonce}:{domain}".encode()
    digest = hmac.new(server_seed.encode(), msg, hashlib.sha256).digest()
    return int.from_bytes(digest[:8], "big") / float(1 << 64)


def rand_int(server_seed: str, client_seed: str, nonce: int, low: int, high: int, domain: str = "") -> int:
    """Inteiro uniforme em [low, high)."""
    return low + int(rand_float(server_seed, client_seed, nonce, domain) * (high - low))
