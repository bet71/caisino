"""API FastAPI: auth, wallet, rodadas, jogos, admin."""
from __future__ import annotations
from decimal import Decimal
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

import rng, wallet, games_crash, games_slots, games_roulette, games_mines, bonus, risk

app = FastAPI(title="casino", version="0.1.0")


class Bet(BaseModel):
    game: str
    stake: Decimal
    client_seed: str = "anon"
    nonce: int = 1
    choice: str | int | None = None
    reveal: int = 0


@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/round/commit")
async def commit_round():
    seed = rng.new_server_seed()
    return {"server_seed_hash": rng.commit(seed)}


@app.post("/play")
async def play(b: Bet):
    bad = risk.check_bet(b.stake, Decimal("100000"))
    if bad:
        raise HTTPException(400, bad)
    seed = rng.new_server_seed()
    if b.game == "crash":
        c = games_crash.crash_point(seed, b.client_seed, b.nonce)
        out = {"crash": str(c)}
    elif b.game == "slots":
        g = games_slots.spin(seed, b.client_seed, b.nonce)
        pay, hits = games_slots.evaluate(g, b.stake)
        out = {"grid": g, "payout": str(pay), "lines": hits}
    elif b.game == "roulette":
        r = games_roulette.land(seed, b.client_seed, b.nonce)
        out = {"result": r, "payout": str(games_roulette.settle(str(b.choice), b.stake, 1, r))}
    elif b.game == "mines":
        m = games_mines.mines(seed, b.client_seed, b.nonce, int(b.choice or 3))
        out = {"mines": sorted(m), "payout": str(games_mines.cashout(b.stake, b.reveal, int(b.choice or 3)))}
    else:
        raise HTTPException(400, "jogo_desconhecido")
    out["server_seed"] = seed
    out["server_seed_hash"] = rng.commit(seed)
    return out


@app.get("/admin/metrics")
async def metrics(x_admin_token: str = Header(...)):
    return {"status": "placeholder", "ggr": "0", "ngr": "0", "active_users": 0}
