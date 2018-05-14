'''
File             : ack.py

Start Date       : 20000124
Refactor Date    : 20180514

Description      : Acknowledgement objects to track problem acknowledgements.

$Id: ack.py 953 2018-05-14 05:00:08Z phillips.ryan $
'''
__version__ = '$Revision: 953 $'

__copyright__ = 'Copyright (c) Ryan Phillips 2018'

__author__ = 'Chris Miles'
__author_email__ = 'miles.chris@gmail.com'

__maintainer__ = 'Ryan Phillips aka Tidanium'
__maintainer_email__ = 'ryan@ryanphillips.org'
__refactor_note__ = 'I have no clue what this is for, personally'

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

import time

class ack:
  """The ack(nowledgement) class to keep state of last acknowledgement."""
  def __init__(self):
    self.state = 'n'
    self.time = None
    self.user = None
    self.details = None
    self.clear()
    
  def clear(self):
    """Clear all acknowledgement information."""
    self.state = 'n'
    self.time = None
    self.user = None
    self.details = None
  
  def set(self, user=None, details=None):
    """Set a user acknowledgement."""
    self.clear()
    
    self.state = 'y'
    self.time = time.localtime(time.time())
    self.user = user
    self.details = details
