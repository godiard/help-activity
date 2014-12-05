==============
Music Keyboard
==============

.. image :: ../images/musickeyboard.png

About
-----

This activity born as a proof of concept for a piano keyboard widget, with the idea of add this widget to the existing Tam Tam suite. This widget should be usable with touch devices, as the XO-4, and support multiple touches, then we need use Gtk3 (Gtk2 only support a simple touch emulation). The `port of Tam Tam suite to Gtk3 <http://wiki.sugarlabs.org/go/Features/GTK3/Porting/TamTam>`_ already started, but is complex and need more work.

The piano widget trigger events for every key pressed/released, and is designed to be easily included in other activities.

The part of the code needed to play the notes, is copied from Tam Tam suite. The backend is using csound, but has not been improved in a lot of time.


Repositories
------------
`The Music Keyboard repository <https://github.com/godiard/music-keyboard-activity>`_

`The Tam Tam repository <https://git.sugarlabs.org/tamtam>`_

Note the master branch in the Tam Tam repository is where the port to Gtk3 started, but is not finished. If you want generate a usable activity, should use the branch sugar-0.94


Download
--------
`Activity page in our activities portal <http://activities.sugarlabs.org/sugar/addon/4654>`_

More Info
---------
If you never developed a Sugar Activity, `must read <http://www.flossmanuals.net/make-your-own-sugar-activities/>`_.

Note, most of the book examples use Gtk2, but we moved to Gtk3.

General information about port from Gtk2 to Gtk3 is `here <http://wiki.sugarlabs.org/go/Features/GTK3/Porting>`_

If you want help us fixing some bugs on activities, and learn a little about how activities work, you can see at this `list of pending tickets <http://dev.laptop.org/~gonzalo/bugs_index.html>`_

References
----------
`Wiki Page <http://wiki.sugarlabs.org/go/Activities/Music_Keyboard>`_