
import argparse
import sys
from aga_roster import AGAMember
from aga_report_format import AGAReport
import command_loop

REGISTRATION_FILE = 'players.txt'

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

Once started, registration.py enters a command loop.  Type 'help' for
help.
'''


class ApplicationState(object):
  LISTING_NONE = 0
  LISTING_FOUND = 1
  LISTING_REGISTERED = 2

  def __init__(self, aga_report):
    self.aga_report = aga_report
    self.found = []
    self.last_listing = ApplicationState.LISTING_NONE

  @property
  def registered(self):
    return self.aga_report.players

  def list_found(self):
    sys.stdout.write('\n%d members match the last search:\n' % len(self.found))
    i = 1
    for m in self.found:
      sys.stdout.write('  %3d.  %s\n' % (i, pretty_member(m, True)))
      i += 1
    self.last_listing = ApplicationState.LISTING_FOUND

  def list_players(self):
    sys.stdout.write('\nThere are %d players registered for the tournament:\n' %
                     len(self.registered))
    i = 1
    for m in self.registered:
      sys.stdout.write('  %3d.  %s\n' % (i, pretty_member(m, True)))
      i += 1
    self.last_listing = ApplicationState.LISTING_REGISTERED

  def register(self, member):
    if member in self.registered:
      sys.stderr.write('%s already registered.\n' % pretty_member(member))
    else:
      self.registered.append(member)
      sys.stdout.write('%s registered.\n' % pretty_member(member))

  def unregister(self, member):
    if member not in self.registered:
      sys.stderr.write("%s isn't registered.\n" % pretty_member(member))
    else:
      self.registered.remove(member)
      sys.stdout.write('%s is no longer registered.\n' % pretty_member(member))


def pretty_member(member, listformat=False):
  if listformat:
    return '%6d %s, %s (%s)' % (member.aga_id, member.last_name, member.first_name, member.playing_at.name)
  return '%d %s, %s (%s)' % (member.aga_id, member.last_name, member.first_name, member.playing_at.name)


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
  if state.last_listing != ApplicationState.LISTING_FOUND:
    sys.stderr.write('You need to do a player search first.')
    return
  count = len(state.found)
  if count == 1:
    state.register(state.found[0])
    return
  index = int(match.group('INDEX'))
  if index < 1 or index > count:
    sys.stderr.write('Selection %d is out of range.\n' % index)
    return
  state.register(state.found[index - 1])


@Commands('unregister', 'unr(?P<INDEX>[0-9]*)')
def unregister(match, state, **ignore):
  if state.last_listing != ApplicationState.LISTING_REGISTERED:
    sys.stderr.write('First use the "who" command to list the players who are registered.')
    return
  count = len(state.registered)
  index = int(match.group('INDEX'))
  if index < 1 or index > count:
    sys.stderr.write('Selection %d is out of range.\n' % index)
    return
  state.unregister(state.registered[index - 1])


@Commands('who', 'who')
def who_is_playing(state, **ignore):
  '''Lists those who are registered for the tournament.'''
  state.list_players()


@Commands('save', 'save')
def save_registration(state, **ignore):
  '''Save the state of registration to a file.'''
  state.aga_report.save()
  sys.stdout.write('Wrote %s.\n' % state.aga_report.file_name)


@Commands('reload', 'reload')
def reload_saved_file(state, **ignore):
  state.aga_report.load()


def main():
  args = parser.parse_args()
  AGAMember.ensure_loaded()
  aga_report = AGAReport(REGISTRATION_FILE)
  aga_report.load()
  state = ApplicationState(aga_report)
  Commands.command_loop(state)
  aga_report.save()


if __name__ == '__main__':
    main()
