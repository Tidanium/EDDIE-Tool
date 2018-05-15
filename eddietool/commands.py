"""
File             : commands.py

Start Date       : 20080513
Refactor Date    : 20180514

Description      : Eddie-Tool command-line entry points.

$Id: commands.py 953 2018-05-14 04:57:27Z phillips.ryan $
"""
__copyright__ = 'Copyright (c) Ryan Phillips 2018'

__author__ = 'Chris Miles'
__author_email__ = 'miles.chris@gmail.com'

__maintainer__ = 'Ryan Phillips aka Tidanium'
__maintainer_email__ = 'ryan@ryanphillips.org'

__url__ = 'https://github.com/Tidanium/EDDIE-Tool'
__license__ = """
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# todo will work on this more after the rest of the content it relies on
from .version import version as __version__

import sys, os, time, signal, re, threading, asyncio

from .common import utils, log
loop = asyncio.get_event_loop()
class Main:
  def __init__(self):
    self.relpath = os.path.relpath('.', '/')