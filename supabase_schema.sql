-- Run this in your Supabase SQL Editor to set up the database.
-- Go to: https://supabase.com → Your Project → SQL Editor → New Query → Paste & Run

CREATE TABLE IF NOT EXISTS waste_logs (
  id          BIGSERIAL PRIMARY KEY,
  category    TEXT        NOT NULL,
  weight_kg   NUMERIC     NOT NULL CHECK (weight_kg > 0),
  latitude    DOUBLE PRECISION NOT NULL,
  longitude   DOUBLE PRECISION NOT NULL,
  notes       TEXT        DEFAULT '',
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security but allow public reads/inserts (for this MVP)
ALTER TABLE waste_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read"
  ON waste_logs FOR SELECT USING (true);

CREATE POLICY "Allow public insert"
  ON waste_logs FOR INSERT WITH CHECK (true);
