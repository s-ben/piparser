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

3. Edit `vote_analysis.py` file to specify path to repo (hardcoded for now...). E.g.,

```
repo_path = '/<user>/<path>/mainnet/
```
4. Run script and pass desired proposal number as an argument.

```python vote_analysis.py 27f87171d98b7923a1bd2bee6affed929fa2d2a6e178b5c80a9971a92a5c7f50```

Check the root directory for csv files containing vote data. The file ending in `...votes.csv` contains raw vote data (one vote per row) for the specified proposal. The file ending in `...votes_stats.csv` contains commit-level (i.e. hourly) vote data, and some basic stats. 

```
27f87171d98b7923a1bd2bee6affed929fa2d2a6e178b5c80a9971a92a5c7f50_votes.csv
27f87171d98b7923a1bd2bee6affed929fa2d2a6e178b5c80a9971a92a5c7f50_votes_stats.csv
```
