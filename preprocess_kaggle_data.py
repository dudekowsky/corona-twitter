# Quick and dirty preprocessing of the tweet dfs: remove unrecognized languages, newline characters and hyperlinks

import pandas as pd
import os
from tqdm import tqdm

path = 'data/raw'
files = os.listdir(path)
tweets = sorted([i for i in files if 'Coronavirus Tweets' in i])
allowed_langs = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ar', 'hi', 'ja', 'ko', 'zh', 'zh-TW']
total_removed = 0
for file in tqdm(tweets):
    df = pd.read_csv(os.path.join(path, file))
    l = len(df)
    # remove all tweets in languages that aws can't recognize
    df = df[df.lang.isin(allowed_langs)]
    total_removed += l - len(df)
    # remove newline characters
    df.text = df.text.apply(lambda x: x.replace('\n', ' '))
    df.text = df.text.apply(lambda x: x.replace('\r', ' '))
    df.text = df.text.apply(lambda x: x.replace('\t', ' '))
    df.text = df.text.apply(lambda x: x.replace('  ', ' '))
    # move hyperlinks into separate column
    df.text = df.text.apply(lambda x: x.split(' '))
    df['hyperlink'] = df.text.apply(lambda x: (', ').join([i for i in x if i.startswith('https://')]))
    # make separate hashtags column but keep them in the text (won't catch hashtags that aren't preceeded by spaces)
    df['hashtag'] = df.text.apply(lambda x: (', ').join([i for i in x if i.startswith('#')]))
    # make separate mentions column bu tkeep them in the text (won't catch at-mentions whtat aren't preceeded by spaces)
    df['mention'] = df.text.apply(lambda x: (', ').join([i for i in x if i.startswith('@')]))
    df.text = df.text.apply(lambda x: (' ').join([i for i in x if not i.startswith('https://')]))
    date = file.split(' ')[0]
    df.to_csv(os.path.join('data/preprocessed', date + '.csv'))
    
print('Preprocessed {} files. Removed {} tweets due to language constraints.'.format(len(tweets), total_removed))