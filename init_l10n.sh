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
TRANSLATED_PO_PATH="translated_po/$LANGUAGE"

# check whether a language is set as an argument
if [ "$#" == "0" ]; then
    echo "No language provided"
    echo "Usage: ./l10n_script.sh <language>"
    exit 1
fi

# check and create directories
if [ ! -d $TRANSLATED_PO_PATH ]; then
    mkdir -p $TRANSLATED_PO_PATH
fi

# create po files
for file in po/*.pot
do
    # remove the prefix numbers and build the mo files
    po_file=$(basename $(echo "$file" | sed 's/\.pot/\.po/'))
    if [ -f $TRANSLATED_PO_PATH/$po_file ]; then
        msgmerge -U $TRANSLATED_PO_PATH/$po_file "$file"
    else
        msginit -i "$file" -l $LANGUAGE -o $TRANSLATED_PO_PATH/$po_file --no-translator
    fi
done
