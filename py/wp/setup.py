from distutils.core import setup, Extension

wp_sources = [
    'wp.i',
    '../../c/bzipreader.c',
    '../../c/wp.c',
    '../../c/lsearcher.c',
    '../../c/safe.c',
    '../../c/blocks.c'
]

wp_module = Extension(
    '_wp',
    sources=wp_sources,
    include_dirs=['../../c'],
    define_macros=[('DEBUG', 1)],
    libraries=['bz2'])

setup(name='wp', version='0.1', 
      author='Wade Brainerd', 
      description="""Offline Wikipedia Interface.""", 
      ext_modules=[wp_module], py_modules=['wp'])
