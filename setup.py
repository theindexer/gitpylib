#!/usr/bin/env python

from distutils.core import setup


setup(
    name='gitpylib',
    version='0.1',
    description='A Python library for Git',
    long_description=open('README.md').read(),
    author='Santiago Perez De Rosso',
    author_email='sperezde@csail.mit.edu',
    url='http://github.com/spderosso/gitpylib',
    packages=['gitpylib'],
    license='GPLv2',
    classifiers=(
      'Development Status :: 2 - Pre-Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries',
      'Topic :: Software Development :: Version Control',
      ))
