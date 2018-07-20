.. _read-etexts:

===========
Read Etexts
===========

Description & Goals
===================

*“Outside of a dog, a book is man's best friend. Inside of a dog it's
too dark to read.”* -- Groucho Marx

The Read Etexts activity is meant to allow the XO laptop to read Project
Gutenberg ETexts, which are plain text files. The original goal of this
Activity was to create a stopgap for reading plain text files until the
core Read activity was able to do that. Read Etexts has become much more
than that, adding features that core Read does not have, like text to
speech with word highlighting, and most recently the ability to search
the Project Gutenberg offline catalog and download books.

Where to get Read Etexts
========================

Read Etexts activity is available for download from the `Sugar Activity Library <http://activities.sugarlabs.org/en-US/sugar/>`__:
`Read Etexts <http://activities.sugarlabs.org/sugar/addon/4035>`__

The source code is available on `GitHub <https://github.com/sugarlabs/readetexts>`__.


How to use
==========

Since the `ManyBooks.net <http://manybooks.net/>`__ website offers
Project Gutenberg titles as PDFs you might wonder why you would need an
Activity to read plain text files. It is a matter of personal
preference. If you have a choice between a text file and a PDF, you may
find that the text file is easier on the eyes than a PDF, takes up less
space in the Journal (especially in zip format), and uses less memory to
read. You will also find that the offline catalog search (Books tab) is
a really convenient way to download books.

The interface to Read Etexts is very similar to the core Read activity,
which should not be surprising as the toolbar code was adapted from
Read's toolbar. You can use the up and down arrows or the game
controller to scroll pages, and the '+' and '-' keys to adjust the font
size. Use Page Up and Page Down to move to the previous and next pages
respectively.

`Project Gutenberg <http://www.gutenberg.org/wiki/Main_Page>`__ is a
website where you can download thousands of public domain books for
free. There are books for every interest: classics, history, childen's
novels, science fiction, and much, much more. `Browse By Library of
Congress Class: Language and Literatures: Juvenile belles
lettres <http://www.gutenberg.org/browse/loccs/pz>`__ will give you a
list of books suitable for young readers.

Read ETexts can read books in plain text format or in Zip format. These
are by far the most popular formats on the Gutenberg website. If for
some reason you cannot use the Catalog search to get a book you can also
download books from the website using the Browse activity. You should
download one of the Zip file formats. These can be encoded as us-ascii
text or as iso-8859-1; Read Etexts can handle either one. The iso-8859-1
encoding is used for books that need accent marks, etc. Save the Zip
file to the Journal, change the Journal entry name to match the title of
the book, and then resume it using the Read Etexts option on the Resume
menu. See the first screenshot.

Current Features
----------------

-  Currently Read Etexts can be used to read Gutenberg Etexts, either as
   text files or as zip files containing one text file. The toolbars
   include Activity, Read (skip to page), Edit (copy to clipboard,
   search for text) and View (zoom text bigger or smaller). The Books
   toolbar comes up if you launch Read Etexts from the Activity ring.
   This toolbar supports searching the Project Gutenberg offline catalog
   and downloading books.
-  Book sharing is supported.
-  The power management code from the core Read activity has been added,
   with a few minor changes, and seems to work OK.
-  Text to speech with Karaoke highlighting. The purpose of this is to
   produce a tool to help someone learn to read. Support for text to
   speech on the XO laptop is done using a gstreamer plugin for espeak.
   This plugin currently is not part of the software included on the XO,
   but is installed on Sugar on a Stick. You do **not** need this plugin
   installed to use Read Etexts, but you will of course not have text to
   speech working unless you do.
-  The Books toolbar lets you search for books in Project Gutenberg's
   offline catalog. Enter in words that you would expect to find in the
   title or author of a book, then press Enter. A table will appear in
   the lower half of the screen listing book titles and authors that
   contain all of the words. Select a book from that table and click the
   download button and the book will arrive in a minute or so. The
   download tries to get the best available version of the book. For
   instance, it will try to download an 8 bit version of the book, and
   if there is none it will try to get a 7 bit version. (8 bit files
   contain accents and diacritical marks; the 7 bit versions do not. Not
   every text has both versions).
-  You can download several books to the Journal in one session. Each
   book will be given a Journal entry when it downloads.
-  The Activity has an annotation feature that enables the user to
   attach notes to pages in the text. These annotations are stored in a
   pickle file that is included in the Zip file containing the document.
   When you share a document your annotations will go along with it. For
   the recipient it will be sort of like buying a used textbook that has
   all the important stuff already marked up.
