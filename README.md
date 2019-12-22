# Chatbook project

This parses chat history logs from the Facebook Messenger, WhatsApp and LINE chat platforms and compiles into tex files to make a book.

This was for a personal project and personal infos have been removed. Do not expect it to work without modifications.

Pretty much based off and forked from <https://medium.com/@pbeck/whatsapp-books-a-hacker-s-guide-edbb397e0bee>.


# FIRST

## For Facebook Messenger chats

* Perform a full Facebook data export and look for the `messages` folder.

* Run the script in the `fb` folder.


## For WhatsApp chats

* Perform a message export in the app to a text file. This format is what was orignally natively supported in the forked code.


## For LINE chats

* Perform a database dump of the appdata from the iPhone itself.

* Run the Python scripts A to D in order to download sticker, sticker icons and to extract the messages.

* There's some manual processing involved here to get sticker icons working properly here; I couldn't find an automated way.


## THEN

* Run `interleave_fb_line_whatsapp.py` to merge all chats into one file.


## FINALLY

* Run `_whatsbook/wa2latex.py` to generate a XeLaTeX file, `whatsbook-folio.tex`.

* Compile `whatsbook.tex`.

* Make a cover in InDesign.

* I manufactured the book on [Blurb](www.blurb.com).
