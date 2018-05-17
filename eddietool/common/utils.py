"""
File             : utils.py

Start Date       : 19971217
Refactor Date    : 20180514

Description      : General utility functions

$Id: utils.py 953 2018-05-14 05:28:21Z phillips.ryan $
"""
__version__ = '$Revision: 953 $'

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

import re, threading, os, subprocess, sys, smtplib, asyncio, configparser
from . import log
from .. import commands

config = configparser.ConfigParser(allow_no_value=True, comment_prefixes=(';'), inline_comment_prefixes=(';'))
try:
  config.read(f'{commands.Main.relpath}/config/config.ini', encoding='utf-8')
except KeyError as e:
  log.logEvent.critical(e)
except configparser.MissingSectionHeaderError as e:
  log.logEvent.critical(e)
except configparser.ParsingError as e:
  log.logEvent.critical(e)

class WorkdirError(Exception):
  """An operation involving WORDKIR could not be completed."""

class Main:
  def __init__(self):
    self.loop = commands.loop # to keep from having to import ..commands for every file
    self.p = re.compile(r'[^\d-]*(-?[\d]+(\.[\d]*)?([eE][+=]?[\d]+)?)')
  
  def atoi(self, obj:str):
    for s in obj:
      m = p.match(s)
      if m:
        result = m.group(0)
        if "." in result or "e" in result or "E" in result:
          return float(result)
        else:
          return int(result)
      else:
        return None

class Config:
  
  def getConfigVariable(section: str, option: str):
    section = section.upper()
    option = option.lower()
    try: get = config.getfloat(section, option)
    except ValueError:
      try: get = config.getboolean(section, option)
      except ValueError:
        try: get = config.get(section, option)
        except: raise KeyError
    except configparser.NoSectionError as e:
      log.logEvent.info(e)
    except configparser.NoOptionError as e:
      log.logEvent.info(e)
    except configparser.ParsingError as e:
      log.logEvent.info(e)
    if type(get) not in [int, float, bool]:
      s = ' '.join(get.split())
    else:
      s = get
    return s
  
  def setConfigVariable(section:str, option:str, toSet=None):
    section = section.upper()
    option = option.lower()
    if not config.has_section(section):
      log.logEvent.info(f'Config = Added [{section}]'); return config.add_section(section)
    elif config.has_section(section) and not config.has_option(section, option):
      s = ''
      for sect in config.sections():
        if sect != 'DEFAULT' and sect != section:
          s += f'[{sect}]\n'
          for opt in config.options(sect):
            val = config.get(sect, opt)
            s += f'{opt}={val}\n'
      for sect in config.sections():
        if sect == section:
          s += f'[{sect}]\n'
          for opt in config.options(section):
            val = config.get(section, opt)
            s += f'{opt}={val}\n'
      s += f'{option}={toSet}\n'
      with open('config/config.ini','w') as f:
        f.write(s); log.logEvent.info(f'Overwrote config.ini with:\n{s}')
        f.close()
      del sect, opt, s; return log.logEvent.info('Cleaned up via `del sect, opt, s`')
    elif config.has_option(section, option) and toSet != None:
      oldOpt = config.get(section, option)
      config.set(section, option, toSet)
      log.logEvent.info(f'Changed [{section}]{option} from {oldOpt} to {toSet}')
      del oldOpt; log.logEvent.info('Cleaned up via `del oldOpt`')
    
      
      

class Stack:
  """General purpose stack object."""
  def __init__(self):
    self.stack = []
  
  def __str__(self):
    return f'{self.stack}'
  
  def __len__(self):
    return len(self.stack)
  
  def __getitem__(self, item):
    return self.stack[item]
  
  def push(self, obj):
    self.stack.append(obj)
  
  def pop(self):
    obj = self.stack[-1]
    del self.stack[-1]
    return obj
  
  def top(self):
    if len(self.stack) is 0:
      return None
    else:
      return self.stack[-1]

