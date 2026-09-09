"""RTP verificado por simulacao. Falha se o jogo sair da faixa alvo."""
from decimal import Decimal
import rng, games_crash, games_slots, games_roulette

N = 200_000


def simulate(fn, stake=Decimal("1")):
    total_in = total_out = Decimal("0")
    for i in range(N):
        out = fn(i, stake)
        total_in += stake
        total_out += out
    return total_out / total_in


def test_crash_rtp():
    def f(i, stake):
        c = games_crash.crash_point("s", "c", i)
        return games_crash.cashout_payout(stake, Decimal("2.00"), c)
    rtp = simulate(f)
    assert Decimal("0.90") <= rtp <= Decimal("1.02"), f"RTP crash fora da faixa: {rtp}"


def test_slots_rtp():
    def f(i, stake):
        g = games_slots.spin("s", "c", i)
        return games_slots.evaluate(g, stake)[0]
    rtp = simulate(f)
    assert Decimal("0.85") <= rtp <= Decimal("1.10"), f"RTP slots fora da faixa: {rtp}"


def test_roulette_rtp():
    def f(i, stake):
        r = games_roulette.land("s", "c", i)
        return games_roulette.settle("red", stake, None, r)
    rtp = simulate(f)
    assert Decimal("0.90") <= rtp <= Decimal("0.99"), f"RTP roleta fora da faixa: {rtp}"
