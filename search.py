#!/usr/bin/python3

import psycopg2
import re
import string
import sys

_PUNCTUATION = frozenset(string.punctuation)


def _remove_punc(token):
    """Removes punctuation from start/end of token."""
    i = 0
    j = len(token) - 1
    idone = False
    jdone = False
    while i <= j and not (idone and jdone):
        if token[i] in _PUNCTUATION and not idone:
            i += 1
        else:
            idone = True
        if token[j] in _PUNCTUATION and not jdone:
            j -= 1
        else:
            jdone = True
    return "" if i > j else token[i:(j+1)]

def _get_tokens(query):
    rewritten_query = []
    tokens = re.split('[ \n\r]+', query)
    for token in tokens:
        cleaned_token = _remove_punc(token)
        if cleaned_token:
            if "'" in cleaned_token:
                cleaned_token = cleaned_token.replace("'", "''")
            rewritten_query.append(cleaned_token)
    return rewritten_query



def search(query, query_type, pagenum):
    
    rewritten_query = _get_tokens(query)
    count = 0
    if len(rewritten_query) == 0:
        return [], 0
    tuple_list = [rewritten_query[0].lower()]
    sql_query = 'CREATE MATERIALIZED VIEW searchResults AS SELECT song_name, a.score, page_link, art.artist_name FROM (SELECT  song_id, COUNT(song_id) as count, SUM(score) as score FROM tfidf WHERE token = %s'

    for i in range(1, len(rewritten_query)):
        tuple_list.append(rewritten_query[i].lower())
        sql_query += ' OR token = %s'

    sql_query += ' GROUP BY song_id'
    and_string = ') a JOIN Song s ON s.song_id = a.song_id JOIN artist art ON s.artist_id = art.artist_id WHERE count = %s ORDER BY score DESC;'
    or_string = ') a JOIN Song s ON s.song_id = a.song_id JOIN artist art ON s.artist_id = art.artist_id WHERE count >= %s ORDER BY score DESC;'
    
    if query_type == "and":
        sql_query += and_string
        tuple_list.append(len(rewritten_query))
    elif query_type == "or" :
        sql_query += or_string
        tuple_list.append(1)
    else:
        return [], 0

#print(sql_query)

    conn = None
    all_songs = []
    try:
        print('Connecting to the searchengine database...')
        conn = psycopg2.connect(host="localhost", database="searchengine", user="cs143", password="cs143", port="5432") 
        cur = conn.cursor()

        # execute a statement
        psql_select = "SELECT * FROM searchResults LIMIT 20 OFFSET %s;"
        offset = pagenum * 20
        select_tup = tuple([offset])
        current_size = 0
        if pagenum == 0:
            psql_drop = "DROP MATERIALIZED VIEW IF EXISTS searchResults;"
            cur.execute(psql_drop)
            conn.commit()
            print(tuple(tuple_list))
            cur.execute(sql_query, tuple(tuple_list))
            conn.commit()
        
        sizeQuery = "SELECT COUNT(*) FROM searchResults;"
        cur.execute(sizeQuery)
        current_size = cur.fetchall()[0][0]
        print(current_size, file = sys.stderr)

        cur.execute(psql_select, select_tup)
            # display the PostgreSQL database server version
        all_songs = cur.fetchall()


     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return all_songs, current_size

if __name__ == "__main__":
    if len(sys.argv) > 2:
        result = search(' '.join(sys.argv[2:]), sys.argv[1].lower())
        print(result)
    else:
        print("USAGE: python3 search.py [or|and] term1 term2 ...")

