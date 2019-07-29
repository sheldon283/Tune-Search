\c searchengine 

-- DROP SCHEMA IF EXISTS tunesearch CASCADE;
-- CREATE SCHEMA tunesearch;

CREATE TABLE IF NOT EXISTS artist (
	artist_id INTEGER PRIMARY KEY,
	artist_name VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS token (
	song_id INTEGER,
	token VARCHAR(255),
	count INTEGER,
	PRIMARY KEY (song_id, token)
);

CREATE TABLE IF NOT EXISTS song (
	song_id INTEGER PRIMARY KEY,
	artist_id INTEGER REFERENCES artist(artist_id),
	song_name VARCHAR(255),
	page_link VARCHAR(1000)
	/* , FOREIGN KEY (artist_id) REFERENCES artist (artist_id) */
);

CREATE TABLE IF NOT EXISTS tfidf (
	song_id INTEGER,
	token VARCHAR(255),
	score FLOAT,
	PRIMARY KEY(song_id, token)
);