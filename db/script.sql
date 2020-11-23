CREATE TABLE IF NOT EXISTS episodes (
    numb integer PRIMARY KEY,
    title text NOT NULL,
    descrip text NOT NULL
);
CREATE TABLE IF NOT EXISTS characters (
    id text PRIMARY KEY,
    descrip text NOT NULL,
    avatar_url text
);