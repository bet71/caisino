import rng


def test_commit_reveal():
    s = rng.new_server_seed()
    assert rng.verify_commit(s, rng.commit(s))
    assert not rng.verify_commit("outra", rng.commit(s))


def test_deterministico():
    a = rng.rand_float("seed", "client", 7, "crash")
    b = rng.rand_float("seed", "client", 7, "crash")
    assert a == b
    assert 0.0 <= a < 1.0


def test_uniforme():
    vals = [rng.rand_int("s", "c", i, 0, 37, "r") for i in range(37000)]
    assert min(vals) >= 0 and max(vals) < 37
    hist = {v: vals.count(v) for v in set(vals)}
    assert min(hist.values()) > 37000 / 37 * 0.7
