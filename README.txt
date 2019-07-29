Schema.sql - contains the schema definition, which is called project1. Under this schema there are 4 tables: artist, song, token, tfidf. 

load.sql - loads the csv files into 3 tables: artist, song, token. The name of the csv file pertains to the table its loaded in

We assumed every variable can't be null in this database, so we set all variables to not null. I also made the default for TDIDF_SCORE and frequency 0. 
