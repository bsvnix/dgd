# Create the tables (same schema as in control_center/schema.sql)
CREATE TABLE scan_results (
  id SERIAL PRIMARY KEY,
  ip TEXT NOT NULL,
  open_ports TEXT
);

CREATE TABLE decoy_events (
  id SERIAL PRIMARY KEY,
  decoy_name TEXT NOT NULL,
  port INTEGER NOT NULL,
  attacker_ip TEXT NOT NULL
);
