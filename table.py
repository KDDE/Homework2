import unicodedata
import re

COL_WIDTH = [40, 20, 15]

def pad_string(string, width):
    n = string_width(string)
    padding = 0 if n >= width else width - n
    return string + ' ' * padding

def char_width(char):
    width = unicodedata.east_asian_width(char)
    if width in ['Na', 'A', 'N']:
        return 1
    else:
        return 2

def string_width(string):
    width = 0
    for char in string:
        width += char_width(char)
    return width

def partition(string, n):
    if string == '':
        return []

    width = 0
    for i, c in enumerate(string):
        width += char_width(c)
        if width > n or c == '\n':
            break
    if width <= n:
        i += 1
    return [string[:i]] + partition(string[i:], n)

def print_line():
    for width in COL_WIDTH:
        print '+' + '-' * width,
    print '+'

def print_row(tweet_data):
    tweet_data = [x.decode('utf8') for x in tweet_data]
    for i in range(len(tweet_data)):
        tweet_data[i] = partition(tweet_data[i], COL_WIDTH[i])

    print_line()
    lines = len(max(tweet_data, key=lambda x: len(x)))
    for i in range(lines):
        for n, col in enumerate(tweet_data):
            s = col[i] if len(col) > i else ''
            print '|' + pad_string(s.replace('\n', ''), COL_WIDTH[n]),
        print '|'

def print_header():
    print_line()
    print '|text' + ' ' * (COL_WIDTH[0] - len('text')),
    print '|user_name' + ' ' * (COL_WIDTH[1] - len('user_name')),
    print '|user_id' + ' ' * (COL_WIDTH[2] - len('user_id')),
    print '|'

def print_table(data):
    print_header()
    for i in data:
        print_row(i)
    print_line()
