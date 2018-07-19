

class FileLineReader (object):
  '''We use FileLineReader to read a file line by line while tracling the current line number.'''
  def __init__(self, filename):
    self.filename = filename
    self.line_number = None
    self.file = None
    self.unread = None

  def __enter__(self):
    self.file = open(self.filename, 'r')
    self.line_number = 0
    return self

  def __exit__(self, *exc):
    self.file.close()
    self.file = None
    self.line_number = None

  @property
  def name(self):
    return self.filename

  def readline(self):
    if self.unread:
      try:
        return self.unread
      finally:
        self.unread = None
    line = self.file.readline()
    self.line_number += 1
    return line

  def unreadline(self, line):
    self.unread = line

  def where(self):
    '''Returns the file name and the line number of the last line read as a string suitable for error messages.'''
    return '%s %d' % (self.name, self.line_number)