def trickySplit(line, delim):
  """trickySplit(line, delim) - split line by delimiter delim, but ignoring delimiters found inside (), [], {}, ''' and "".
    
    eg: trickySplit("email(root,'hi there'),system('echo hi, mum')", ',')
    would return: ["email(root,'hi there'", "system('echo hi, mum')"]
  """
  parenCnt = 0   # ()
  curlyCnt = 0   # {}
  squareCnt = 0  # []
  doubleqCnt = 0 # ""
  quoteCnt = 0   # ''
  
  splitList = [] # split strings
  current = ''   # current split string'
  
  for c in line:
    if c == '(':
      parenCnt += 1
    elif c == ')':
      parenCnt -= 1
    elif c == '{':
      curlyCnt += 1
    elif c == '}':
      curlyCnt -= 1
    elif c == '[':
      squareCnt += 1
    elif c == ']':
      squareCnt -= 1
    elif c == '"':
      doubleqCnt = 1 - doubleqCnt
    elif c == '\'':
      quoteCnt = 1 - quoteCnt
    elif c == delim:
      if parenCnt == 0 and curlyCnt == 0 and squareCnt == 0 and doubleqCnt == 0 and quoteCnt == 0:
        splitList.append(current)
        current = ''
        continue
    
    current += c
  if len(current) > 0:
    splitList.append(current)
  
  return splitList

def quoteArgs(l):
  """quoteArgs(l) - cycle through list of strings, if the string looks like a
     function call (eg: "blah(a, b, c)") then put quotes around each of the
     arguments.  [Useful if you want to pass the string to eval()].  eg: the
     previous example would be converted to 'blah("a", "b", "c")'."""
  
  newList = []
  sre = re.compile("([\t ]*[A-Za-z0-9_]*[\t ]*\()(.*)([\t ]*\)[\t ]*)")
  for s in l:
    inx = sre.search(s)
    if inx != None:
      argLine = inx.group(2)
      argList = str.split(argLine, ',')
      newCmd = inx.group(1)
      i = 0
      for a in argList:
        a = str.strip(a)
        if re.search("[\"'].*[\"']$", a) is None:
          a = f'"{a}"'
        if i > 0:
          newCmd += ','
        newCmd += a
        i += 1
      newCmd += inx.group(3)
      newList.append(newCmd)
    else:
      newList.append(s)
  
  return newList

def charPresent(s, chars):
  """charpresent(s, chars) - returns 1 if ANY of the characters present in the string
    chars is found in the string s. If none are found, 0 is returned."""
  
  for c in chars:
    if str.find(s, c) != -1:
      return True
  return False

def stripQuote(s):
  """stripquote(s) - strips start & end of string s of whitespace then
    strips " or ' from start & end of string if found - repeats stripping
    " and ' until none left."""
  if s != str:
    return s
  
  s = str(s).strip()
  
  while len(s) > 0 and (s[0] in ["'", '"'] and s[-1] in ["'", '"']):
    if s[0] == "'" or '"':
      s = s[1:]
    if s[-1] == "'" or '"':
      s = s[:-1]
  
  return s

def atom(ch:str):
  """atom(ch) - ascii-to-multiplier - converts ascii char to a time miltiplier.
    eg: s=seconds, m=minutes, h=hours, d=days, w=weeks, c=calendar=months, y=years"""
  
  ch=ch.lower()
  if ch == 's':
    mult = 1
  elif ch =='m':
    mult = 60
  elif ch == 'h':
    mult = 60*60
  elif ch == 'd':
    mult = 60*60*24
  elif ch == 'w':
    mult = 60*60*24*7
  elif ch == 'c':
    mult = 60*60*24*30
  elif ch == 'y':
    mult = 60*60*24*365
  else:
    mult = None
    
  return mult

