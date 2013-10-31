#!/usr/bin/env python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import logging
import os
import zipfile
from fnmatch import fnmatch

from sugar3.activity import bundlebuilder

"""
We reimplement the packager, to add to the .xo file the html files
because they are not in git
"""

INCLUDE_DIRS = ['activity', 'html', 'images', 'source', 'locale']

IGNORE_FILES = ['.gitignore', '*.pyc', '*~']


class XOHelpPackager(bundlebuilder.Packager):

    def __init__(self, builder):
        bundlebuilder.Packager.__init__(self, builder.config)

        self.builder = builder
        self.builder.build_locale()
        self.package_path = os.path.join(self.config.dist_dir,
                                         self.config.xo_name)

    def package(self):
        bundle_zip = zipfile.ZipFile(self.package_path, 'w',
                                     zipfile.ZIP_DEFLATED)

        for f in self.list_files('./', True):
            logging.info('Adding %s', f)
            bundle_zip.write(os.path.join(self.config.source_dir, f),
                             os.path.join(self.config.bundle_root_dir, f))

        bundle_zip.close()

    def list_files(self, base_dir, filter_directories=False):
        if filter_directories:
            include_dirs = INCLUDE_DIRS
        else:
            include_dirs = None

        ignore_files = IGNORE_FILES
        result = []

        base_dir = os.path.abspath(base_dir)

        for root, dirs, files in os.walk(base_dir):

            if ignore_files:
                for pattern in ignore_files:
                    files = [f for f in files if not fnmatch(f, pattern)]

            rel_path = root[len(base_dir) + 1:]
            for f in files:
                result.append(os.path.join(rel_path, f))

            if root == base_dir:
                n = 0
                while n < len(dirs):
                    directory = dirs[n]
                    if include_dirs is not None and \
                            not directory in include_dirs:
                        logging.debug("** Ignoring directory %s", directory)
                        dirs.remove(directory)
                    else:
                        n = n + 1
        return result


bundlebuilder.XOPackager = XOHelpPackager


bundlebuilder.start()
