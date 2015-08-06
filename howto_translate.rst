How to localizate the help content
==================================

Help activity supports translation of the text, and will show to the 
user the content in the language configured in Sugar if available.
The same ability is included in the contextual help included in Sugar.
Only the text is localized, not the images, to keep the activity
size relatively small. This means the text in the images will be in English.
While not ideal, is a compromise. We try not include text in the images,
when needed, we add numbers in the images and mention that numbers in the
page text.

The help text is stored in .rst format, and we use Sphinx to generate html,
and other output formats. Sphinx also is used to generate the translated html files.
Here we describe the process used to generate them.


Steps in the translation process:
---------------------------------

1. Create the po files. This is done just one time (while there are not changes,
in the .rst files)::

    make gettext

The .pot files are generated in the directory ./po

2. Create the .po files to enable translation. This need be done for every language 
we want translate. You need substitute *lang* by your two letters ISO 639-1 language code::

    ./init_l10n.sh lang

The files are created in translated_po/lang

Now the translators can start to translate the .po files.
If you never saw a .po file have a header and every paragraph have a format similar
to the following example::

    # 461fbe19d69643f1b6ddbfdde9dffc62
    #: ../source/about_sugar.rst:61
    msgid ""
    "Sugar Labs is a non-profit foundation whose mission is to produce, "
    "distribute, and support the use of the Sugar learning platform. Sugar Labs "
    "supports the community of educators and software developers who want to "
    "extend the platform and who have been creating Sugar Activities. Sugar is a "
    "community project. It is available under the open-source GNU General Public "
    "License (GPL) and free to anyone who wants to use or extend it."
    msgstr ""

The translator work is complete the msgstr part. The msgid should not be changed.
The lines starting with # are comments and can be ignored.
The last example translated to Spanish will be::

    # 461fbe19d69643f1b6ddbfdde9dffc62
    #: ../source/about_sugar.rst:61
    msgid ""
    "Sugar Labs is a non-profit foundation whose mission is to produce, "
    "distribute, and support the use of the Sugar learning platform. Sugar Labs "
    "supports the community of educators and software developers who want to "
    "extend the platform and who have been creating Sugar Activities. Sugar is a "
    "community project. It is available under the open-source GNU General Public "
    "License (GPL) and free to anyone who wants to use or extend it."
    msgstr ""
    "Sugar Labs es una fundación sin fines de lucro cuya misión es producir, "
    "distribuir y apoyar el uso de la plataforma de aprendizaje Sugar. Sugar "
    "Labs apoya la comunidad de educadores y desarrolladores de software que "
    "quieran ampliar la plataforma y que han creado Actividades para Sugar. "
    "Sugar es un proyecto de la comunidad. Está disponible bajo la "
    "licencia GNU General Public License (GPL) y es libre para cualquier "
    "persona que quiera utilizar o ampliarlo."

After the .po files have been created, you can try initialize those files
with a automatic translation. We have a script to send every paragraph,
from every file to the Google Translate service, get the result and update
the .po files. The result of course is not good enough, but usually is less
work correct the mistakes that start the translation from zero.

To run the scrip you need do::

    python tools/seed_translation.py lang


3. Generate translated html files. Once you have finished translate (or every
time you want check the result of your translation), you do::

    ./l10n_script.sh lang

The html files will be created in the directory html/*lang*.

You can send your translations to the Help activity maintainer and a new version
of the activity will be created ready to be distributed.

Notes specifics about the translation of our Help  files
========================================================

* "Sugar" or "Sugar Labs" are names, and should not be translated.

* For the activity names, and element from the interface, use the same names,
that are already used in the translations fo revery activity.
 
* In some cases. rst format is included in a paragraph, by example::

    msgid ""
    "|sugar_sharing| Sugar facilitates sharing and collaboration. Children can "
    "write documents, share books and pictures, or make music together with ease."

In this case *|sugar_sharing|* with the bars (|), means a image with that name
will be inserted in the text. You need preserve that untranslated.

You can read more about .rst format here:

https://help.sugarlabs.org/restructuredtext.html

Contact
=======

The current maintainer of Help activity is Gonzalo Odiard <godiard@gmail.com>
As the translation is a process, is recommended contact the maintainer and 
coordinate tasks.
