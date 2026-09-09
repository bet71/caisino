"""Risk: limites e sinais de abuso. Nada aqui bloqueia sozinho, so marca."""
from __future__ import annotations
from decimal import Decimal

MAX_BET = Decimal("5000")
RAPID_BET_MS = 400
DAILY_LOSS_ALERT = Decimal("2000")


def check_bet(stake: Decimal, balance: Decimal, user_limit: Decimal = MAX_BET) -> str | None:
    if stake <= 0:            return "stake_invalida"
    if stake > user_limit:    return "acima_do_limite"
    if stake > balance:       return "saldo_insuficiente"
    return None


def signals(bets_last_hour: int, avg_interval_ms: int, deposit_to_bet_ratio: Decimal) -> list[str]:
    s = []
    if bets_last_hour > 600:            s.append("volume_anormal")
    if avg_interval_ms < RAPID_BET_MS:  s.append("aposta_botonica")
    if deposit_to_bet_ratio > Decimal("50"): s.append("wash_deposito")
    return s