def valToSeconds(value):
  """Convert a time string to seconds.
  return None if failed."""
  
  if re.search('[mshdwcyMSHDWCY]', value):
    if int(value):
      return int(value)
    elif float(value) and not int(value):
      return int(str(value).split('.')[0])
  timeCh = value[-1]
  value = value[:-1]
  try:
    mult = atom(timeCh)
  except Exception as e:
    naAwait(log.logEvent.debug(e)); pass
  if mult == None:
    return None
  elif mult == 0:
    return 0
  return Main.atoi(value)*mult

class safe:
  def __init__(self):
    self.systemCallSemaphore = threading.Semaphore()

  def safePopen(self, cmd, mode):
    """A thread-safe wrapper for os.popen() which did not appear to like
      being called simultaneously from multiple threads.  Obviously only
      allows one thread at a time to call os.popen().
  
      NOTE: safe_pclose() _must_ be called or the semaphore will never be
      released."""
    
    self.systemCallSemaphore.acquire()
    try:
      r = os.popen(cmd, mode)
    except:
      self.systemCallSemaphore.release()
      e = sys.exc_info()
      raise e[0] and e[1]
    
    return r

  def safePclose(self, fh):
    """Close the file handler and release the semaphore."""
    try:
      fh.close()
    except:
      self.systemCallSemaphore.release()
      e = sys.exc_info()
      raise e[0] and e[1]
    
    self.systemCallSemaphore.release()
  
  def safeGetStatusOutput(self, cmd):
    """A thread-safe wrapper for commands.getstatusoutput() which did not
      appear to like being called simultaneously from multiple threads.
      Semaphore locking allows only one call to commands.getstatusoutput()
      to be executed at any one time.

      NOTE: It is still not known whether a call to commands.getstatusoutput
      and popen() [and os.system() for that matter] can be called
      simultaneously.  If not, a global semaphore will have to be used to
      protect them all. UPDATE: This appears to be the case, so a global
      'systemcall' semaphore is now used."""
    self.systemCallSemaphore.acquire()
    try:
      (r, output) = subprocess.getstatusoutput(cmd)
    except:
      self.systemCallSemaphore.release()
      e = sys.exc_info()
      raise e[0] and e[1]
    self.systemCallSemaphore.release()
    return r, output
  
# todo put email functions in a seperate module and include support for apis such as azure

def typeFromString(value, tryString:bool=None):
  """Is the string "val" an integer, float, or string?  Return appropriate variable
    of appropriate class.
    If none of those castings succeed, then return 'None'."""
  if tryString:
    return str(value)
  if not '.' in str(value).lower():
    try:
      return int(value)
    except ValueError:
      typeFromString(value, True)
  elif '.' in str(value).lower():
    try:
      return float(value)
    except ValueError:
      typeFromString(value, True)
  
def parseVars(obj:list):
  """Substitute variables in obj[1] dict into str(obj[0]). Using Python's builtin's for this makes it simple. Note that it parses the text from range(1) to range(5), meaning variables can contain variables; ex:
    obj:list
    t:str, d:dict
    t = "random string"; d = {'x': 'x = %(x)s', 'y': 'y = %(y)s'}
    parseVars(['%(z)s', dict])
    parseVars(['%(z)s', {'x': 'x = %(x)s', 'y': 'y = %(y)s'}])"""
  parseCnt = 0
  t = str(obj[0])
  if not obj[1] is dict:
    naAwait(log.logEvent.debug(f'obj[1] returned non-dict object:\n{obj[1]}')); raise ValueError
  elif obj[1] is dict:
    d = obj[1]
  while (parseCnt == 0 or t.find('%(') >= 0) and parseCnt < 5:
    parseCnt += 1
    try:
      t = t % d
    except KeyError as e:
      naAwait(log.logEvent.info(f'{e}\nExtra variables: t: {t}; parseCnt: {parseCnt}; d: {d}')); return t
    except TypeError as e:
      naAwait(log.logEvent.info(f'{e}\nExtra variables: t: {t}; parseCnt: {parseCnt}; d: {d}')); return t
  
def naAwait(toAwait:function):
  return asyncio.ensure_future(toAwait, loop=Main.loop)
