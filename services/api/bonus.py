"""Bonus e rollover. Bonus nunca e dinheiro ate bater o requisito de giro."""
from __future__ import annotations
from decimal import Decimal


def grant(amount: Decimal, multiplier: Decimal = Decimal("30")) -> tuple[Decimal, Decimal]:
    bonus = amount.quantize(Decimal("0.01"))
    return bonus, (bonus * multiplier).quantize(Decimal("0.01"))


def progress(wagered: Decimal, wager_required: Decimal) -> Decimal:
    if wager_required == 0:
        return Decimal("1.00")
    return min(Decimal("1.00"), (wagered / wager_required).quantize(Decimal("0.0001")))


def release(bonus_balance: Decimal, wagered: Decimal, wager_required: Decimal) -> Decimal:
    """Quanto do bonus vira saldo real nesta aposta. Liberacao proporcional ao giro."""
    if wager_required <= 0 or wagered >= wager_required:
        return bonus_balance
    frac = (wagered / wager_required).quantize(Decimal("0.0001"))
    return (bonus_balance * frac).quantize(Decimal("0.01"))
