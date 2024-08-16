CREATE TABLE users(
  id SERIAL PRIMARY KEY, 
  first_name TEXT NOT NULL, 
  last_name TEXT NOT NULL,
  username TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  disabled BOOLEAN NOT NULL,
  administrator BOOLEAN NOT NULL
);

CREATE TABLE resources(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  "path" TEXT NOT NULL,
  "size" INTEGER NOT NULL
);
