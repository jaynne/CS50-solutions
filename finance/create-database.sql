CREATE TABLE users (
	id INTEGER,
	username TEXT NOT NULL,
	hash TEXT NOT NULL, 
	cash NUMERIC NOT NULL DEFAULT 10000.00,
	PRIMARY KEY(id));
CREATE UNIQUE INDEX username ON users (username);


CREATE TABLE user_stock (
	user_id INTEGER NOT NULL,
	stock TEXT NOT NULL,
	quantity NUMERIC,
	FOREIGN KEY(user_id) REFERENCES users(id)
);


CREATE TABLE user_history(
	user_id INTEGER NOT NULL,
	stock TEXT NOT NULL,
	shares NUMERIC, 
	price REAL,
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	FOREIGN KEY(user_id) REFERENCES users(id)
);
