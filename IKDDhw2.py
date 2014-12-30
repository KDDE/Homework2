import psycopg2
import unicodedata

import table

host = 'host=iServDB.cloudopenlab.org.tw port=5432'
dbname = 'dbname=stanley811213_db_7744'
login_info = 'user=stanley811213_user_7744 password=OUvWLGmm'

conn = psycopg2.connect(host + ' ' + dbname + ' ' + login_info)
cur = conn.cursor()

query = raw_input('Input: ')
cur.execute("SELECT text, user_name, user_id  FROM twitter WHERE q='" + query + "';")
result = cur.fetchall()

final_result = sorted(result, key=lambda x: int(x[2]))

table.print_table(final_result)

cur.close()
conn.close()
