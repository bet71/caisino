"""Wallet com ledger imutavel. Saldo nunca e UPDATE: e sempre SUM(lancamentos).

Regras:
- Todo lancamento grava balance_after e e imutavel.
- idempotency_key impede deposito/saque duplicado em retry de rede.
- Aposta passa por reserve -> settle -> release; nunca duas apostas no mesmo saldo.
"""
from __future__ import annotations
from decimal import Decimal, ROUND_DOWN

TWO = Decimal("0.01")


def money(x) -> Decimal:
    return Decimal(str(x)).quantize(TWO, rounding=ROUND_DOWN)


async def balance(conn, account_id: int) -> Decimal:
    row = await conn.fetchval(
        "SELECT COALESCE(SUM(amount),0) FROM ledger WHERE account_id=$1", account_id)
    return money(row)


async def post(conn, account_id: int, amount: Decimal, kind: str, currency: str,
               idempotency_key: str | None = None, ref_type: str = "", ref_id: str = "") -> int:
    """Registra um lancamento. Idempotente: a mesma chave nao entra duas vezes."""
    if idempotency_key:
        exists = await conn.fetchval(
            "SELECT id FROM ledger WHERE idempotency_key=$1", idempotency_key)
        if exists:
            return exists
    async with conn.transaction():
        cur = money(await conn.fetchval(
            "SELECT COALESCE(SUM(amount),0) FROM ledger WHERE account_id=$1 FOR UPDATE",
            account_id))
        new = cur + money(amount)
        if new < 0:
            raise InsufficientFunds(account_id, cur, amount)
        return await conn.fetchval(
            """INSERT INTO ledger (account_id, amount, currency, kind, ref_type, ref_id,
                                   idempotency_key, balance_after)
               VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id""",
            account_id, money(amount), currency, kind, ref_type, ref_id,
            idempotency_key, new)


class InsufficientFunds(Exception):
    def __init__(self, account_id, have, wanted):
        super().__init__(f"conta {account_id}: saldo {have}, tentou debitar {wanted}")


async def reserve_bet(conn, account_id: int, stake: Decimal, bet_id: int, currency: str) -> int:
    return await post(conn, account_id, -money(stake), "bet", currency,
                      idempotency_key=f"bet:{bet_id}", ref_type="bet", ref_id=str(bet_id))


async def settle_bet(conn, account_id: int, stake: Decimal, payout: Decimal,
                     bet_id: int, currency: str) -> int:
    """Devolve o que nao virou perda e credita o premio liquido."""
    delta = money(payout) - money(stake)
    if delta == 0:
        return 0
    return await post(conn, account_id, delta, "win", currency,
                      idempotency_key=f"settle:{bet_id}", ref_type="bet", ref_id=str(bet_id))
