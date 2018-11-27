import pandas as pd 
import json
import re
import time
from git import Repo
import os
import sys


# ----------------- Specify Git path  -------------------

# Path to repo with Pi data
repo_path = '/Users/sben/Documents/coins/decred/analytics/voteAnalytics/mainnet/'

proposal_title = 'Title of proposal (To fe filled in later)' # don't worry about this for now


# ----------------- Extract and Analyze Votes  -----------------

def count_votes(repo, proposal_num, proposal_title):


	# repo.git.checkout('master')		# checkout master branch to reset HEAD if needed

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

				if 'castvote' in item.keys(): 		# if a vote was cast
					vote['timestamp'] = commits[i].committed_date		# time (unix)
					# vote['timestamp_human'] = time.strftime("%a, %d %b %Y %H:%M", time.gmtime(commits[i].committed_date))	# time (human readable)
					vote['commit_num'] = len(commits) - i				# commit number
					# vote['raw_data'] = votes_raw[j]		# raw txt vote
					vote['ticket'] = item['castvote']['ticket']  	# ticket number
					vote['votebit'] = item['castvote']['votebit']  	# votebit (Yes/No)

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

	return votes, votes_stats


# ----------------- Parse journal files to dicts  -------------------

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



# ----------------- get proposal numbers --------------------------

# create repo object ()
repo = Repo(repo_path)	


if len(sys.argv) > 1:

	proposals = []
	for i in range(1,len(sys.argv)):
		proposals.append(sys.argv[i])
		# print(sys.argv[i])
	# print(proposals)
else:

	proposals = []
	# fetch mainnet tree (repo object w/ contents)
	tree = repo.heads.master.commit.tree
	# get proposals (assumption: all folders in root repo are proposal folders)
	proposal_objs = tree.trees

	for i in range(0,len(proposal_objs)):
		if proposal_objs[i].name != 'anchors':
			proposals.append(proposal_objs[i].name)
	# print(proposals)
	# print(len(proposals))


# ----------------- tally votes --------------------------

for i in range(0,len(proposals)):

	proposal_num = proposals[i] 
	# print(proposal_num)

	repo.git.checkout('master')		# checkout master branch to reset HEAD 

	ballot_path = repo.git.ls_files(proposal_num+'/*/plugins/decred/ballot.journal')  

	if ballot_path != '':	# if a ballot.journal file exists, count votes

		print('processing proposal: '+ proposal_num)

		# ----------------- Process votes -----------------
		votes, votes_stats = count_votes(repo, proposal_num, proposal_title)

		# ----------------- Save to csv  -----------------
		# save raw vote data to csv
		df = pd.DataFrame(votes)  
		df.to_csv(proposal_num+'_votes.csv', sep=',',index=False,header=True,columns=['commit_num','timestamp','ticket','vote'])

		# saave vote stats to csv
		df = pd.DataFrame(votes_stats)  
		df.to_csv(proposal_num+'_votes_stats.csv', sep=',',index=False,header=True,columns=['commit_num','num_votes','num_yes_votes','perc_yes_votes'])


repo.git.checkout('master')		# checkout master branch to reset HEAD if needed







