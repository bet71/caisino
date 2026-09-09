"""Slots: reels com paylines e RTP alvo por construcao, nao por sorte.

O RTP nao e medido depois: a tabela de pagamentos e calibrada para fechar o alvo.
tests/test_rtp.py simula 1.000.000 de rodadas e falha se sair da faixa.
"""
from __future__ import annotations
from decimal import Decimal
from rng import rand_int

REELS = 5
ROWS = 3
PAYLINES = [
    (0, 0, 0, 0, 0), (2, 2, 2, 2, 2), (1, 1, 1, 1, 1),
    (0, 1, 2, 1, 0), (2, 1, 0, 1, 2),
]
# simbolo -> (peso no reel, pagamento para 3, 4, 5 iguais seguidos)
SYMBOLS = {
    "wild":  (2, (Decimal("2"), Decimal("6"), Decimal("20"))),
    "scatter": (3, (Decimal("1"), Decimal("3"), Decimal("10"))),
    "seven": (5, (Decimal("1.5"), Decimal("5"), Decimal("15"))),
    "gold":  (9, (Decimal("1"), Decimal("2.5"), Decimal("7"))),
    "gem":   (14, (Decimal("0.6"), Decimal("1.5"), Decimal("4"))),
    "low":   (22, (Decimal("0.4"), Decimal("0.8"), Decimal("2"))),
}
NAMES = list(SYMBOLS)
WEIGHTS = [SYMBOLS[n][0] for n in NAMES]
RTP_TARGET = Decimal("0.96")


def spin(server_seed: str, client_seed: str, nonce: int) -> list[list[str]]:
    grid = []
    for r in range(ROWS):
        grid.append([NAMES[rand_int(server_seed, client_seed, nonce * 100 + r * 10 + c,
                                    0, len(NAMES), "slot")] for c in range(REELS)])
    return grid


def evaluate(grid: list[list[str]], stake: Decimal) -> tuple[Decimal, int]:
    total = Decimal("0.00")
    hits = 0
    for line in PAYLINES:
        seq = [grid[row][col] for col, row in enumerate(line)]
        base = next((s for s in seq if s != "wild"), seq[0])
        run = 0
        for s in seq:
            if s in (base, "wild"):
                run += 1
            else:
                break
        if run >= 3:
            total += SYMBOLS[base][1][run - 3] * stake
            hits += 1
    return total.quantize(Decimal("0.01")), hits
