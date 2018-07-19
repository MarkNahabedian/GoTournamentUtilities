
import math
from enum import Enum


def define_ranks():
  ranks = []
  for kyu in range(30, 0, -1):
    ranks.append('%dK' % kyu)
  for dan in range(1, 10):
    ranks.append('%dD' % dan)
  global Rank
  Rank = Enum('Rank', ranks)

define_ranks()
del define_ranks


def rank_from_rating(rating):
  r = math.trunc(rating)
  if r >= 1:
    # Dan rating
    return Rank(Rank['1D'].value + r - 1)
  if r <= -1:
    return Rank(Rank['30K'].value + r + 30)
  raise Exception('Invalid rating %f' % (rating,))


# for rank in Rank:
#   print(rank.name, rank.value)

# # Validating
assert rank_from_rating(1.1) == Rank['1D']
assert rank_from_rating(9.9) == Rank['9D']
assert rank_from_rating(-30) == Rank['30K']
assert rank_from_rating(-1.2) == Rank['1K']

