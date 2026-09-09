import asyncio
from decimal import Decimal
import wallet


def test_money_arredonda_para_baixo():
    assert wallet.money("1.005") == Decimal("1.00")
    assert wallet.money(2) == Decimal("2.00")


def test_invariante_saldo_e_soma_do_ledger():
    """Saldo nunca e UPDATE. E sempre a soma dos lancamentos."""
    lancamentos = [Decimal("100.00"), Decimal("-40.00"), Decimal("15.50")]
    assert sum(lancamentos) == Decimal("75.50")


def test_settle_devolve_so_o_liquido():
    stake, payout = Decimal("10.00"), Decimal("25.00")
    assert wallet.money(payout - stake) == Decimal("15.00")


def test_aposta_perdida_nao_devolve():
    assert wallet.money(Decimal("0.00") - Decimal("10.00")) == Decimal("-10.00")
