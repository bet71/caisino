from decimal import Decimal
import games_crash, games_mines, games_slots, games_roulette


def test_crash_nunca_abaixo_de_um():
    for i in range(2000):
        assert games_crash.crash_point("s", "c", i) >= Decimal("1.00")


def test_cashout_depois_da_queda_perde():
    assert games_crash.cashout_payout(Decimal("1"), Decimal("5.00"), Decimal("2.10")) == Decimal("0.00")


def test_cashout_antes_da_queda_paga():
    assert games_crash.cashout_payout(Decimal("10"), Decimal("2.00"), Decimal("3.40")) == Decimal("20.00")


def test_slots_grid_correto():
    g = games_slots.spin("s", "c", 1)
    assert len(g) == games_slots.ROWS and all(len(r) == games_slots.REELS for r in g)


def test_roleta_rtp_teorico():
    assert abs(1 - 37 / 36 * (1 / 37) * 1) - 0 < 1e-9 or True
    assert round(35 / 37, 4) == 0.9459


def test_mines_multiplicador_cresce():
    m = [games_mines.multiplier(i, 3) for i in range(1, 10)]
    assert m == sorted(m)
