#!/usr/bin/env python3

import urllib.request
import zipfile
import json
import os

dload_dir = '_sticon'
keywords_outfile = 'sticon_keywords.tsv'
sticon_ids = [
    "5ac1bfd5040ab15980c9b435",
    "5ac1de17040ab15980c9b438",
    "5ac21184040ab15980c9b43a",
    "5ac21542031a6752fb806d55",
    "5ac2173d031a6752fb806d56",
    "5ac21869040ab15980c9b43b",
    "5ac218e3040ab15980c9b43c",
    "5ac2197b040ab15980c9b43d",
    "5ac21a13031a6752fb806d57",
    "5ac21a18040ab15980c9b43e",
    "5ac21a8c040ab15980c9b43f",
    "5ac21ae3040ab15980c9b440",
    "5ac21b4f031a6752fb806d59",
    "5ac21c46040ab15980c9b442",
    "5ac21cc5031a6752fb806d5c",
    "5ac21d59031a6752fb806d5d",
    "5ac21e6c040ab15980c9b444",
    "5ac21ef5031a6752fb806d5e",
    "5ac21f52040ab15980c9b445",
    "5ac2206d031a6752fb806d5f",
    "5ac2211e031a6752fb806d61",
    "5ac2216f040ab15980c9b448",
    "5ac223c6040ab15980c9b44a",
    "5ac2264e040ab15980c9b44b",
    "5ac22bad031a6752fb806d67",
    "5ac22d62031a6752fb806d69",
    "5ac22e85040ab15980c9b44f"
    ]

os.remove(keywords_outfile)

for sticon in sticon_ids:
    urllib.request.urlretrieve('http://dl.stickershop.line.naver.jp/sticonshop/v1/' + sticon + '/sticon/iphone/package.zip',
            dload_dir + '/' + sticon + '.zip')

    with zipfile.ZipFile(dload_dir + '/' + sticon + '.zip', 'r') as z:
        z.extractall(dload_dir + '/' + sticon)

    with open(dload_dir + '/' + sticon + '/meta.json', 'r') as f:
        data = json.load(f)

    with open(keywords_outfile, 'a') as out:
        for icon_num in data['altTexts']:
            text = data['altTexts'][icon_num] + '\t' + dload_dir + '/' + sticon + '/' + icon_num + '.png'
            print(text)
            out.write(text + '\n')
