\c searchengine 

\copy artist FROM '/home/cs143/data/artist.csv' DELIMITER ',' QUOTE '"' CSV;
\copy song   FROM '/home/cs143/data/song.csv'   DELIMITER ',' QUOTE '"' CSV;
\copy token  FROM '/home/cs143/data/token.csv'  DELIMITER ',' QUOTE '"' CSV;

DROP TABLE IF EXISTS IDF_COUNT;

CREATE TABLE IF NOT EXISTS IDF_COUNT (
	token VARCHAR(255),
	idf_score int
);

INSERT INTO IDF_COUNT
SELECT DISTINCT
	token,
	COUNT(token) as idf_score
FROM token
GROUP BY token;

INSERT INTO tfidf
SELECT 
	song_id,
	token.token as token ,
	count * LOG ((SELECT COUNT(*) FROM SONG)/CAST(IDF_COUNT.idf_score as float)) as score
FROM token JOIN IDF_COUNT ON token.token = IDF_COUNT.token
ORDER BY score desc;

DROP TABLE IDF_COUNT;
