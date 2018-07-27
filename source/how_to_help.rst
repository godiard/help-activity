===============================
How to edit Help and contribute
===============================

Help displays documentation for Sugar and the XO laptop.

This version of Help contains all the source files and images, and now a *View source* button. These files can be edited within Help, and displayed. Help is now capable of producing new pages for Help, or making completely fresh documentation.

This page aims to show how to write attractive documentation, which, if users share their work, could be used to improve Help. To contribute you only need to:

* Create a development environment
* Make changes
* Contribute the changes

Create a development environment
--------------------------------

XO Help.xo 17 already includes the source files ready to use.

Alternatively, you can use git to get Help Activity with the most recent sources included. If you have the Activity Help already installed, uninstall it first. Generally an Activity is uninstalled from the F3, Home View, List, by selecting the Activity, and press Erase. Where Erase is not available, you need to delete ``Help.activity`` from the folder ``~/Activities``.

The following guide assumes you ``git clone`` from your home directory. This command will collect all the required resources.

::

 git clone git@github.com:godiard/help-activity.git

You can install it in your Sugar development environment doing: ::

 cd help-activity
 ./setup.py dev

You need have a complete sugar environment to run "setup.py dev" if you have a error in your system, try run it in the Terminal Activity.

and, when you are ready, to populate your Help pages ::

 make html

You can modify any .rst file in ~/help-activity/source/ directory or the images in the ~/help-activity/source/images/ directory.

To create the new HTML files you only need do: ::

 cd help-activity
 make html

If you see an error indicating that HTML cannot be built, the most likely cause is that ``python-sphinx`` is missing.

To fix this, in Terminal Activity (or any terminal emulator) as root, ::

 yum install python-sphinx

or in Debian or Ubuntu derivatives, ::

 sudo apt-get install python-sphinx

In **Sugar** you don't need restart Help to see the changes after running ``make html``, you just click with the secondary mouse button, and select reload.

In any other, non-Sugar, Linux environment the command ``git clone git@github.com:godiard/help-activity.git`` works to download the sources, ``./setup.py dev`` should be omitted, and the output of ``make html`` is in ``~/help-activity/html``, and is displayed by opening ``~/help-activity/html/index.html`` in a browser.

What if I break Help?
:::::::::::::::::::::

In Sugar you cannot break Help. If you start to follow these instructions and get lost or make a mistake, and Help will not display correctly, you should not worry.

First back up any files.rst you have already made, then visit `ASLO <http://activities.sugarlabs.org>`_ with Browse. Search for Help, and download and install a new copy of XO Help.

Alternatively, experienced users might make a backup .xo before starting to work by doing: ::

 ./setup.py dist_xo

This will create a directory dist and inside, an .xo file.

Tutorial 0 - Browse filesystem
::::::::::::::::::::::::::::::

In Browse and some other browsers if you type ::

 file:///

in the address bar, you will be browsing the root of your file system.

Now move progressively through ::

 file:///home

 file:///home/your-username

 file:///home/your-username/help-activity

 file:///home/your-username/help-activity/source

You are now able to open and inspect any of the *source_files.rst* safely.

We can back off again and reach ::

 file:///home/your-username/help-activity/html

and then select and display any of the output HTML files.

In this page we use the convention of calling ``/home/your-username/help-activity/source`` by the shorter, ``~/help-activity/source``.

.. _Orientation:

Orientation
:::::::::::

**Source**

The two source folders we look at are filled initially by the download of Help.

The directory ``~/help-activity/source/`` contains the text files we will be altering in this guide.

The directory ``~/help-activity/images/`` contains all the images that are used on the various pages of Help. You can add image files to this folder, and if they are linked into documents, they will display in the *output* of the command ``make html``.

In Sugar you have the ability to inspect the source files safely, using the *View source* button on the Help icon in the Frame.

The key page in navigating Help is the Index or contents page. In the ``~/help-activity/source/`` folder, `index.rst` is the text document which automatically provides links to all other pages in the source folder.

**Output**

The pages displayed in Help are the output of the command ``make html``. The files are in the folder ``~/help-activity/html/``.

Also part of the output of the command ``make html`` are the files in ``~/help-activity/doctrees/``. The role of the ``all_files.doctree`` is to interlink all the HTML pages within the rules of the underlying software.