-  The Activity supports multiple bookmarks in a document, and easy
   navigating between them. This is in addition to the current feature
   that remembers where you left off when you last read a document.
-  The Activity supports highlightings passages in text. The highlight
   is shown as a yellow background (like a hi-lighter pen would make)
   plus a single underline. You can highlight multiple passages on a
   page.
-  Word wrap is supported for those text documents that require it. Read
   Etexts considers a line of text to be no more than 80 characters, so
   a page break is calculated based on how many 80 character strings
   will fit in the paragraphs, plus one. A page will not break in the
   middle of a paragraph, so not every page is the same number of lines.
-  With version 17 you can now read texts from the Baen Free Library in
   the Rich Text Format (RTF). Read Etexts will automatically convert
   RTF documents to plain text format for reading.

Using Text to Speech
--------------------

Read Etexts uses software called gstreamer espeak plugin to read text
aloud and to perform callbacks which enable the word being spoken to be
highlighted. This plugin is not yet included with the normal XO software
distribution, but is included in Sugar on a Stick.

To start text to speech you simply press the check mark button on the
XO's display (Numeric Keypad “End” on a standard keyboard). This button
will also pause and resume speech. Only the current page will be spoken,
and always starting from the first word on the page unless you are
resuming after pausing. You need to have the text control containing the
text to be spoken in focus. I use the check button because you can use
it when the XO is folded into its ebook reader configuration. There is
also a Play/Pause button on the Speech tab of the toolbar that you can
use instead.

If your system does not have the needed software to support text to
speech you will *not* see the Speech tool bar. This is intentional.

The toolbar is very much like the one in the Speak activity and was
adapted from its code. It allows you to change the language, pitch, and
rate of speech. You can only do this while the Activity is not speaking.
You can pause the speech, change its rate, pitch,or language, and then
resume.

Sharing Documents
-----------------

This activity uses code adapted from the core Read activity for document
sharing over the network. To share a document with someone that person
must also have the Read Etexts activity installed, and it should be the
same version for best results. You can invite an individual to join the
activity or share it with the whole neighborhood, but either way only
those who have the activity installed will see the invitation.

When someone accepts the invitation to join the activity a copy of the
document is sent to his computer for him to read. When he exits the
activity the document will be saved in the journal.

The Baen Free Library
---------------------

The `Baen Free Library <http://www.baen.com/library/>`__ is a website
from Baen Books that publishes free etexts of some of their books with
the idea that this will ultimately increase sales of the printed
editions. So far it seems to be working. Unfortunately, the formats they
offer for downloading are not currently supported by any reading
Activity for Sugar. The closest thing to a supported format is RTF (Rich
Text Format) which you can load into the Write Activity. Write is a poor
choice for reading etexts, unfortunately.

Version 17 of Read Etexts solves this problem by converting RTF to a
plain text file automatically. So now, in addition to the great classics
of literature by dead authors that Project Gutenberg gives you you can
also read fairly current science fiction from Baen Books.

You can use the Browse Activity to download RTF files from the site. Be
sure to choose the RTF file, not the zipped up RTF file. The zipped
version *should* work, but the website does something to it that keeps
it from getting a proper MIME type. I was able to use Browse on my XO
running Sugar .82 to download RTFs. If Browse doesn't work for you an
alternative is to use another computer to download the file to a thumb
drive, then copy that file from the thumb drive to the Journal.

When you Restore the file for the first time be sure to do it with Read
Etexts, *not* Write. Write does something to the file that prevents Read
Etexts from being able to convert it properly. Once you open it with
Read Etexts it will be given the Read Etexts icon and will open with the
correct Activity by default.

I'm dedicating this feature to the author Howard L. Myers. His book *The
Creatures of Man* is available for download from the website. Back in
1974 I was graduating from High School and subscribing to *Galaxy*
magazine. *Galaxy* ran a couple of cracking good yarns by Myers, writing
as “Verge Foray”, in the May and June issues. I was really looking
forward to more in the series, and even wrote an incoherent letter to
the magazine asking for more Verge Foray stories. I only found out this
year why no more stories ever came. Howard L. Myers had died in 1971.


The Movie!
----------

See the future of reading, here today, by watching `Read Etexts: The
Movie <http://www.dailymotion.com/video/xa4bhu_readetexts-the-movie_tech>`__.

*“You are interested in the future, because it is where we will spend
the rest of our lives. And remember my friends, future events such as
these will affect you in the future.”* -- Edward D. Wood


Where to report problems
========================

Please report bugs and make feature requests at `readetexts/issues <https://github.com/sugarlabs/readetexts/issues>`__.

