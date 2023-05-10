DROP TABLE IF EXISTS hosts;
DROP TABLE IF EXISTS joins;
DROP TABLE IF EXISTS lobby;
DROP TABLE IF EXISTS player;

CREATE TABLE lobby (
    roomcode VARCHAR(4) NOT NULL PRIMARY KEY,
    roomsize INTEGER NOT NULL
);

CREATE TABLE player (
    username VARCHAR(15) NOT NULL PRIMARY KEY
);

CREATE TABLE hosts (
    username VARCHAR(15) NOT NULL,
    roomcode VARCHAR(4) NOT NULL,
    FOREIGN KEY (username) REFERENCES player (username) ON DELETE CASCADE,
    FOREIGN KEY (roomcode) REFERENCES lobby (roomcode) ON DELETE CASCADE
);

CREATE TABLE joins (
    username VARCHAR(15) NOT NULL,
    roomcode VARCHAR(4) NOT NULL,
    FOREIGN KEY (username) REFERENCES player (username) ON DELETE CASCADE,
    FOREIGN KEY (roomcode) REFERENCES lobby (roomcode) ON DELETE CASCADE
);
