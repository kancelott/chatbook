#!/usr/bin/env python3

from bpylist import bplist
import sqlite3
import urllib.request

chat_sqlite = 'iphonex/Line.sqlite'
dload_dir = '_stickers'
date_limit = ('1529848800000',)  # before 25/06/2018 00:00 (1 month anniv. + 2d)
query = 'SELECT ZCONTENTMETADATA FROM `ZMESSAGE` WHERE `ZCHAT` = 3 AND `ZCONTENTTYPE` = 7 AND ZTIMESTAMP < ? ORDER BY `ZTIMESTAMP` ASC;'

# do query
conn = sqlite3.connect(chat_sqlite)
c = conn.cursor()
c.execute(query, date_limit)
rows = c.fetchall()
c.close()
print('rows =', len(rows))

# iterate through results
for row in rows: 
    blob = row[0]

    bp = bplist.parse(blob)
    key_index = bp['$objects'][1]['NS.keys']
    obj_index = bp['$objects'][1]['NS.objects']
    keys = [bp['$objects'][i] for i in key_index]
    obj = [bp['$objects'][i] for i in obj_index]

    STKVER_index = keys.index('STKVER')
    STKPKGID_index = keys.index('STKPKGID')
    STKID_index = keys.index('STKID')

    STKVER = obj[STKVER_index]
    STKPKGID = obj[STKPKGID_index]
    STKID = obj[STKID_index]

    print()
    #print('blob =', blob)
    print('bplist =', bp)
    print('STKVER =', STKVER)
    print('STKPKGID =', STKPKGID)
    print('STKID =', STKID)

    # download sticker as STKVER_STKPKGID_STKID.png
    urllib.request.urlretrieve('http://dl.stickershop.line.naver.jp/products/0/0/' + STKVER + '/' + STKPKGID + '/android/stickers/' + STKID + '.png',
            dload_dir + '/' + STKVER + '_' + STKPKGID + '_' + STKID + '.png')
