# NBA_v2

## What is it?
This is a small application for getting stats from nba.com into a database, usually for 
other applications to use. It uses the rather splendid nba-api by Swar Patel (swar): https://github.com/swar/nba_api 
with some modifications to the default headers used for requests made to nba.com. The data processing and upload to dbs,
as well as the config, orchestration and helpers are my own.
##What is it for?
Mostly I did this to play around with publishing my own web project with NBA stats. The web site can be accessed 
at: 

https://nba-scores-daily.herokuapp.com

That being said the app can be used for other projects that use nba.com stats.
### How to install?
Just download and set up a virtual env using the requirements.txt file and you should be done.
### How to use it?
Running main.py with any python 3 (3.7 and up) should do the trick. The app defaults to pulling yesterdays stats and 
results. That behaviour can be altered by setting up runtime flags. To upload results to a db you also need to set up
the correct environment variables. Here are the current runtime flags and env vars:

##### Environment variables used:
* NBA_DB_URL - the url for the database that will store the output stats
* NBA_MONITOR_DB_URL - the url for the database that will store the monitor log keeping track of the base runtime data
(e.g. for what dates were the stats pulled, was the db upload successful)

##### Runtime flags:
* --NBASTARTDATE - the first date for witch the app will run
* --NBAENDDATE - the last date (inclusive) for which the app will run

If start date and end date are provided, the app will attempt to get all of the stats between those two dates, 
both dates included. The size of the batch processed and the timeouts between batches can be modified in the config.py 
file.

### Future development?
If any, probably as a separate project. This can see changes if the NBA get's fussy about it's endpoints again.



 
