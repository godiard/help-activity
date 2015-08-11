#!/bin/sh
#This script generates build files for a given lanaguage.
#Copyright (C) 2013  Kalpa Welivitigoda <callkalpa@gmail.com>
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

# usage: l10n_script.sh <language>

LANGUAGE="$1"
SOURCE_DIR="source"
DESTINATION_DIR="html/$LANGUAGE"
TRANSLATED_PO_PATH="translated_po/$LANGUAGE"
TRANSLATED_MO_PATH="source/translated/$LANGUAGE"

# check whether a language is set as an argument
if [ "$#" == "0" ]; then
    echo "No language provided"
    echo "Usage: ./l10n_script.sh <language>"
    exit 1
fi

# create mo files
if [ ! -d $TRANSLATED_PO_PATH ]; then
    echo "No PO files found for the language"
    exit 1
fi

# check and create directories
if [ ! -d $TRANSLATED_MO_PATH/LC_MESSAGES ]; then
    mkdir -p $TRANSLATED_MO_PATH/LC_MESSAGES
fi

for file in $TRANSLATED_PO_PATH/*.po
do
    # remove the prefix numbers and build the mo files
    mo_file=$(basename $(echo "$file" | sed 's/\.po/\.mo/') | sed 's/^[0-9]*_//')
    msgfmt "$file" -o $TRANSLATED_MO_PATH/LC_MESSAGES/"$mo_file"
done

# build html
if [ ! -d $DESTINATION_DIR ]; then
    mkdir $DESTINATION_DIR
fi
sphinx-build -b html -Dlanguage=$LANGUAGE $SOURCE_DIR $DESTINATION_DIR

# remove images files in the translated directories
rm -rf $DESTINATION_DIR/_images

# create symbolic links to _images
ln -rs images $DESTINATION_DIR/_images
