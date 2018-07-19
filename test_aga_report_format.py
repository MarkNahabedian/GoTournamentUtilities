# Test code for aga_report_format.py.  Assumes the presence of a TDListA.txt
# file contraining the member records of the players listed in test_players.txt.
#
# To run:
#
#   python -m unittest test_aga_report_format.py


import difflib
import filecmp
import os.path
import sys
import unittest
from aga_report_format import *
from aga_roster import AGAMember


class TestRegularExpressions (unittest.TestCase):
  def source_dir(self):
    return os.path.dirname(sys.modules[__name__].__file__)

  def setup(self):
    os.chdir(os.path.join(self.source_dir(), 'test'))
    AGAMember.ensure_loaded()

  # make sure that name_pattern succeeds on every first and last
  # name in the current player roster.
  def test_name_pattern(self):
    self.setup()
    for member in AGAMember.AllMembers:
      self.assertIsNotNone(re.match(name_pattern('NAME'), member.last_name))
      if member.first_name:
        self.assertIsNotNone(re.match(name_pattern('NAME'), member.first_name))

  def test_read_write(self):
    self.setup()
    reference = os.path.join(self.source_dir(), 'test_players.txt')
    result = os.path.join(self.source_dir(), 'test', 'test_players.txt')
    def lines(filename):
      with open(filename, 'r') as f:
        return f.readlines()
    report = AGAReport(reference)
    report.load()
    report.file_name = result
    report.save()
    self.assertTrue(filecmp.cmp(reference, result))
    if not filecmp.cmp(reference, result):
      d = difflib.Differ().compare(lines(reference), lines(result))
      if d:
        for dl in d:
          print(dl)
        self.assertFalse(d)



