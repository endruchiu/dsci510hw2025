
CREATE TABLE artists (
    artist_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    genre TEXT NOT NULL
);

CREATE TABLE stages (
    stage_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE performances (
    performance_id INTEGER PRIMARY KEY,
    artist_id INTEGER,
    stage_id INTEGER,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    FOREIGN KEY (stage_id) REFERENCES stages(stage_id)
);

CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    purchaser_name TEXT NOT NULL,
    purchase_date DATE NOT NULL,
    price REAL NOT NULL
);
