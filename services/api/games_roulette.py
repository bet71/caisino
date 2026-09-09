"""Roleta europeia: 37 casas, zero simples. RTP fixo = 35/37 = 94.59%."""
from __future__ import annotations
from decimal import Decimal
from rng import rand_int

EUROPEAN = [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26]
RED = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
PAYOUT = {"straight": 35, "split": 17, "street": 11, "corner": 8, "line": 5,
          "dozen": 2, "column": 2, "red": 1, "black": 1, "even": 1, "odd": 1, "low": 1, "high": 1}


def land(server_seed, client_seed, nonce) -> int:
    return EUROPEAN[rand_int(server_seed, client_seed, nonce, 0, len(EUROPEAN), "roulette")]


def settle(bet_type: str, stake: Decimal, chosen, result: int) -> Decimal:
    won = False
    if bet_type == "straight": won = result == chosen
    elif bet_type == "red":    won = result in RED
    elif bet_type == "black":  won = result in RED is False and result != 0
    elif bet_type == "even":   won = result != 0 and result % 2 == 0
    elif bet_type == "odd":    won = result % 2 == 1
    elif bet_type == "low":    won = 1 <= result <= 18
    elif bet_type == "high":   won = 19 <= result <= 36
    elif bet_type == "dozen":  won = (chosen - 1) * 12 <= result <= chosen * 12 and result != 0
    return (stake * (PAYOUT[bet_type] + 1)).quantize(Decimal("0.01")) if won else Decimal("0.00")
