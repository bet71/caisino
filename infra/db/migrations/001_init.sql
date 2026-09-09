-- Ledger imutavel: nunca UPDATE em saldo. Saldo = SUM(amount).
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL, currency CHAR(3) NOT NULL DEFAULT 'BRL',
  kyc_status TEXT NOT NULL DEFAULT 'none', status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE sessions (
  id BIGSERIAL PRIMARY KEY, user_id BIGINT NOT NULL REFERENCES users(id),
  token_hash TEXT NOT NULL, expires_at TIMESTAMPTZ NOT NULL, ip INET
);
CREATE TABLE wallet_accounts (
  id BIGSERIAL PRIMARY KEY, user_id BIGINT NOT NULL REFERENCES users(id),
  currency CHAR(3) NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (user_id, currency)
);
CREATE TABLE ledger (
  id BIGSERIAL PRIMARY KEY, account_id BIGINT NOT NULL REFERENCES wallet_accounts(id),
  amount NUMERIC(20,4) NOT NULL, currency CHAR(3) NOT NULL,
  kind TEXT NOT NULL CHECK (kind IN ('deposit','withdraw','bet','win','bonus','rakeback','reversal','adjust')),
  ref_type TEXT, ref_id TEXT, idempotency_key TEXT UNIQUE,
  balance_after NUMERIC(20,4) NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ON ledger (account_id, created_at DESC);

CREATE TABLE rounds (
  id BIGSERIAL PRIMARY KEY, game TEXT NOT NULL, server_seed_hash TEXT NOT NULL,
  server_seed TEXT, client_seed TEXT, nonce BIGINT, outcome JSONB NOT NULL,
  rtp_sample BOOLEAN NOT NULL DEFAULT true, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE bets (
  id BIGSERIAL PRIMARY KEY, user_id BIGINT NOT NULL REFERENCES users(id),
  game TEXT NOT NULL, round_id BIGINT REFERENCES rounds(id),
  stake NUMERIC(20,4) NOT NULL, payout NUMERIC(20,4) NOT NULL DEFAULT 0,
  status TEXT NOT NULL CHECK (status IN ('reserved','settled','voided')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(), settled_at TIMESTAMPTZ
);
CREATE TABLE withdrawals (
  id BIGSERIAL PRIMARY KEY, user_id BIGINT NOT NULL REFERENCES users(id),
  amount NUMERIC(20,4) NOT NULL, currency CHAR(3) NOT NULL, method TEXT NOT NULL,
  destination TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'pending_review',
  reviewed_by BIGINT, reviewed_at TIMESTAMPTZ, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE bonus_state (
  user_id BIGINT PRIMARY KEY REFERENCES users(id), bonus_balance NUMERIC(20,4) NOT NULL DEFAULT 0,
  wager_required NUMERIC(20,4) NOT NULL DEFAULT 0, wagered NUMERIC(20,4) NOT NULL DEFAULT 0,
  expires_at TIMESTAMPTZ
);
CREATE TABLE risk_events (
  id BIGSERIAL PRIMARY KEY, user_id BIGINT, kind TEXT NOT NULL, payload JSONB, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Invariante: balance_after do ultimo lancamento tem de bater com SUM(amount).
CREATE OR REPLACE VIEW v_balance AS
  SELECT account_id, SUM(amount) AS computed_balance FROM ledger GROUP BY account_id;
