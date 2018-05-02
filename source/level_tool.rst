.. _level-tool:

==========
Level Tool
==========

Level Tool Activity
===================

Level Tool is an activity to check the inclination of a surface with respect to ground.

**Note: You need XO 1.75+ laptop, to use Level Tool.**

.. figure:: ../images/Level.png

How does Level Tool work
------------------------

Level Tool uses your accelerometer to detect the inclination of your XO with respect to ground and displays it in a well defined circular grid.

Where to get Level Tool
-----------------------

The Level Tool activity is available for download from the `Sugar
Activity Library <http://activities.sugarlabs.org>`__: `Level
Tool <http://activities.sugarlabs.org/en-US/sugar/addon/4628>`__

The source code is available on `GitHub <https://github.com/sugarlabs/level-activity>`__.

Where to report problems
------------------------
You can report bugs and make feature requests at `level-activity/issues <https://github.com/sugarlabs/level-activity/issues>`__

Localization tips
-----------------

In short, this activity uses the XO 1.75 and XO-4 internal accelerometer
to measure the tilt of the laptop in the horizontal plane and display x
and y coordinates (to two decimal places).

The only three strings in the PO file are.

Level

x: %.2f

y: %.2f

In this context, the meaning of the word Level would be a verb form (we
try to name activities with verbs to show they are for “doing”) and it
would represent that action of making something flat in the horizontal
plane.

“She levels the sand before building a castle.”

It does NOT have the connotation of “height”, as in “the sound level is
too high”.

If a verb form of “level” is awkward or not available, a noun form
describing the instrument used to measure flatness in the horizontal
plane, would be acceptable and an accurate description of the function
the activity provides.

As for the other two strings

x: %.2f

y: %.2f

The x and y represent the lower-case x and y symbols employed to
describe two of the axes in the Cartesian coordinate system, they are
not really the Latin alphabet letters themselves, but those letters used
as symbols to represent a mathematical concept, in the same manner that
the Greek letter “π” or pi is used to represent the ratio of a circle's
circumference to it's diameter. For many languages, there will be no
need to change the x or y symbol at all, because the true source
language of “mathematics” has a certain universality. The rest of those
two strings “%.2f” instructs the program to display numbers with two
decimal points of precision and should not be changed in L10n.

Author
------

This activity is created by `Aneesh Dogra <http://wiki.sugarlabs.org/go/User:Aneesh_Dogra>`__
