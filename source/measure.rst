.. _measure:

=======
Measure
=======

About
-----

This Activity draws a picture of the sound heard by the internal microphone or of the signal present on the microphone socket. More specifically it draws a graph of this input versus time, the input is on the vertical axis and time is on the horizontal axis. That is, the laptop functions like a machine called an oscilloscope.

As well as graphing signal as a function of time, Measure can also graph as a function of frequency.

The XO-1 laptop is only capable of mono input, the XO-1.5 and XO-1.75 are capable of stereo input on their microphone socket and can graph two signals at once.

.. image :: ../images/200px-Measure_tut_1_24.jpg


Where to get Measure
--------------------

Measure activity is available for download from the `Sugar Activity Library <http://activities.sugarlabs.org/en-US/sugar/>`__:
`Measure <http://activities.sugarlabs.org/en-US/sugar/addon/4197>`__

The source code is available on `GitHub <https://github.com/sugarlabs/Measure>`__.


Using
-----

.. image :: ../images/600px-Measure-screen.JPG

1. Select secondary toolbar - allows the Activity's Journal entry to be renamed
2. Select secondary toolbar - measurement settings
3. The selected input type - Sound (AC voltage), resistance or DC voltage
4. The time scale
5. Freeze the display
6. Capture sample now - saves an image of the wave in the Journal
7. Stop - exits the Activity
8. Invert - invert the display
9. Use these sliders to control the sensitivity
10. The settings that are selected 

.. image :: ../images/600px-Measure2ndtoolbar.JPG

The secondary toolbar - measurement settings

11. Sound - use this setting with the internal microphone, external microphone and external AC signals

12. Resistance sensor - use with external resistive type transducers

13. Voltage sensor - use with external sensors which generate a voltage

14. Time base/frequency - graphs the signal vs. time or graphs amplitude vs. frequency

15. Sample interval - a text file 'Measure Log' is saved to the journal, it contains one sample per interval

16. Starts/stops saving a text file 'Measure Log' with measured values as readable text

17. This feature is not working well in version 36, the intention is to synchronize the sample period to the waveform so that the sample will start on a rising edge or falling edge

Applying
--------

Let the children experiment with the internal microphone, try singing, whistling, musical instruments, the Tam Tam musical Activity. The Turtle Blocks Activity can generate an audio tone, see the Python Block.

The children should learn through guided discovery that:

* sound is a pressure wave
* the pitch of the sound is determined by the frequency or cycles per second (Hz)
* the loudness of a sound is determined by the amplitude
* sounds contain multiple frequency components or harmonics
* the more pure sounds have less harmonics 

Sharing
-------

This Activity does not support sharing.

Extending
---------

Measure is able to take input from a wide range of external sensors including switches, photocells, temperature sensors, inductive loops, hall effect sensors, soil probes and many more.

Care should be taken not to exceed the allowable input voltage:

    XO-1 -0.5 V to 5 V

    XO-1.5 -6 V to +9 V

    XO-1.75 -6 V to +9 V 

It is a good idea, particularly on the XO-1, to put a resistor of 680 ohms in the phono plug, this increases the allowable input voltage range.

You can find ideas for fun science experiments at http://wiki.sugarlabs.org/go/Activities/TurtleArt/Using_Turtle_Art_Sensors and http://wiki.laptop.org/go/Measure 


Where to report problems
------------------------

Please report bugs and make feature requests at `Measure/issues <https://github.com/sugarlabs/Measure/issues>`__.
