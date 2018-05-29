# Summary

 This script analyzes file stream from EDGAR analytics and analyze user activities by reading it line-by-line. This data is then ingested and summarized into an output file. We try to identify user's sessions and how long was the user visit as well as how many documents were accessed by the user. Each user is assumed to be uniquely associated with a single IP address and we use a constant inactivity time for all users that is accepted as one of the inputs of the script.

# Dependencies
The script is written in Python 3.6, and has following package dependencies:
time
datetime
sys

## Assumptions
* Each user has unique IP address and vice versa.
* Every line represents an access of a document.
* Input csv and txt files are present.
* Input log.csv file entries exist in chronological order.
* Date and Time exist in the expected format of yyyy-mm-dd H:M:S.
* `run.sh` executes python script in src/ and accepts three command line arguments
  *  path of `log.csv`
  * path of `inactivity_period.txt`
  * output file path


## Input files

### `log.csv`
The file contains data from SEC. The first line of the file is header and is ignored for processing purpose. The rest of the lines are processed one by one and are assumed to be in chronological order.

### `inactivity_period.txt`
This input file has an integer value that represents the time period, in seconds, during which if a user does not have an activity, their session is expired.

## Output file

The output file `sessionization.txt` contains a summary of the user sessions:

* IP address of the user
* Date and time of the first document access for the session
* Date and time of the last document access for the session
* Number of seconds the session lasted
* Number of documents accessed during the session