Depending on the setup of your installation there may be a number of other folders present in the ``~/help-activity/html/`` folder (for instance ``_sources``, ``_static``, and ``_images``). These are also *output files*, they could be regarded as hidden folders, and should not be edited.

Make changes
------------

You can just write a page in simple text, perhaps with some explanatory pictures or screen-shots. Screen-shots are made in Sugar from the keyboard, by pressing the "Alt" key and 1.

The page :doc:`/restructuredtext` gives some guidance on the features of the markup language we use. Do not be concerned with complex features, plain, simply written text will be of most use to new learners.

You will have your own ideas about what you would like to change and contribute. When you explain anything, which you have struggled to learn, it is likely to be of use to others. Seeing your work published gives quite a buzz!

Here are a few exercises, which demonstrate making changes, and making pages.

Tutorial 1 - Make a page
::::::::::::::::::::::::

We are going to make a fresh page in reStructuredText. It will not at first be connected to the index, or contents page, of Help.

1. Open a new file in any text editor.

2. Save the file with the name ``my_first.rst`` in ``~/help-activity/source``. Type some text onto the page. In order to give the page a title we put a line of "=" "equal" signs above and below the title like this. Leave a line of white space, then type some text. This is an example:

::

 =============
 My first page
 =============

 I am going to learn to write a Help page.

3. Now we want to convert our little page of text into an attractive page of Help. Open Terminal Activity (or any terminal emulator) and type,

::

 cd help-activity
 make html

4. There will be about ten lines of output, there will be mention of errors. Read the error trace, expect to see an error line like the one below, but the final two lines here report a success.

::

 ~/help-activity/source/my_first.rst:: WARNING: document isn't included in any toctree
 ...
 build succeeded, 3 warnings.
 Build finished. The HTML pages are in ./html.

The warning, "WARNING: document isn't included in any toctree" is telling us the document is not linked into the Help index yet.

Tutorial 2 will fix this. It does exist and you could see what it looks like if you can find it as described above with a browser in ``~/help-activity/html``.

Tutorial 2 - Link page to index
:::::::::::::::::::::::::::::::

1. Backup your index file. Open Terminal Activity (or any terminal emulator) and type,

::

 cd help-activity
 cd source
 cp index.rst index.rst.ori

Above, we have changed directory into help-activity, changed directory into source, and copied ``index.rst`` to a new file named ``index.rst.ori``

2. Before proceeding make sure you are familiar with how to restore your index from the backup, in case you damage your Help index.

3. Open ``~/help-activity/source/index.rst`` with a text editor. Notice the line spacing (lines of white space especially) and indents. They are very important to maintain.

4. Scroll down ``index.rst`` right to the bottom of the page. Put the cursor at the front of the last line. Using the arrow keys you will see that the indent is 4 "spaces", it is not "Tab".

5. Put the cursor at the end of the last line. Press *Enter*, press space bar 4 times, and enter the file name you used above ``my_page.rst``. Use "Enter" and the space bar so that you exactly copy the indentation, and line spacing as used in the other entries.

6. Double check your changes to ``index.rst`` and save your changes. 

7. Now we want to convert our index into HTML. Open Terminal Activity (or any terminal emulator) and type,

::

 cd help-activity
 make html

8. The newly changed index page will now display in Help, or in your browser, once you reload the page. In Sugar you click with the secondary button, and select reload, or in a browser pointing to ``~/help-activity/html/index.html`` press the reload button. In the index, or contents page, the link to your new page can be clicked to open your page "my_page.html"

Tutorial 3 - Adding an image
::::::::::::::::::::::::::::

1. Open your existing page in any text editor, or create and "Title" a new page, and add it to the bottom of the index.

2. An image which is already in ``~/help-activity/images/`` can be included by typing this on to your page.

::

 .. image :: ../images/Help.png

The "reference line" above needs a line of white space, above and below it.

3. You can add an image file in .jpg or .png format to ``~/help-activity/images/``. It is best if the image does not exceed 800 pixels in width. It can be difficult to read around tall images. For this reason screen-shots 600 pixels in width may be a good compromise if the content is simple.

4. If you add an image file ``my_image.png``, made in, say, Paint to ``~/help-activity/images/``, then you link it into your page with:

