"""Crash: ponto de queda com cauda pesada e casa embutida.

Distribuicao: crash = max(1.00, (1 - house_edge) / (1 - u)) com u em [0,1).
RTP alvo = 1 - house_edge. O ponto de queda e decidido ANTES de qualquer cashout,
e fica preso ao server_seed revelado, entao o jogador audita depois.
"""
from __future__ import annotations
from decimal import Decimal
from rng import rand_float

HOUSE_EDGE = Decimal("0.04")


def crash_point(server_seed: str, client_seed: str, nonce: int) -> Decimal:
    u = rand_float(server_seed, client_seed, nonce, domain="crash")
    if u >= 1 - 1e-12:
        return Decimal("10000.00")
    raw = (Decimal(1) - HOUSE_EDGE) / (Decimal(1) - Decimal(repr(u)))
    return max(Decimal("1.00"), raw.quantize(Decimal("0.01")))


def cashout_payout(stake: Decimal, cashout_at: Decimal, crash: Decimal) -> Decimal:
    """Cashout antes da queda paga; depois disso a aposta esta perdida."""
    return (stake * cashout_at).quantize(Decimal("0.01")) if cashout_at <= crash else Decimal("0.00")
