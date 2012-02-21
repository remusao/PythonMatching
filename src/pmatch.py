#################################################################################
#
#  PythonMatching is a Python3 module that allows an Ocaml-like pattern matching
#  on Python structures.
#
#  Copyright (C) 2011-2012  Remi BERSON
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##################################################################################


import re
from functools import reduce


class Match():
  """
    Object able to match structural patterns
  """

  def __init__(self, *r):
    """
      Init a Match objet by giving an arbitrary number of
      couple (pattern, action) to the constructor
    """
    self.special = [re.compile('.*::.*'), re.compile('_.*_')]
    self.rules = []
    self.env = {'rec' : self, 'self' : self}
    if len(r) % 2:
      raise NameError('Invalid rules')
    for i in range(0, len(r), 2):
      self.rules.append((r[i], r[i + 1]))


  def is_special(self, pattern):
    """
      Check if the pattern is a special one :
        - h::t
        - _var_
    """
    for index, exp in enumerate(self.special):
      if exp.match(pattern):
        return index
    return -1


  def list_dec(self, l, pattern):
    """
      Treats the h::t pattern, put the first element of l in h
      and the rest in h
    """
    tmp_vars = pattern.split('::')
    if not l:
      for x in tmp_vars:
        self.env[x] = []
      return False
    elif isinstance(l, dict):
      l = l.items()
    elif isinstance(l, set):
      l = list(l)
      
    self.env['tmp'] = l
    if len(l) < len(tmp_vars):
      for x in tmp_vars[len(l):]:
        self.env[x] = []
      tmp_vars = tmp_vars[:len(l)]
      if len(tmp_vars) == 1:
        exec(str(tmp_vars[0]) + ' = tmp[0]', self.env)
      else:
        exec(', '.join(tmp_vars[:-1]) + ', *' + tmp_vars[-1] + ' = tmp', self.env)
    else:
      exec(', '.join(tmp_vars[:-1]) + ', *' + tmp_vars[-1] + ' = tmp', self.env)
    return True


  def var_assign(self, to_match, pattern):
    """
      assign 'to_match' to the var 'pattern' in self.env
    """
    self.env[pattern] = to_match
    return True


  def match_it(self, to_match, pattern):
    """
      Will parse recursively to_match and pattern and call self.match
      on their items.
    """
    res = True
    if isinstance(to_match, list) or isinstance(to_match, tuple):
      for line, elt in enumerate(to_match):
        res = res and self.match(elt, pattern[line])
    elif isinstance(to_match, dict):
      for x in to_match:
        if x in pattern:
          res = res and self.match(to_match[x], pattern[x])
        else:
          return False
    elif isinstance(to_match, set):
      return True
    return res


  def match(self, to_match, pattern):
    """
      Match recursively the two var to_match and pattern
    """
    # Check if the pattern is a var, a h::t pattern or a regexp
    if isinstance(pattern, str):
      if pattern == '_':
        return True
      tmp = self.is_special(pattern)
      if tmp == 0: # h::t pattern
        if getattr(to_match, '__iter__', False):
          return self.list_dec(to_match, pattern)
        else:
          return False
      elif tmp == 1: # _var_ pattern
        return self.var_assign(to_match, pattern)
      return to_match == pattern

    # Check if to_match and pattern are iterable
    elif getattr(pattern, '__iter__', False) and getattr(to_match, '__iter__', False):
      # Check if they have the same type and the same len
      if type(pattern) == type(to_match):
        if len(pattern) == len(to_match):
          if len(pattern) != 0:
            return self.match_it(to_match, pattern)
          else:
            return True
        else:
          return False
      else:
        return False

    return pattern == to_match


  def __call__(self, to_match):
    """
      Will try to match the argument 'to_match' with each rule
      given at the init of the Match object, and run the 'action'
      code given if one rule matches.
    """
    self.result = None
    for pattern, action in self.rules:
      if self.match(to_match, pattern):
        try:
          self.result = eval(action, self.env)
        except:
          try:
            exec(action, self.env)
          except:
            print('Unable to run the given action :', action)
        return self.result

    print('Pattern Matching is not exaustive')
    return self.result
