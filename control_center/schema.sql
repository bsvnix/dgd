-- Table for storing scan results
CREATE TABLE IF NOT EXISTS scan_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT NOT NULL,
    open_ports TEXT NOT NULL
);

-- Table for storing decoy events
CREATE TABLE IF NOT EXISTS decoy_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decoy_name TEXT NOT NULL,
    port INTEGER NOT NULL,
    attacker_ip TEXT NOT NULL
);
