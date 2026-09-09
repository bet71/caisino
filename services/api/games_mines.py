"""Mines: grade 5x5 com N minas, multiplicador por casa segura revelada."""
from __future__ import annotations
from decimal import Decimal
from rng import rand_int

SIZE, CELLS = 5, 25


def mines(server_seed, client_seed, nonce, count: int) -> set[int]:
    out = set()
    while len(out) < count:
        out.add(rand_int(server_seed, client_seed, nonce, len(out) * 97, CELLS, "mines"))
    return out


def multiplier(safe_revealed: int, count: int, house_edge: float = 0.03) -> Decimal:
    m = 1.0
    for i in range(safe_revealed):
        m *= (CELLS - i) / (CELLS - count - i)
    return Decimal(repr(m * (1 - house_edge))).quantize(Decimal("0.01"))


def cashout(stake: Decimal, revealed: int, count: int) -> Decimal:
    return (stake * multiplier(revealed, count)).quantize(Decimal("0.01")) if revealed else Decimal("0.00")
