# Model of the AGA's tournament and rated game reporting format.

import datetime
import re
from rank import Rank
from file_line_reader import FileLineReader
from aga_roster import AGAMember
from tournament import Tournament


class FileFormatError (Exception):
  def __init__(self, input, line_number, line, message):
    self.file_name = input.name
    self.line_number = line_number
    self.line = line
    self.message = message
  def __str__(self):
    return '%s %d: %s' % (self.file_name, self.line_number, self.message)


def aga_id_pattern(name):
  return '(?P<%s>[0-9]+)' % name

def name_pattern(name):
  return '(?P<%s>[a-zA-Z.]+)' % name

def names_pattern(name):
  return '(?P<%s>[a-zA-Z. ]+)' % name

def whitespace_pattern():
  return '''\s+'''

def opt_comma_pattern(name='COMMA'):
  return '(?P<COMMA>,?)'

def rank_pattern(name='RANK'):
  return '(?P<%s>[0-9]+[KDP])' % name

def winner_pattern(name='WINNER'):
  return '(?P<%s>[wb])' % name

def handicap_pattern(name='HANDICAP'):
  return '(?P<%s>[0-9])' % name

def komi_pattern(name='KOMI'):
  return '(?P<%s>-?[0-9]+)' % name

PLAYER_RECORD_FMT = '%(AGA_ID)6d %(LAST_NAME)s, %(FIRST_NAME)s %(RANK)s'

PLAYER_RECORD_RE = re.compile(
    aga_id_pattern('AGA_ID') +
    whitespace_pattern() +
    name_pattern('NAME1') +
    opt_comma_pattern() +
    whitespace_pattern() +
    names_pattern('NAME2') +
    whitespace_pattern() +
    rank_pattern())

PAIRING_RECORD = re.compile(
    aga_id_pattern('WHITE_ID') +
    whitespace_pattern() +
    aga_id_pattern('BLACK_ID'))

RESULT_RECORD = re.compile(
    aga_id_pattern('WHITE_ID') +
    whitespace_pattern() +
    aga_id_pattern('BLACK_ID') +
    whitespace_pattern() +
    winner_pattern() +
    handicap_pattern() +
    whitespace_pattern() +
    komi_pattern())

# For players taking a by
PASS_RECORD = re.compile(
    'PASSED:' +
    whitespace_pattern() +
    aga_id_pattern('AGA_ID'))

# Section headers

SH_TOURNAMENT = 'TOURNEY'
SH_TOURNAMENT_RE = re.compile(SH_TOURNAMENT, re.IGNORECASE)

SH_PLAYERS = 'PLAYERS'
SH_PLAYERS_RE = re.compile(SH_PLAYERS, re.IGNORECASE)

SH_GAMES = 'GAMES'
SH_GAMES_RE = re.compile(SH_GAMES, re.IGNORECASE)


# e.g. 6/30/2004
REPORT_DATE_FORMAT = '%m/%d/%Y'


def write_tournament_header(output, tournament):
  assert isinstance(tournament, Tournament), 'Gt %r' % tournament
  output.write('%s %s\n' % (SH_TOURNAMENT, tournament.description))
  output.write('\tstart=%s\n' % tournament.start_date.strftime(REPORT_DATE_FORMAT))
  output.write('\tfinish=%s\n' % tournament.end_date.strftime(REPORT_DATE_FORMAT))
  output.write('rules=%s\n' % tournament.rules)
  output.write('\n')


def read_tournament_header_string(input):
  '''For reading and writiing the player roster, pairings and resukts, we
     donlt need to parse the tournament section.'''
  assert isinstance(input, FileLineReader), 'Got %r' % input
  lines = []
  line = input.readline()
  if not SH_TOURNAMENT_RE.search(line):
    raise FileFormatError(input, input.line_number, line, 'Expected line to start with %s' % SH_TOURNAMENT)
  while True:
    line = input.readline()
    if line == '\n':
      break
    lines.append(line)
  return ''.join(lines)


def skip_empty_lines(input):
  assert isinstance(input, FileLineReader), 'Got %r' % input
  while True:
    line = input.readline()
    if line == '':
      break
    if not line.strip() == '':
      input.unreadline(line)
      break


def write_players_section(output, players):
  output.write('%s\n' % SH_PLAYERS)
  for p in players:
    # We could use PLAYER_RECORD_RE but we want the AGA id to be space padded.
    output.write(PLAYER_RECORD_FMT % {
        'AGA_ID': p.aga_id,
        'LAST_NAME': p.last_name,
        'FIRST_NAME': p.first_name,
        'RANK': p.playing_at.name
        } + '\n')
  output.write('\n')


def read_players(input):
  '''Reads the PLAYERS section of input and returns a list of player dicts.'''
  assert isinstance(input, FileLineReader) ,'Got %r' % input
  players = []
  skip_empty_lines(input)
  line = input.readline()
  if not SH_PLAYERS_RE.search(line):
    raise FileFormatError(input, input.line_number, line, 'Expected %s line.' % SH_PLAYERS)
  while True:
    line = input.readline()
    if line == '\n':
      break
    m = PLAYER_RECORD_RE.search(line)
    if not m:
      raise FileFormatError(input, input.line_number, line, 'malformed player line.')
    aga_id = int(m.group('AGA_ID'))
    rank = Rank[m.group('RANK')]
    player = AGAMember.lookupID(aga_id)
    if ',' in m.group('COMMA'):
      first_name = m.group('NAME2')
      last_name = m.group('NAME1')
    else:
      last_name = m.group('NAME1')
      first_name = m.group('NAME2')
    if not player:
      player = AGAMember(last_name, first_name, aga_id, None, None, None)
    else:
      if player.last_name != last_name:
        raise Exception("For AGA member %d, last names don't match: %s versus %s." %
                        (aga_id, last_name, player.last_name))
    player.play_at(rank)
    players.append(player)
  return players


class AGAReport (object):
  def __init__(self, file_name):
    self.file_name = file_name
    self.tournament_header = None
    self.players = []
    self.pairings = []
    self.games = []

  def load(self):
    try:
      with FileLineReader(self.file_name) as input:
        self.tournament_header = read_tournament_header_string(input)
        self.players = read_players(input)
    except FileNotFoundError:
      pass

  def save(self):
    with open(self.file_name, 'w') as output:
      output.write('%s\n%s\n' % (SH_TOURNAMENT, self.tournament_header))
      write_players_section(output, self.players)
      output.write('\n')
