# Test code fior aga_roster.py.  Assumes the presence of a TDListA.txt
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
  def ensure_loaded(self):
    os.chdir(os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'test'))
    try:
      AGAMember.read_member_file()
    except AGAMembersAlreadyLoaded:
      pass

  def test_read(self):
    self.ensure_loaded()
    # Expect a reasonable number of records read:
    self.assertGreaterEqual(len(AGAMember.AllMembers), 2000)

  def test_id_lookup(self):
    self.ensure_loaded()
    m = AGAMember.lookupID(AGA_ID)
    self.assertNotEqual(m, None)
    self.assertEqual(FIRST_NAME, m.first_name)
    self.assertEqual(LAST_NAME, m.last_name)

  def test_substring_lookup(self):
    self.ensure_loaded()
    found = AGAMember.search('ahabed')
    self.assertEqual(len(found), 1)
    m = found[0]
    self.assertNotEqual(m, None)
    self.assertEqual(FIRST_NAME, m.first_name)
    self.assertEqual(LAST_NAME, m.last_name)


if __name__ == '__main__':
    unittest.main()
