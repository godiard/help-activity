====
Log
====

About
-----

.. image :: ../images/Log0Icon.png

The Log Activity allows you to troubleshoot problems with your computer.  You
can view the log files of Sugar and your Activities.  Log files contain errors,
warnings and debugging information to help you fix problems.

Using Log
---------

.. image :: ../images/Log1Main.png

When you open Log, there are 2 panels.  On the left is a list of log files.
On the right, the contents of the selected file is displayed.

The list of log files is divided into sections, each representing a folder.
Pressing the arrow icon a to the folder name will hide or show its contents.
Items without arrows are log files.  Pressing an item that does not have an
arrow will display the contents of that file in the right panel.

There are 3 main folders in the log file list.  The first is the ``.sugar`` or
``dotsugar`` folder.  This contains the log files of Sugar and your Activities.
The sub-folders contain backups of older logs (log files in ``.sugar`` are
deleted on shutdown).  The second main folder ``/var/log``.  This contains
system log files.  These are helpful for troubleshooting issues related to your
computer hardware.  The last main folder is ``Other``, and contains
miscellaneous log files.

The Toolbars
------------

.. image :: ../images/Log2Toolbar.png

1. Activity Toolbar
2. Hide/Show the list of files
3. Copy the log file
4. Enable/Disable word wrap.  When word wrap is disabled, there is a horizontal
   scroll bar.  When word wrap is enabled, the lines of text too long to fit on
   the screen are broken up.
5. Find and highlight text in the log file
6. Previous matching text
7. Next matching text
8. Delete current log file
9. Stop activity

.. image :: ../images/Log3ActivityToolbar.png

1. Activity Name
2. Activity Description
3. Save log files to Journal.  This packages the log files in a format that you
   can send over the internet.
