import psycopg2
import unicodedata

host = 'host=iServDB.cloudopenlab.org.tw port=5432'
dbname = 'dbname=stanley811213_db_7744'
login_info = 'user=stanley811213_user_7744 password=OUvWLGmm'

def char_width(char):
    width = unicodedata.east_asian_width(unicode(char))
    if width == 'Na':
        return 1
    else:
        return 2

def partition(string, n):
    if string == '':
        return []

    width = 0
    for i, c in enumerate(string):
        width += char_width(c)
        if width > n:
            break
    if width <= n:
        i += 1
    else:
        width -= char_width(c)

    return [string[:i] + ' ' * (n - width)] + partition(string[i:], n)

def print_row(data):
    text = partition(data[1], 30)
    author = partition(data[2], 20)
    twitter_id = partition(data[3], 15)

    print('+' + '-' * 30 + '+' + '-' * 20 + '+' + '-' * 15 + '+')
    lines = max(len(text), len(author), len(twitter_id))
    for i in range(lines):
        _text = text[i] if len(text) > i else ' ' * 30
        _author = author[i] if len(author) > i else ' ' * 20
        _twitter_id = twitter_id[i] if len(twitter_id) > i else ' ' * 15
        print '|' + _text + '|' + _author + '|' + _twitter_id + '|'
    
conn = psycopg2.connect(host + ' ' + dbname + ' ' + login_info)
cur = conn.cursor()

query = raw_input('Input: ')
cur.execute("SELECT * FROM twitter WHERE q='" + query + "';")
result = cur.fetchall()

final_result = sorted(result, key=lambda x: int(x[3]))
print final_result[0]
for i in final_result:
    print_row(i)

cur.close()
conn.close()
