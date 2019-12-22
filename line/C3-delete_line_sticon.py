#!/usr/bin/env python3

# aids manually identifying sticons...
# warning: overwrites sticons which have the same keyword within the same
# pack...

import csv
import os

dload_dir = '_sticon'
keywords_file = 'sticon_Merged_key.tsv'

preserve = []

with open(keywords_file) as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for row in reader:
        _, path = row
        filename = path.split('\\')[-1]
        preserve.append(filename)

    for filename in os.listdir(dload_dir):
        print(filename)
        if filename not in preserve and filename.endswith('.png'):
            os.remove(dload_dir + '/' + filename)
