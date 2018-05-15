"""
File             : config.py

Start Date       : 19971211
Refactor Date    : 20180515

Description      : Eddie software config

$Id: config.py 954 2018-05-14 18:16:38Z phillips.ryan $
"""
__version__ = '$Revision: 954 $'

__copyright__ = 'Copyright (c) Ryan Phillips 2018'

__author__ = 'Chris Miles; Rod Telford'
__author_email__ = 'miles.chris@gmail.com; '

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

import sys, os, configparser, re
from . import log, utils
from ..commands import Main

class ParseFailure(Exception):
  pass



if utils.Config.getConfigVariable('.config', 'rescanconfig') is True:
  scanPeriod = utils.valToSeconds(getConfigVariable('.config', 'scanperiod'))
else:
  scanPeriod = False

class Config:
  """The main Eddie configuration class."""
  def __init__(self, name:str, parent=None):
    self.name = utils.Config.getConfigVariable('.config', 'name')
    if len(name) < 1:
      raise SyntaxError
    self.type = utils.Config.getConfigVariable('.config', 'type')
    self.display = utils.Config.getConfigVariable('.config', 'displayedconfigonce?')
    
    self.groupDirectives = {}
    self.MDict = definition.MsgDict()
    if parent != None:
      self.MDict.update(parent.MDict)
      
    self.aliasDict = {}
    self.NDict = {}
    self.classDict  = {}
    
    self.groups = []
    self.configfiles = {
      "mainconfig": f"{Main.relpath}/config/config.ini",
      "dictconfig": f"{Main.relpath}/config/config.json",
      "gitconfig": f"{Main.relpath}/config/gitconfig.ini"
    }
    self.parent = parent
    if parent != None:
      self.aliasDict.update(parent.aliasDict)
      self.NDict.update(parent.NDict)
    
  def __str__(self):
    s = f"<Config name='{self.name}' type='{self.type}'"
    s +=f"\n groupDirectives: {self.groupDirectives}"
    s +=f"\n groups:          {', '.join([i for i in self.groups])}"
    s +=f"\n MDict:           {', '.join([i for i in self.MDict])}"
    s +=f"\n aliasDict:       {self.aliasDict}"
    s +=f"\n NDict:           {', '.join([i for i in self.NDict])}"
    s +=f"\n classDict:       {self.classDict}"
    s += "\nConfig end>"
    return s
