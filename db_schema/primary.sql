DROP TABLE IF EXISTS hosts;
DROP TABLE IF EXISTS joins;
DROP TABLE IF EXISTS lobby;
DROP TABLE IF EXISTS player;

CREATE TABLE lobby (
    roomcode VARCHAR(4) PRIMARY KEY
);

CREATE TABLE player (
    username VARCHAR(15) PRIMARY KEY
);

CREATE TABLE hosts (
    username VARCHAR(15),
    roomcode VARCHAR(4),
    FOREIGN KEY (username) REFERENCES player (username),
    FOREIGN KEY (roomcode) REFERENCES lobby (roomcode)
);

CREATE TABLE joins (
    username VARCHAR(15),
    roomcode VARCHAR(4),
    FOREIGN KEY (username) REFERENCES player (username),
    FOREIGN KEY (roomcode) REFERENCES lobby (roomcode)
);
