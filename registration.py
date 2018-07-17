
import argparse
import sys
from aga_roster import AGAMember
import command_loop

REGISTRATION_FILE = 'registered.tsv'

parser = argparse.ArgumentParser()

parser.usage = '''

registration.py is a terminal based interactive program to create the
list of players in a Go tournament.

All of the files associated with a tournament are kept in a file
system diorectory that was created for that purpose.  registration.py
should be run with that directory as the current working directory.

registration.py depends on the AGA membership file TDListA.txt being
present in that directory.  If it's not there it will be downloaded.
An internet connection is required in this case.

Once started, registration.py enters a command loop.  Type '?' for
help.
'''


class ApplicationState(object):
  def __init__(self):
    self.found = []
    self.registered = []

  def list_found(self):
    sys.stdout.write('\n%d members match the last search:\n' % len(self.found))
    i = 1
    for m in self.found:
      sys.stdout.write('  %3d.  %s\n' % (i, pretty_member(m, True)))
      i += 1

  def register(self, member):
    if member in self.registered:
      sys.stderr.write('%s already registered.\n' % pretty_member(member))
    else:
      self.registered.append(member)
      sys.stdout.write('%s registered.\n' % pretty_member(member))


def pretty_member(member, listformat=False):
  if listformat:
    return '%6d %s, %s' % (member.aga_id, member.last_name, member.first_name)
  return '%d %s, %s' % (member.aga_id, member.last_name, member.first_name)


Commands = command_loop.CommandTable()

Commands.add_command(command_loop.EXIT_COMMAND)
Commands.add_command(command_loop.HELP_COMMAND)


@Commands('lookup', '[?](?P<AGA_ID>[0-9]+)')
def id_lookup_action(match, state, **ignore):
  '''Find the AGA member with the specified ID number.'''
  id = int(match.group('AGA_ID'))
  member = AGAMember.lookupID(id)
  if member:
    state.found = [member]
    state.list_found()
  else:
    sys.stderr.write('No member with AGA id %d found.\n' % id)
  

@Commands('lookup', '[?](?P<SUBSTRING>[A-Za-z -]+)')
def name_search_action(match, state, **ignore):
  '''Find AGA members whose first or last name contains the specified substring.'''
  substring = match.group('SUBSTRING')
  members = AGAMember.search(substring)
  if members:
    state.found = members
    state.list_found()
  else:
    sys.stderr.write('No members have names matching %s.\n' % substring)


@Commands('found', 'found')
def list_found(state, **ignore):
  '''Show the most recent search results.'''
  state.list_found()


@Commands('register', 'r(?P<INDEX>[0-9]*)')
def register(match, state, **ignore):
  '''Register a player from among the most recent search results.'''
  count = len(state.found)
  if count == 1:
    state.register(state.found[0])
    return
  index = int(match.group('INDEX'))
  if index < 1 or index > count:
    sys.stderr.write('Selection %d is out of range.\n' % count)
    return
  state.register(state.found[index - 1])


def main():
  args = parser.parse_args()
  AGAMember.ensure_loaded()
  Commands.command_loop(ApplicationState())


if __name__ == '__main__':
    main()
