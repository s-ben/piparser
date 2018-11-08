
import pandas as pd 
import json
import re
import time
from git import Repo


# Proposal we want to analyze
proposal_num = '27f87171d98b7923a1bd2bee6affed929fa2d2a6e178b5c80a9971a92a5c7f50'

# Path to repo with Pi data
repo_path = '/Users/sben/Documents/coins/decred/analytics/voteAnalytics/mainnet'


# ----------------- Git automation -----------------

# create repo object ()
repo = Repo(repo_path)	

# get all commits on master branch
commits = list(repo.iter_commits('master'))#, max_count=10, skip=20))

# print commits and their timestamp (human readable) to screen
for i in range(0,len(commits)):

	print(commits[i])	# print commit object (which shows hash #)
	print(time.strftime("%a, %d %b %Y %H:%M", time.gmtime(commits[i].committed_date)))

# get git tree for most recent commit
tree = commits[0].tree

# search tree (top-level dir) for desired proposal folder
for i in range(0,len(tree.trees)):

	if tree.trees[i].name == proposal_num:		# look for folder with desired proposal
		print(tree.trees[i].name)
		proposal_tree = tree.trees[i]			# get tree of desired proposal


# print contents of directories in proposal_tree
for entry in proposal_tree.trees[2]:                                         # intuitive iteration of tree members
    # print(entry)
    print(entry.name)	# print filename

# print contents of directories in proposal_tree containing votes (cheating here by hard coding)
for entry in proposal_tree.trees[2]:                                         # intuitive iteration of tree members
    # print(entry)
    print(entry.name)	# print filename

# get votes from 'ballot.journal' file (cheating and hard coding here)
votes = proposal_tree.trees[2].trees[1].trees[0].blobs[0] 


# ----------------- Parse vote data -----------------

# NOTE: the code below assumes you are in the directory with 
# the 'ballot.journal' file you want to analyze (not yet using 
# above git automation)

# filename  = 'comments.journal'
filename  = 'ballot.journal'

# open file with votes, parse according to /n (newline)
votes = open(filename).read().splitlines()

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


# parse journal file, extracting individual "json" (not sure if actually json)
# objects into a list of python dicts (which can be used to store/query data 
# however we like)

data = []

for i in range(0,len(votes)):
# for i in range(0,1):
	for item in iterparse(votes[i]):
	    data.append(item)

# print first vote in list
print(data[0])
print(data[1])

# as a test, store first vote data in panda DataFrame and write to csv 
# (not currently working, but you get the idea)
df = pd.DataFrame(data[1])  
df.to_csv('testvote.csv', sep=',',index=False,header=None)

