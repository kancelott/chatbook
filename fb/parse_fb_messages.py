#!/usr/bin/env python3

from datetime import datetime
from lxml import html

msg_file = 'messages/inbox/XXX_xyzabc/message_1.html'
output_file = 'FB Messenger Chat with XXX.txt'
date_limit = 1529848800000  # before 25/06/2018 00:00

with open(msg_file, 'r') as f:
    with open(output_file, 'w') as fb:
        tree = html.fromstring(f.read())
        messages = tree.xpath("//div[contains(@class, 'pam _3-95 _2pi0 _2lej')]")
        print('messages (total excl. date filter) =', len(messages))

        for m in reversed(messages):
            timestamp = m.xpath(
                    "div[contains(@class, '_3-94 _2lem')]/text()")
            person = m.xpath(
                    "div[contains(@class, '_3-96 _2pio _2lek _2lel')]/text()")
            message = m.xpath(
                    "div[contains(@class, '_3-96 _2let')]/div/div[2]/text()")
            media = m.xpath(
                    "div[contains(@class, '_3-96 _2let')]/div/div[5]//img/@src")
            link = m.xpath(
                    "div[contains(@class, '_3-96 _2let')]/div/div[2]/a/@href")
            link_text = m.xpath(
                    "div[contains(@class, '_3-96 _2let')]/div/div[2]/a/text()")

            # exclusions
            if len(message) == 1 and (message[0].startswith('Say hi to your new Facebook friend') or
                    message[0].startswith('You set the nickname for')):
                continue

            # write date
            if len(timestamp) == 1:
                ts = datetime.strptime(timestamp[0], "%d %b %Y, %H:%M")
                if ts > datetime.fromtimestamp(date_limit/1000):
                    # over the time frame -- exit
                    break
                fb.write(ts.strftime('%-d/%-m/%y, %H:%M'))
            else:
                print('WARNING: multiple timestamp=', timestamp)

            # write seperator
            fb.write(' - ')

            # write sender
            if len(person) == 1:
                if person[0] == 'Kancelot To':
                    fb.write('Kancelot To')
                else:
                    fb.write('Cecilia Chan')
            else:
                print('WARNING: multiple person=', person)

            # write seperator
            fb.write(': ')

            # write message
            if len(message) == 1:
                # text
                fb.write(message[0])

            elif len(message) > 1:
                # link (at least for this instance I found)
                print('WARNING: multilink -- manual hack: review code!!')
                print(timestamp)
                print(message)
                print(person)
                #for multi_message in message:
                #    fb.write(multi_message)
                fb.write('oh maybe you need to go on the messenger.com site')

            elif len(message) == 0 and len(link) == 1:
                # link
                assert(link == link_text)
                fb.write(link[0])

            elif len(message) == 0 and len(media) == 1:
                # media
                fb.write(media[0] + ' (FB:media)')

            else:
                print('WARNING: unforseen message type')
                print(timestamp)
                print(message)
                print(person)

            # end of this line
            fb.write('\n')
