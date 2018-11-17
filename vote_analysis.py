import pandas as pd 
import json
import re
import time
from git import Repo
import os


# Proposal we want to analyze
# proposal_num = '27f87171d98b7923a1bd2bee6affed929fa2d2a6e178b5c80a9971a92a5c7f50'
# proposal_title = 'Ditto Communications Proposal for Decred'

proposal_num = 'fa38a3593d9a3f6cb2478a24c25114f5097c572f6dadf24c78bb521ed10992a4'
proposal_title = 'Decred Contractor Clearance Process'




# Path to repo with Pi data
repo_path = '/Users/sben/Documents/coins/decred/analytics/voteAnalytics/mainnet/'

proposal_path = repo_path + proposal_num



# function to parse multiple dicts from string of dicts ret
nonspace = re.compile(r'\S')

def iterparse(j):
    decoder = json.JSONDecoder()
    pos = 0
    while True:
        matched = nonspace.search(j, pos)
        if not matched:
            break
        pos = matched.start()
        decoded, pos = decoder.raw_decode(j, pos)
        yield decoded



# ----------------- Git automation -----------------

# create repo object ()
repo = Repo(repo_path)  

# get path to 'ballot.journal' file (vote file) for given proposal
ballot_path = repo.git.ls_files(proposal_num+'/*/plugins/decred/ballot.journal')  

# find all commits that contain a 'ballot.journal' file (vote file)
commits = list(repo.iter_commits(paths=ballot_path))

votes = []
votes_stats = []

votes_yes = 0
votes_total = 0

# for each commit with a 'ballot.journal' file (from oldest commit to latest), extract votes
for i in range(len(commits)-1,-1,-1): 

    print('processing commit: '+ str(i))
    # print(commits[i].name_rev.split()[0])

    # checkout commit (oldest to latests)
    # repo.git.checkout(commits[len(commits)-i-1].name_rev.split()[0])

    # checkout commit 
    repo.git.checkout(commits[i].name_rev.split()[0])

    # read .journal file (newline separated txt file)
    votes_raw = open(repo_path+ballot_path).read().splitlines()



    # for each (new) vote in a commit 
    for j in range(len(votes),len(votes_raw)):
    
        vote = {}
        vote_stats = {}

        # for each vote (raw txt data), extract params to dict
        for item in iterparse(votes_raw[j]):

            if 'castvote' in item.keys():       # if a vote was cast
                vote['timestamp_unix'] = commits[i].committed_date      # time (unix)
                vote['timestamp_human'] = time.strftime("%a, %d %b %Y %H:%M", time.gmtime(commits[i].committed_date))   # time (human readable)
                vote['commit_num'] = len(commits) - i               # commit number
                vote['raw_data'] = votes_raw[j]     # raw txt vote
                vote['ticket'] = item['castvote']['ticket']     # ticket number
                vote['votebit'] = item['castvote']['votebit']   # votebit (Yes/No)

                if int(item['castvote']['votebit']) == 1:
                    vote['vote'] = 'No'
                    votes_total += 1
                elif int(item['castvote']['votebit']) == 2:
                    vote['vote'] = 'Yes'
                    votes_yes += 1
                    votes_total += 1

                votes.append(vote)


    vote_stats['commit_num'] = len(commits) - i
    vote_stats['num_votes'] = votes_total
    vote_stats['num_yes_votes'] = votes_yes 
    vote_stats['perc_yes_votes'] = votes_yes/votes_total

    votes_stats.append(vote_stats)


df = pd.DataFrame(votes)  
df.to_csv(proposal_title+'_votes.csv', sep=',',index=False,header=True)


df = pd.DataFrame(votes_stats)  
df.to_csv(proposal_title+'_votes_stats.csv', sep=',',index=False,header=True)




