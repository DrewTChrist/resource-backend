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

CREATE TABLE favorites(
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  resource_id INT NOT NULL,
  CONSTRAINT fk_user
    FOREIGN KEY(user_id)
      REFERENCES users(id)
      ON DELETE CASCADE,
  CONSTRAINT fk_resource
    FOREIGN KEY(resource_id)
      REFERENCES resources(id)
      ON DELETE CASCADE
);

CREATE TABLE metadata_types(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE metadata(
  id SERIAL PRIMARY KEY,
  value TEXT NOT NULL,
  metadata_type_id INT NOT NULL,
  resource_id INT NOT NULL,
  CONSTRAINT fk_metadata_type
    FOREIGN KEY(metadata_type_id)
      REFERENCES metadata_types(id)
      ON DELETE CASCADE,
  CONSTRAINT fk_resource
    FOREIGN KEY(resource_id)
      REFERENCES resources(id)
      ON DELETE CASCADE
);
