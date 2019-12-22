#!/usr/bin/env python3

# aids manually identifying sticons...

import csv
import os

dload_dir = '_sticon'
keywords_file = 'sticon_keywords.tsv'

with open(keywords_file) as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for keyword, path in reader:
        folder = os.path.dirname(path)
        path = path.replace('.png', '')
        sticker_pack = folder.replace('_sticon/', '')
        if os.path.exists(path + '.png'):
            os.rename(path, path + '_' + keyword + '.png')
