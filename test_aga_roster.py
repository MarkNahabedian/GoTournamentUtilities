# Test code for aga_roster.py.  Assumes the presence of a TDListA.txt
# file contraining the member record of the author.
#
# To run:
#
#   python -m unittest test_aga_roster.py

import os
import os.path
import sys
import unittest
from aga_roster import AGAMember, AGAMembersAlreadyLoaded


FIRST_NAME = "Mark"
LAST_NAME = "Nahabedian"
AGA_ID = 7068


class TestAGARoster(unittest.TestCase):
  def setup(self):
    os.chdir(os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'test'))
    AGAMember.ensure_loaded()

  def test_read(self):
    self.setup()
    # Expect a reasonable number of records read:
    self.assertGreaterEqual(len(AGAMember.AllMembers), 2000)

  def test_id_lookup(self):
    self.setup()
    m = AGAMember.lookupID(AGA_ID)
    self.assertNotEqual(m, None)
    self.assertEqual(FIRST_NAME, m.first_name)
    self.assertEqual(LAST_NAME, m.last_name)

  def test_substring_lookup(self):
    self.setup()
    found = AGAMember.search('ahabed')
    self.assertEqual(len(found), 1)
    m = found[0]
    self.assertNotEqual(m, None)
    self.assertEqual(FIRST_NAME, m.first_name)
    self.assertEqual(LAST_NAME, m.last_name)

  def test_highest_rank(self):
    max = -1000
    min = 1000
    for member in AGAMember.AllMembers:
      if member.rating:
        if member.rating > max:
          max = member.rating
        if member.rating < min:
          min = member.rating
    self.assertLess(max, 10)
    self.assertGreaterEqual(min, -30)

if __name__ == '__main__':
    unittest.main()
