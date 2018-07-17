# A library for applications that provide simple interactive text
# based interfaces.

import re
import sys


class CommandTable (object):
  def __init__(self, prompt=None):
    self.commands = []
    self.prompt = prompt if prompt else '> '

  def __call__(self, command_name, command_regular_expression):
    '''CommandTable can serve as a decorator for definiing commands.'''
    def finish_command(action_function):
      cmd = Command(command_name, command_regular_expression,
                    action_function.__doc__, action_function)
      self.commands.append(cmd)
      return cmd
    return finish_command

  def command_loop(self, state=None):
    '''Loop, reading commands from the terminal and executing them.
       The CommandTable itself, the re match results and state are
       passed to each command.'''
    try:
      while True:
        sys.stdout.write(self.prompt)
        sys.stdout.flush()
        input = sys.stdin.readline().strip()
        if not input:
          continue
        done = False
        for c in self.commands:
          m = c.match(input)
          if m:
            c.doit(self, m, state)
            done = True
            break
        if not done:
          sys.stderr.write('Command not found.\n')
        sys.stdout.flush()
        sys.stderr.flush()
      
    except Exit:
      pass

  def add_command(self, command):
    self.commands.append(command)

  def help(self, match):
    for c in self.commands:
      print('  %s: %s  %s' % (c.name, c.regexp.pattern, c.description))


class Command (object):
  '''Command associates a regular expression with an action function to
     be called if the regular expression matches the input line.
     Command can be used as a decorator for defining new commands.'''

  AllCommands = []

  def __init__(self, name, regexp, description, action):
    if isinstance(regexp, str):
      regexp = re.compile(regexp)
    self.name = name
    self.regexp = regexp
    self.description = description
    self.action = action
    self.__class__.AllCommands.append(self)

  def match(self, command_input):
    return self.regexp.fullmatch(command_input)

  def doit(self, command_table, match, state):
    self.action(command_table=command_table, match=match, state=state)


class Exit (Exception):
  def __str__():
    return 'Exit command loop'


COMMON_COMMANDS = CommandTable()

@COMMON_COMMANDS('exit', re.compile('exit', re.IGNORECASE))
def EXIT_COMMAND(**ignore):
  '''Exit the command loop.'''
  raise Exit()


@COMMON_COMMANDS('help', re.compile('help', re.IGNORECASE))
def HELP_COMMAND(command_table, match, **ignore):
  '''Show command help.'''
  command_table.help(match)

