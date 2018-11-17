# piparser
Python scripts for parsing Politeia data for analysis.

The `vote_analysis.py` script analyzes proposal data stored in the [decred-proposals/mainnet](https://github.com/decred-proposals/mainnet) repo, which is updated hourly by the Politeia system. 

# Requirements

- git
- python 3 (though I think python 2.7 will work too...haven't tested...)

# Installation

Install requrired python modules:

```pip install -r requirements.txt```

# How to use

1. If you haven't already, clone the [decred-proposals/mainnet](https://github.com/decred-proposals/mainnet) repo.

```git clone https://github.com/decred-proposals/mainnet```

2. Pull most recent data, if necessary.

```git pull```

3. Edit `vote_analysis.py` file to specify the proposal number, proposal title, and path to repo (these are hardcoded for now...). E.g.,

```
proposal_num = 'fa38a3593d9a3f6cb2478a24c25114f5097c572f6dadf24c78bb521ed10992a4'
proposal_title = 'Decred Contractor Clearance Process'
repo_path = '/<user>/<path>/mainnet/
```
4. run script.

```python vote_analysis.py```

Check the root directory for csv files containing vote data. The file ending in `...votes.csv` contains raw vote data (one vote per row) for the specified proposal. The file ending in `...votes_stats.csv` contains commit-level (i.e. hourly) vote data, and some basic stats. 

```
Decred Contractor Clearance Process_votes.csv
Decred Contractor Clearance Process_votes_stats.csv
```
