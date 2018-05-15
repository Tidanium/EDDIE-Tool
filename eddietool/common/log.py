"""
File             : log.py

Start Date       : 19980107
Refactor Date    : 20180515

Description      : Eddie software logging components

$Id: log.py 954 2018-05-14 17:56:36Z phillips.ryan $
"""
__version__ = '$Revision: 954 $'

__copyright__ = 'Copyright (c) Ryan Phillips 2018'

__author__ = 'Chris Miles'
__author_email__ = 'miles.chris@gmail.com'

__maintainer__ = 'Ryan Phillips aka Tidanium'
__maintainer_email__ = 'ryan@ryanphillips.org'

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

import logging, asyncio
from . import config, utils
def log():
  name = utils.Config.getConfigVariable('logging','name') if utils.Config.getConfigVariable('logging', 'logfilename') == '' else name = utils.Config.getConfigVariable('logging', 'logfilename')
  logger = logging.getLogger(name)
  logger.setLevel(utils.Config.getConfigVariable('logging', ''))

class logEvent:
  
  def critical(self, msg, *args, **kwargs):
    return logging.critical(msg, *args, **kwargs)
  
  def debug(self, msg, *args, **kwargs):
    return logging.debug(msg, *args, **kwargs)
  
  def error(self, msg, *args, **kwargs):
    return logging.error(msg, *args, **kwargs)
  
  def info(self, msg, *args, **kwargs):
    return logging.info(msg, *args, **kwargs)

  def warning(self, msg, *args, **kwargs):
    return logging.warning(msg, *args, **kwargs)
  