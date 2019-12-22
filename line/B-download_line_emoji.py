#!/usr/bin/env python3

import urllib.request
import json

dload_dir = '_emoji'
emojis_url = 'http://dl.stickershop.line.naver.jp/products/0/0/100/5/android/productInfo.meta'

with urllib.request.urlopen(emojis_url) as url:
    data = json.loads(url.read().decode())

    for emoji in data['stickers']:
        STKID = str(emoji['id'])

        # download sticker as STKVER_STKPKGID_STKID.png
        urllib.request.urlretrieve('http://dl.stickershop.line.naver.jp/products/0/0/100/5/WindowsPhone/stickers/' + STKID + '.png',
                dload_dir + '/100_5_' + STKID + '.png')
        #urllib.request.urlretrieve('http://dl.stickershop.line.naver.jp/products/0/0/100/5/WindowsPhone/stickers/' + STKID + '_key.png',
        #        dload_dir + '/100_5_' + STKID + '_key.png')
