# GoTournamentUtilities

Programs for assisting the director of a Go tournament.

This is how I envision the workflow:

1. Create a new file system directory to contain the files for this tournament.  Make it your current directory.

2. Fetch https://www.usgo.org/ratings/TDListA.txt.

3. Run registration.py.  It will create players.tsv, a tab separated values file.  registration.py can be run several times to add more players.


4. Run pairings.py for each successive round.  *How should we tell it which players are taking a by for the round?* It produces round*X*_pairings.tsv.  To re-pair a round first delete the round*X*_pairings.tsv file for that round.

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


### players.tsv

**players.tsv** is created and maintained by registration.py.  It lists
the players who have signed up for the tournament.

Should it be written in alphabetical order by last and first name,
ascending order by AGA id, or descending order by entered rank?

What columns should it have:

* AGA id
* last name
* first name
* entered rank
* eligible/expired
* preregistered
* amount paid?
* arbitrary notes?


### 