::

 .. image :: ../images/my_image.png

5. Now we want to convert our page with an image into HTML. Open Terminal Activity (or any terminal emulator) and type,

::

 cd help-activity
 make html

6. The newly changed page will now display in Help, or in your browser, once you reload the page.

Tutorial 4 - Write or improve a Help page
:::::::::::::::::::::::::::::::::::::::::

Decide whether you want to make a page from a fresh start, you could just start writing on a subject you know about. Alternatively experiment with improving an existing page. You could work from the text of an existing page (it might be this page) or a more simple page.

1. Open ``~/help-activity/source/index.rst``.

2. Put the cursor at the end of the last line. Press *Enter*, press space bar 4 times, and enter a new file name, perhaps, ``my_second.rst``. Use "Enter" and the space bar so that you exactly copy the indentation, and line spacing as used in the other entries.

3. Double check your changes to ``index.rst`` and save your changes.

4. Open a new file in any text editor.

5. Save the page as the new file name chosen above, perhaps, ``my_second.rst``.

6. Type in a title like this:

::

 ==================
 How I changed Help
 ==================

7. Enter your text, and save your changes.


8. Now we want to convert our page into HTML. Open Terminal Activity (or any terminal emulator) and type,

::

 cd help-activity
 make html

9. The newly generated page will now display in Help, or in your browser, once you reload the page.

10. You can now go back to your page, and improve it.

11. Again, write the changes to HTML version, with:

::

 cd help-activity
 make html

12. You have now written your first improved page for the Activity Help. We would love it if you could share it with the Sugar community!

.. _Contribute:

Contribute
----------

Once you are familiar with editing, adding a page, and making or improving a Help page, you could make a page with the intention of having it published in the next version of Help.

You might write a tutorial on a subject you know about.

In the next version of Activity Help, better "New to Sugar" pages might be included at the beginning of Help, as a quick introduction for new Sugar learners. Contributions to be considered would be welcome.

Some Activities have no easy to find instructions. If you can write even a very short introduction, it could be very useful for other Sugar learners.

The Sugarlabs wiki page http://wiki.sugarlabs.org/go/Activities/Help/Contribute might have some ideas on pages, which have been requested, or which others are working on and might appreciate collaboration.

What to do with your finished work
::::::::::::::::::::::::::::::::::

First of all you might briefly contact gonzalo at laptop dot org by e-mail to tell him what you would like to contribute. If you write a new page , you can send him the page (as my_page.rst) as an attachment to an e-mail explaining briefly what is attached. If new images are linked into the page, send them too.

If you have improved a page, the preferred method is to submit it as a "patch".

Tutorial 5 - generate a patch
:::::::::::::::::::::::::::::

1. Let's say you decide to work on the Help page, "Switching Activities". You might back up that page before you start. Open Terminal Activity (or any terminal emulator) and type,

::

 cd help-activity
 cd source
 cp switching_activities.rst switching_activities.rst.ori

Above, we have changed directory into help-activity, changed directory into source, and copied ``switching_activities.rst`` to a new file named ``switching_activities.rst.ori``

2. Make your changes to ``switching_activities.rst``. Save your changes regularly, and check by running the ``make html`` command that the page displays nicely. Once you are happy with your work, you can generate a patch like this:

::

 cd help-activity
 cd source
 diff -u switching_activities.rst.ori switching_activities.rst > switching_activities.patch

3. The patch can now be sent as an e-mail attachment.

4. For more information, in Terminal Activity (or any terminal emulator) type,

::

 man diff

and

::

 man patch

.. _Further reading:

Further reading
---------------

|more| For more complete help on reStructuredText:

.. |more| image:: ../images/more.png

Quick reStructuredText, http://docutils.sourceforge.net/docs/user/rst/quickref.html, is a cheat-sheet for reStructuredText.

"reStructuredText Directives" http://docutils.sourceforge.net/docs/ref/rst/directives.html by David Goodger, March 2013.

Sphinx reStructuredText Primer, http://sphinx-doc.org/rest.html, a brief introduction to reStructuredText concepts and syntax.

Sphinx home page, http://sphinx-doc.org/index.html.

Another tutorial, http://matplotlib.org/sampledoc/.
