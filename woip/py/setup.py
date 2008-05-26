# Copyright (C) 2007, One Laptop Per Child
#
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

from distutils.core import setup, Extension

wp_sources = [
    'wp.i',
    '../c/bzipreader.c',
    '../c/wp.c',
    '../c/lsearcher.c',
    '../c/safe.c',
    '../c/blocks.c'
]

wp_module = Extension(
    '_wp',
    sources=wp_sources,
    include_dirs=['../c'],
    define_macros=[('DEBUG', 1)],
    libraries=['bz2'])

setup(name='wp', version='0.1', 
      author='Wade Brainerd', 
      description="""Offline Wikipedia Interface.""", 
      ext_modules=[wp_module], py_modules=['wp'])
