#!/usr/bin/env python3

from datetime import datetime
from operator import itemgetter
import os

fb_file = 'fb/FB Messenger Chat with XXX.txt'
line_file = 'line/LINE Chat with XXX.txt'
whatsapp_file = 'whatsapp/WhatsApp Chat with XXX.txt'
output_file = 'Merged Chats.txt'

fb_lines = []
line_lines = []
whatsapp_lines = []

#if os.path.exists(fb_file) and os.path.exists(line_file) and os.path.exists(whatsapp_file):
if os.path.exists(fb_file):
    with open(fb_file, 'r') as f:
        fb_lines = f.readlines()

if os.path.exists(line_file):
    with open(line_file, 'r') as f:
        line_lines = f.readlines()

if os.path.exists(whatsapp_file):
    with open(whatsapp_file, 'r') as f:
        whatsapp_lines = f.readlines()

lines = fb_lines + line_lines + whatsapp_lines
lines = [line.split(' - ', 1) for line in lines]
lines = [[datetime.strptime(line[0], "%d/%m/%y, %H:%M"), line[1]] for line in lines]
lines = sorted(lines, key=itemgetter(0))

with open(output_file, 'w') as out:
    for line in lines:
        out.write(line[0].strftime('%-d/%-m/%y, %H:%M') + ' - ' + line[1])
