# Representation of the contents of https://www.usgo.org/ratings/TDListA.txt

import abc
import csv
import datetime

AGA_MEMBER_FILE_URI = 'https://www.usgo.org/ratings/TDListA.txt'
AGA_MEMBER_FILE_NAME = 'TDListA.txt'

class AGAMembersAlreadyLoaded (Exception):
  def __str__(self):
    return 'The AGA membership list has already been loaded.'


class AGAMember (object):
  '''AGAMember represents a single item in the AGA membership list.'''
  AllMembers = []

  @classmethod
  def check_loaded(cls):
    '''Raises AGAMembersAlreadyLoaded if the list of loaded AGA members isn't empty.'''
    if len(cls.AllMembers) > 0:
      raise AGAMembersAlreadyLoaded()

  @classmethod
  def read_member_file(cls):
    '''Loads TDListA.txt from the current directory.'''
    cls.check_loaded()
    with open(AGA_MEMBER_FILE_NAME, 'r') as f:
      reader = csv.reader(f, delimiter='\t')
      for row in reader:
        if len(row) >= 5:
          cls.fromCSVRecord(row)

  @classmethod
  def fromCSVRecord(cls, parsed_csv_record):
    '''Creates an AGAMEmber from a single record of the membership file.'''
    name = parsed_csv_record[0].split(',')
    last_name = name[0].strip()
    first_name = None
    if len(name) > 1:
      first_name = name[1].strip()
    aga_id = int(parsed_csv_record[1])
    membership_type = parsed_csv_record[2]
    rating = parsed_csv_record[3]
    if len(rating) > 0:
      rating = float(rating)
    else:
      rating = None
    expiration = parsed_csv_record[4].split('/')
    expiration_date = None
    if len(expiration) == 3:
      expiration_date = datetime.date(int(expiration[2]), int(expiration[0]), int(expiration[1]))
    member = AGAMember(last_name, first_name, aga_id, membership_type, rating, expiration_date)
    cls.AllMembers.append(member)

  @classmethod
  def search(cls, substring):
    '''Returns a list of AGAMember objects whose first or last names contain substring.'''
    matches = []
    for member in cls.AllMembers:
      if substring in member.last_name:
        matches.append(member)
        continue
      if member.first_name and substring in member.first_name:
        matches.append(member)
    return matches

  @classmethod
  def lookupID(cls, id):
    '''Looks up an AGAMember by AGA ID number.'''
    for member in cls.AllMembers:
      if id == member.aga_id:
        return member
    return None

  def __init__(self, last_name, first_name, aga_id, membership_type, rating, expiration_date):
    '''Makes an AGAMember from the specified data.'''
    self.last_name = last_name
    self.first_name = first_name
    self.aga_id = aga_id
    self.membership_type = membership_type
    self.rating = rating
    self.expiration_date = expiration_date



