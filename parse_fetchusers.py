# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 18:54:42 2017

"""

import pandas as pd
import sys
import re

columns = ['username', 'discriminator', 'user_id']
pattern_user = re.compile(r"'username': '(.+)', 'discrim")
pattern_discrim = re.compile(r"'discriminator': '(\d+)',")
pattern_id = re.compile(r"'id': '(\d+)',")

def parse_user(text):
    m = pattern_user.search(text)
    if m is None:
        return
    else:
        return m.group(1)
    
def parse_discrim(text):
    m = pattern_discrim.search(text)
    if m is None:
        return
    else:
        return m.group(1)
    
def parse_id(text):
    m = pattern_id.search(text)
    if m is None:
        return
    else:
        return m.group(1)

def main():
    json_fp = sys.argv[1]
    with open(json_fp, 'r') as f:
        df = pd.read_json(f)
        df = df.T.reset_index()
        df['user_str'] = df['user'].astype('str')
        df['username'] = df['user_str'].apply(parse_user)
        df['discriminator'] = df['user_str'].apply(parse_discrim).astype('int64')
        df['user_id'] = df['user_str'].apply(parse_id)
        df = df[columns]
        df2 = pd.read_csv('data.csv', encoding = "utf-8")
        df3 = df2.merge(df, on=['username','discriminator'])
        print(df.username.dtype)
        print(df2.username.dtype)
        df3.to_csv('join.csv', index=False, encoding='utf-8')
        df4 = pd.read_csv('join.csv', encoding='utf-8')
        assert(df3.equals(df4))

if __name__ == '__main__':
    main()