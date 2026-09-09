"""Worker: liquidacao de saques pendentes, expiracao de bonus, amostragem de RTP."""
from __future__ import annotations
import asyncio, time

POLL_SECONDS = 5


async def expire_bonuses():
    """Bonus vencido volta para a casa como lancamento de reversal."""
    ...


async def settle_withdrawals():
    """Saques aprovados no backoffice viram lancamento no ledger."""
    ...


async def rtp_sampling():
    """Marca rodadas para auditoria de RTP e grava desvio por jogo."""
    ...


async def loop():
    while True:
        t0 = time.time()
        await expire_bonuses()
        await settle_withdrawals()
        await rtp_sampling()
        await asyncio.sleep(max(0.0, POLL_SECONDS - (time.time() - t0)))


if __name__ == "__main__":
    asyncio.run(loop())
