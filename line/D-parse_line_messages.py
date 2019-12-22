#!/usr/bin/env python3

from bpylist import bplist
from datetime import datetime
import sqlite3
import os

chat_sqlite = 'iphonex/Line.sqlite'
sticker_dir = '_stickers'
picture_dir = '_attachments'
video_dir = '_attachments'
date_limit = ('1529848800000',)  # before 25/06/2018 00:00 (1 month anniv. + 2d)
query = 'SELECT ZCONTENTTYPE, ZTIMESTAMP, ZSENDER, ZID, ZTEXT, ZCONTENTMETADATA FROM `ZMESSAGE` WHERE `ZCHAT` = 3 AND ZTIMESTAMP < ? ORDER BY `ZTIMESTAMP` ASC;'
output_file = 'LINE Chat with XXX.txt'

texts = 0
pics = 0
vids = 0
stickers = 0
unknowns = 0

# do query
conn = sqlite3.connect(chat_sqlite)
c = conn.cursor()
c.execute(query, date_limit)
rows = c.fetchall()
c.close()
print('rows =', len(rows))

# iterate through results
with open(output_file, 'w') as f:
    for row in rows: 
        content_type = row[0]
        timestamp = row[1]
        sender = row[2]
        zid = row[3]
        text = str(row[4]).strip().replace('\n', '\\n')
        blob = row[5]

        #print('CONTENTTYPE =', content_type, end=', ')
        #print('TIMESTAMP =', timestamp, end=', ')
        #print('SENDER =', sender, end=', ')
        #print('ZID =', zid, end=', ')
        #print('TEXT =', text, end=' ')
        #print()

        # write date
        ts = datetime.fromtimestamp(timestamp/1000)
        f.write(ts.strftime('%-d/%-m/%y, %H:%M'))

        # write seperator
        f.write(' - ')

        # write sender
        if sender == 103:
            f.write('Kancelot To')
        else:
            f.write('Cecilia Chan')

        # write seperator
        f.write(': ')

        # write message
        if content_type == 0:
            # text
            texts += 1
            text.replace("’", "'")
            f.write(text)

        elif content_type == 1:
            # picture
            pics += 1
            path = picture_dir + '/' + zid + '.jpg'
            if os.path.exists(path):
                f.write(path + ' (LINE:picture)')
            else:
                print('WARNING: picture %s doesn\'t exist, msg skipped' % (path))

        elif content_type == 2:
            # video
            vids += 1
            path = video_dir + '/' + zid + '.mp4'
            if os.path.exists(path):
                print('VIDEO screenshot req: %s.mp4' % (zid))
                f.write(path + ' (LINE:video)')
            else:
                print('WARNING: video %s doesn\'t exist, msg skipped' % (path))

        elif content_type == 7:
            # sticker
            stickers += 1
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

            #print('STKVER =', STKVER, end=', ')
            #print('STKPKGID =', STKPKGID, end=', ')
            #print('STKID =', STKID, end=', ')
            #print()
            path = sticker_dir + '/' + STKVER + '_' + STKPKGID + '_' + STKID + '.png'
            if os.path.exists(path):
                f.write(path + ' (LINE:sticker)')
            else:
                print('WARNING: sticker %s doesn\'t exist, msg skipped' % (path))

        else:
            unknowns += 1
            print('WARNING: unhandled content_type=%s, ZID=%s' % 
                    (content_type, zid))

        # end of this line
        f.write('\n')

# summary
print('text =', texts)
print('pics =', pics)
print('vids = ', vids)
print('stickers =', stickers)
print('unknown =', unknowns)
