# GoTournamentUtilities

Programs for assisting the director of a Go tournament.

This is how I envision the workflow:

1. Create a new file system directory to contain the files for this tournament.  Make it your current directory.

2. Fetch https://www.usgo.org/ratings/TDListA.txt.

3. Run registration.py.  It will create players.tsv, a tab separated values file.  registration.py can be run several times to add more players.


4. Run pairings.py for each successive round.  It produces round*X*_pairiings.tsv.  To re-pair a round first delete the round*X*_pairiings.tsv file for that round.

5. When the tournament is finished, run results.py to see the winners.


## Notes

### AGA Membership File

https://www.usgo.org/ratings/TDListA.txt is a tab delimited text file.  The columns are

* last name, first name

* AGA member number

* type of membership

* rating

* membership expiration date as month/day/four digit year

* Go club affiliation

* state

* last rated game?

