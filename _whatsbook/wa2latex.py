#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
wa2latex.py
Pelle Beckman, 2016
Kancelot To, 2019

Reformats data from WhatsApp chat logs for LaTeX.
See medium.com/@pbeck and the article about 'Books from WhatsApp'
for more info. Uses code from socialmediaparse
(github.com/seandolinar/socialmediaparse).

Requires python2.7 and pandas ('pip install pandas').

2016-01-30
Code is pretty crude, but gets (most of) the job done.
Currently does not support skin modifiers

2016-02-09
Added if clause to final print output for Win support
'''

import io
import sys
import re
import os
import csv
import pandas as pd
from datetime import datetime

class EmojiHandler(object):
    def __init__(self):
        #loads the emoji table in the data folder in the package
        file_path = os.path.dirname(os.path.abspath(__file__))
        emoji_key = pd.read_csv(file_path + '/data/' + 'emoji_table.txt', encoding='utf-8', index_col=0)

        #loads the diversity table
        diversity_df = pd.read_csv(file_path + '/data/' + 'diversity_table.txt', encoding='utf-8', index_col=0)

        #intialize emoji count
        emoji_key['count'] = 0
        emoji_dict = emoji_key['count'].to_dict()
        emoji_dict_total = emoji_key['count'].to_dict()

        #initialize diversity analysis
        diversity_df['count'] = 0
        diversity_keys = diversity_df['count'].to_dict().keys()
        human_emoji = []

        for emoji in diversity_keys:
            emoji = emoji.replace(u'\U0001f3fb', '')
            emoji = emoji.replace(u'\U0001f3fc', '')
            emoji = emoji.replace(u'\U0001f3fd', '')
            emoji = emoji.replace(u'\U0001f3fe', '')
            emoji = emoji.replace(u'\U0001f3ff', '')
            human_emoji.append(emoji)

        human_emoji_unique = list(set(human_emoji))
        human_emoji_dict = {}

        for emoji in human_emoji_unique:
            human_emoji_dict[emoji] = 0

        self.dict = emoji_dict
        self.dict_total = emoji_dict_total
        self.emoji_list = emoji_dict.keys()
        self.baskets = []
        self.total_emoji = 0
        self.total_indiv_emoji = 0

        self.skin_tones = ['\U0001f3fb', '\U0001f3fc', '\U0001f3fd', '\U0001f3fe', '\U0001f3ff']
        self.skin_tones_dict = {'human_emoji': 0, '\U0001f3fb':0, '\U0001f3fc':0, '\U0001f3fd': 0, '\U0001f3fe':0, '\U0001f3ff':0}
        self.human_emoji = human_emoji_unique
        self.human_emoji_dict = human_emoji_dict

    def replace_emoji(self, text):
        for emoji in self.emoji_list:
            if emoji in text:
                text = text.replace(emoji, "\\emoji{" + emoji.encode('unicode-escape').encode('utf-8') + "}")
                text = text.replace("\"", "")
                text = text.replace(u"\\U000", "")
                text = text.replace(u"\\u000", "")

        for emoji in self.human_emoji:
            if emoji in text:
                text = text.replace(emoji, "\\emoji{" + emoji.encode('unicode-escape') + "}")
                #text = text.replace(u"\\U000", "")
        return text

# line emoji mapping
emoji_location = '../line/_emoji/'
line_emoji = {
        u'\U00100078': '100_5_701.png',
        u'\U00100079': '100_5_702.png',
        u'\U0010007A': '100_5_703.png',
        u'\U0010007B': '100_5_704.png',
        u'\U0010007C': '100_5_705.png',
        u'\U0010007D': '100_5_706.png',
        u'\U0010007E': '100_5_707.png',
        u'\U0010008C': '100_5_721.png',
        u'\U0010008D': '100_5_722.png',
        u'\U0010008E': '100_5_723.png',
        u'\U0010008F': '100_5_724.png',
        u'\U00100090': '100_5_725.png',
        u'\U00100091': '100_5_726.png',
        u'\U00100092': '100_5_727.png',
        u'\U00100093': '100_5_728.png',
        u'\U00100094': '100_5_729.png',
        u'\U00100095': '100_5_730.png',
        u'\U0010007F': '100_5_708.png',
        u'\U00100080': '100_5_709.png',
        u'\U00100081': '100_5_710.png',
        u'\U00100082': '100_5_711.png',
        u'\U00100083': '100_5_712.png',
        u'\U00100096': '100_5_731.png',
        u'\U00100097': '100_5_732.png',
        u'\U00100098': '100_5_733.png',
        u'\U00100099': '100_5_734.png',
        u'\U0010009A': '100_5_735.png',
        u'\U0010009B': '100_5_736.png',
        u'\U0010009C': '100_5_737.png',
        u'\U0010009D': '100_5_738.png',
        u'\U0010009E': '100_5_739.png',
        u'\U00100084': '100_5_713.png',
        u'\U00100085': '100_5_714.png',
        u'\U00100086': '100_5_715.png',
        u'\U00100087': '100_5_716.png',
        u'\U00100088': '100_5_717.png',
        u'\U00100089': '100_5_718.png',
        u'\U0010008A': '100_5_719.png',
        u'\U0010008B': '100_5_720.png',
        u'\U0010009F': '100_5_740.png',
        u'\U00100001': '100_5_741.png',
        u'\U00100002': '100_5_742.png',
        u'\U00100003': '100_5_743.png',
        u'\U00100004': '100_5_744.png',
        u'\U00100005': '100_5_745.png',
        u'\U00100006': '100_5_746.png',
        u'\U00100007': '100_5_747.png',
        u'\U00100008': '100_5_748.png',
        u'\U00100009': '100_5_749.png',
        u'\U0010000A': '100_5_750.png',
        u'\U0010000B': '100_5_751.png',
        u'\U0010000C': '100_5_752.png',
        u'\U0010000D': '100_5_753.png',
        u'\U0010000E': '100_5_754.png',
        u'\U0010000F': '100_5_755.png',
        u'\U00100010': '100_5_756.png',
        u'\U00100011': '100_5_757.png',
        u'\U00100012': '100_5_758.png',
        u'\U00100013': '100_5_759.png',
        u'\U00100014': '100_5_760.png',
        u'\U00100015': '100_5_761.png',
        u'\U00100016': '100_5_762.png',
        u'\U00100017': '100_5_763.png',
        u'\U00100018': '100_5_764.png',
        u'\U00100019': '100_5_765.png',
        u'\U0010001A': '100_5_766.png',
        u'\U0010001B': '100_5_767.png',
        u'\U0010001C': '100_5_768.png',
        u'\U0010001D': '100_5_769.png',
        u'\U0010001E': '100_5_770.png',
        u'\U0010001F': '100_5_771.png',
        u'\U00100020': '100_5_772.png',
        u'\U00100021': '100_5_773.png',
        u'\U00100022': '100_5_774.png',
        u'\U00100023': '100_5_775.png',
        u'\U0010005D': '100_5_776.png',
        u'\U0010005F': '100_5_777.png',
        u'\U0010005E': '100_5_778.png',
        u'\U001000A0': '100_5_779.png',
        u'\U001000A1': '100_5_780.png',
        u'\U00100024': '100_5_781.png',
        u'\U001000A2': '100_5_782.png',
        u'\U001000A3': '100_5_783.png',
        u'\U001000A4': '100_5_784.png',
        u'\U001000A5': '100_5_785.png',
        u'\U001000A6': '100_5_786.png',
        u'\U001000A7': '100_5_787.png',
        u'\U00100026': '100_5_788.png',
        u'\U00100027': '100_5_789.png',
        u'\U00100029': '100_5_790.png',
        u'\U0010002A': '100_5_791.png',
        u'\U0010002B': '100_5_792.png',
        u'\U0010002C': '100_5_793.png',
        u'\U0010002D': '100_5_794.png',
        u'\U0010002E': '100_5_795.png',
        u'\U0010002F': '100_5_796.png',
        u'\U0010003A': '100_5_797.png',
        u'\U001000A8': '100_5_798.png',
        u'\U001000A9': '100_5_799.png',
        u'\U001000AA': '100_5_800.png',
        u'\U001000AB': '100_5_801.png',
        u'\U001000AC': '100_5_802.png',
        u'\U00100033': '100_5_803.png',
        u'\U001000AD': '100_5_804.png',
        u'\U00100030': '100_5_805.png',
        u'\U00100031': '100_5_806.png',
        u'\U00100032': '100_5_807.png',
        u'\U001000AE': '100_5_808.png',
        u'\U00100035': '100_5_809.png',
        u'\U00100036': '100_5_810.png',
        u'\U00100039': '100_5_811.png',
        u'\U00100037': '100_5_812.png',
        u'\U00100038': '100_5_813.png',
        u'\U001000AF': '100_5_814.png',
        u'\U001000B0': '100_5_815.png',
        u'\U001000B1': '100_5_816.png',
        u'\U001000B2': '100_5_817.png',
        u'\U001000B3': '100_5_818.png',
        u'\U0010003B': '100_5_819.png',
        u'\U0010003C': '100_5_820.png',
        u'\U0010003D': '100_5_821.png',
        u'\U001000B4': '100_5_822.png',
        u'\U00100040': '100_5_823.png',
        u'\U00100041': '100_5_824.png',
        u'\U00100042': '100_5_825.png',
        u'\U00100043': '100_5_826.png',
        u'\U00100044': '100_5_827.png',
        u'\U00100045': '100_5_828.png',
        u'\U001000B5': '100_5_829.png',
        u'\U00100047': '100_5_830.png',
        u'\U00100049': '100_5_831.png',
        u'\U0010004A': '100_5_832.png',
        u'\U0010004B': '100_5_833.png',
        u'\U0010004C': '100_5_834.png',
        u'\U0010004D': '100_5_835.png',
        u'\U0010004E': '100_5_836.png',
        u'\U0010004F': '100_5_837.png',
        u'\U00100050': '100_5_838.png',
        u'\U00100051': '100_5_839.png',
        u'\U00100053': '100_5_840.png',
        u'\U00100054': '100_5_841.png',
        u'\U00100055': '100_5_842.png',
        u'\U00100056': '100_5_843.png',
        u'\U001000B6': '100_5_844.png',
        u'\U00100057': '100_5_845.png',
        u'\U00100058': '100_5_846.png',
        u'\U00100059': '100_5_847.png',
        u'\U001000B7': '100_5_848.png',
        u'\U0010005B': '100_5_849.png',
        u'\U0010005C': '100_5_850.png',
        u'\U00100060': '100_5_851.png',
        u'\U00100061': '100_5_852.png',
        u'\U00100062': '100_5_853.png',
        u'\U001000B8': '100_5_854.png',
        u'\U001000B9': '100_5_855.png',
        u'\U00100064': '100_5_856.png',
        u'\U00100065': '100_5_857.png',
        u'\U00100066': '100_5_858.png',
        u'\U00100067': '100_5_859.png',
        u'\U00100068': '100_5_860.png',
        u'\U00100069': '100_5_861.png',
        u'\U0010006A': '100_5_862.png',
        u'\U0010006B': '100_5_863.png',
        u'\U0010006C': '100_5_864.png',
        u'\U0010006D': '100_5_865.png',
        u'\U0010006E': '100_5_866.png',
        u'\U0010006F': '100_5_867.png',
        u'\U00100070': '100_5_868.png',
        u'\U00100071': '100_5_869.png',
        u'\U00100072': '100_5_870.png',
        u'\U00100073': '100_5_871.png',
        u'\U00100074': '100_5_872.png',
        u'\U00100075': '100_5_873.png',
        u'\U00100076': '100_5_874.png',
        u'\U00100077': '100_5_875.png'
        }

# sticon mapping
sticon_mapping_file = 'sticon_keywords_Merged.tsv'


if __name__ == '__main__':
    emojis = EmojiHandler()
    month = None
    prevdate = None
    prevmonth = None
    prevsender = None
    prevdt = datetime(2009, 10, 13, 0, 0, 0, 0)

    with io.open(sys.argv[1], 'r', encoding="utf-8") as f:
        for line in f.readlines():
            #######################
            # Pre-pre-processing
            #######################

            # Remove trailing newline chars
            line = line.rstrip()

            # Skip if empty line
            if line in ['', '\n', '\r\n']:
                continue

            # grab important infos
            line = line.replace("-", "|", 1)    # date seperator, replace to disambiguate
            date, _ = line.split(" | ", 1)
            sender, message = _.split(": ", 1)
            dt = datetime.strptime(date, "%d/%m/%y, %H:%M")
            date = dt.strftime("%a\\enspace%-d/%m/%Y")
            month = dt.strftime("%B")
            time = dt.strftime("%H:%M")

            #######################
            # Sectioning-off
            #######################

            # print chapter months
            if prevmonth != month:
                if prevmonth is not None:
                    print(u"\end{longtable}\n")
                print(u"\chapter{%s}\n" % month)

            # print section dates
            # TODO: Some lines do not start with dates
            if prevdate != date:
                if prevdate is not None and prevmonth == month:
                    print(u"\end{longtable}\n")
                print(u"\\needspace{4\\baselineskip}")
                print(u"\section*{%s}" % date)
                print(u"\\begin{longtable}{Rp{0.9\linewidth}}")
                prevsender = None

            #######################
            # Special cases
            #######################

            # Fix links to LaTeX command '\url{}' (subtitution only)
            # http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
            url_re = re.search(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", message)
            if url_re:
                message = re.sub(url_re.re.pattern, "\\url{" + url_re.group(0) + "}", message)

            # Include media attachments (special case)
            # http://tex.stackexchange.com/questions/32886/how-to-fit-a-large-figure-to-page
            # TODO: Handle video? (.mp4, .mov, etc)
            media_re = re.search(r"([\./%a-zA-Z0-9-_]+).(jpg|png)", line)
            if media_re and not url_re:
                # print time in margin?
                if (dt - prevdt).total_seconds() / 60 > 6 or prevdate != date:
                    print_margin = True
                else:
                    print_margin = False

                # sender
                if sender.startswith("Kancelot"):
                    sender = u"\\kancelot"
                else:
                    sender = u"\\cecilia "

                # display sender normally for stickers, always for pics; stickers are smaller
                if "sticker" in media_re.group(0):
                    if prevsender == sender and not print_margin:
                        sender = u"        "
                    message = sender + u" & \\includegraphics[height=2.5cm,keepaspectratio,valign=t]{" + media_re.group(0) + u"} \\\\"
                else:
                    message = sender + u" & \\includegraphics[width=0.88\\textwidth,keepaspectratio,valign=t]{" + media_re.group(0) + u"} \\\\"
                              #u"\\caption{from " + line.split()[3] + " @ " + line.split()[1] + "}"

                # print graphics command
                print(u"\n\\rule{0pt}{3ex}")
                if print_margin:
                    print(u"\marginnote{%s}" % time)
                print(message)
                print(u"\\rule{0pt}{3ex}\n")

                # set previous variables
                prevmonth = month
                prevdate = date
                prevsender = sender
                prevdt = dt
                continue

            #######################
            # Pre-processing
            #######################

            # Replace LaTeX reserved chars
            # TODO: handle backslashes properly (hard because what's being replaced has backslashes...)
            if not url_re and not media_re:
                # have to do this first because some replacements contain {}
                message = message.replace("{", "\\{")
                message = message.replace("}", "\\}")
                #message = message.replace("\\", "\\textbackslash{}")
                message = message.replace(":\\", ":\\textbackslash{}")
                message = message.replace("=\\", "=\\textbackslash{}")
                message = message.replace(u"¯\\_(ツ)_/¯", u"¯\\textbackslash{}_(ツ)_/¯")

                message = message.replace("~", "\\textasciitilde{}")
                message = message.replace("^", "\\textasciicircum{}")
                message = message.replace("&", "\\&")
                message = message.replace("$", "\\$")
                message = message.replace("#", "\\#")
                message = message.replace("%", "\\%")
                message = message.replace("_", "\\_")
                message = message.replace("-", "\\-")
                message = message.replace(u"…", "...")

                # smart quotes (thrice to be safe)
                message = message.replace(" '", " `")
                message = message.replace("\"", "``", 1)
                message = message.replace("\"", "''", 1)
                message = message.replace("\"", "``", 1)
                message = message.replace("\"", "''", 1)
                message = message.replace("\"", "``", 1)
                message = message.replace("\"", "''", 1)
                message = message.replace(u"“", "``")
                message = message.replace(u"”", "''")

            # Remove various cruft (might require editing for localized stuff)
            #message = re.sub("<.*>", "", message)

            # replace emoji
            message = emojis.replace_emoji(message)
            message = message.replace("\\ufe0f", "")
            message = message.replace("\\emoji{\\u", "\\emoji{")
            message = message.replace("\emoji{1f4741f3fd}", "\emoji{1f474-1f3fd}")

            # test if line is pure ascii before searching for emojis
            # (compute-intensive)
            try:
                message.encode('ascii')
            except UnicodeEncodeError:
                # replace line emoji
                for k in line_emoji:
                    emoji_re = re.search(k, message, re.UNICODE)
                    if emoji_re:
                        message = re.sub(emoji_re.re.pattern, 
                                "\\includegraphics[height=0.5cm,keepaspectratio,valign=m]{" + emoji_location + line_emoji[emoji_re.group(0)] + u"}",
                                message)

                # replace line sticon -- search for ending char
                while u'\U0010FFFF' in message:
                    message_bytes = bytearray(message, 'utf8')

                    i = 0
                    index_start = -1
                    index_end = -1
                    while i < len(message_bytes) - 3:
                        if index_start == -1 and message_bytes[i] == 0xF4 and message_bytes[i+4] == 0xF4:
                                index_start = i
                                i += 5
                                continue
                        if index_end == -1 and message_bytes[i] == 0xF4 and \
                                message_bytes[i+1] == 0x8F and \
                                message_bytes[i+2] == 0xBF and \
                                message_bytes[i+3] == 0xBF:
                            index_end = i
                            break
                        i += 1

                    keyword = message_bytes[index_start+8 : index_end].decode('utf8')
                    del message_bytes[index_start : index_start + 8]
                    del message_bytes[index_end - 8 : index_end - 8 + 4]
                    message = message_bytes.decode('utf8')
                    message = message[:index_start] + \
                            'STICON(' + message[index_start:index_start + len(keyword)] + ')' + \
                            message[index_start + len(keyword):]
                    #sys.stderr.write(message + '\n')

                # read from mapping file to replace
                with open(sticon_mapping_file, 'r') as mapping_file:
                    reader = csv.reader(mapping_file, delimiter='\t')
                    for keyword, path in reader:
                        sticon_re = re.search(r'STICON\(' + keyword + r'\)',
                                message)
                        if sticon_re:
                            message = re.sub(sticon_re.re.pattern,
                                "\\includegraphics[height=0.5cm,keepaspectratio,valign=m]{" + path + u"}",
                                message)

            # Add LaTeX line endings
            message = message.replace("\\n", " \\\\ & ")
            message = message + " \\\\"

            #######################
            # Printing
            #######################

            # print time in margin as well?
            if (dt - prevdt).total_seconds() / 60 > 6 or prevdate != date:
                print(u"\marginnote{%s}" % time)
                print_margin = True
            else:
                print_margin = False

            # print sender
            if prevsender != sender or print_margin:
                if sender.startswith("Kancelot"):
                    message = u"\\kancelot & " + message
                else:
                    message = u"\\cecilia  & " + message
            else:
                message = u"          & " + message

            # set previous variables
            prevmonth = month
            prevdate = date
            prevsender = sender
            prevdt = dt

            # output the line
            print(message.encode('utf-8'))

        print(u"\end{longtable}\n")
