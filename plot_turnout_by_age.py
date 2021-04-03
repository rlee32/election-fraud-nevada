#!/usr/bin/env python3

import csv
from typing import Dict, Set
from matplotlib import pyplot as plt

VOTER_FILE = './data/voters.csv'
VOTE_FILE = './data/votes.csv'
MINIMUM_REGISTERED_VOTERS = 40 # ages with less registered voters are not plotted.

def str_to_int(date: str):
    """converts MM/DD/YYYY to YYYYMMDD int for easy comparison."""
    tokens = date.strip().split('/')
    if len(tokens) != 3:
        return None
    return int(f'{tokens[-1]}{tokens[0]}{tokens[1]}')

def get_age(start: int, end: int):
    """Returns integer age given dates in form YYYYMMDD as integers. """
    diff = end - start
    if diff < 0:
        return diff / 10000.0
    else:
        return int(diff / 10000)

def read_voters(csv_file: str, election_date: int = 20201103):
    """Reads a csv file containing eligible voters for the specified election.
    Returns a map of voter ID to various properties:
    {
        str: {
            'age': int,
            'registered': bool
            'county': str
        },
        str: {
            'age': int,
            'registered': bool
            'county': str
        },
        ...
    }
    Expected columns:
        VoterID,Residential County,First Name,Middle Name,Last Name,
        Suffix,Birth Date,Registration Date,Residential Address 1,Residential Address 2,
        Residential City,Residential State,Residential Zip,Phone,Party,
        Congressional District,Senate District,Assembly District,Education District,Regent District,
        Registered Precinct,County Status,County Voter ID,ID Required
    """
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f)

        # skip header
        for row in csv_reader:
            header = row
            break

        VOTER_ID_INDEX = 0
        COUNTY_INDEX = 1
        DATE_OF_BIRTH_INDEX = 6
        REGISTRATION_DATE_INDEX = 7

        voters = {}

        for row in csv_reader:
            voter_id = row[VOTER_ID_INDEX]
            birth_date = row[DATE_OF_BIRTH_INDEX]
            if not birth_date:
                print(f'voter ID {voter_id} has no birth date {birth_date}')
                continue
            birth_date = str_to_int(row[DATE_OF_BIRTH_INDEX])
            if not birth_date:
                print(f'voter ID {voter_id} has invalid birth date {row[DATE_OF_BIRTH_INDEX]}')
                continue

            age = get_age(birth_date, election_date)

            assert(voter_id not in voters)

            voters[voter_id] = {'age': age, 'registered': False, 'county': row[COUNTY_INDEX]}

            # assume voters with no registration date are actually registered, if their status is active.
            registration_date = row[REGISTRATION_DATE_INDEX]
            if registration_date:
                registration_date = str_to_int(registration_date)
                if registration_date <= election_date:
                    voters[voter_id]['registered'] = True
                    continue

        print(f'num voters: {len(voters)}')
        return voters

def read_votes(csv_file: str, election_date: str = '11/03/2020'):
    """Reads a csv file containing vote history.
    Returns a set of voter IDs that voted in the specified election.
    Expected columns:
        VotingHistoryID,VoterID,Election Date,Vote Code
    """
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f)

        # skip header
        for row in csv_reader:
            header = row
            break

        VOTER_ID_INDEX = 1
        ELECTION_DATE_INDEX = 2

        votes = set()

        for row in csv_reader:
            if row[ELECTION_DATE_INDEX] != election_date:
                continue
            votes.add(row[VOTER_ID_INDEX])

        print(f'num votes: {len(votes)}')
        return votes

def organize_voters(voters: Dict[str, any]):
    """Organizes voters by county and age. """
    result = {}
    for i in voters:
        v = voters[i]
        c = v['county']
        if c not in result:
            result[c] = {}
        a = v['age']
        if a not in result[c]:
            result[c][a] = 0
        result[c][a] += 1
    return result

def organize_votes(voters: Dict[str, any], votes: Set[str]):
    """Organizes votes by county and age. """
    result = {}
    for i in votes:
        if i not in voters:
            print(f'could not find voter with ID {i}')
            continue
        v = voters[i]
        c = v['county']
        if c not in result:
            result[c] = {}
        a = v['age']
        if a not in result[c]:
            result[c][a] = 0
        result[c][a] += 1
    return result

def plot_age_distribution(voters: Dict[int, int], votes: Dict[int, int], color: str = ''):
    """'votes' and 'voters' map age to number of votes or registered voters. """
    vote_ages = set()
    for age in votes:
        vote_ages.add(age)
    voter_ages = set()
    for age in voters:
        voter_ages.add(age)
    ages = set()
    for age in voter_ages:
        if age in vote_ages:
            ages.add(age)
    ages = list(ages)
    ages.sort()
    total = sum([voters[x] for x in ages])
    print(f'\t{total} registered voters')
    if color:
        plt.plot([x for x in ages if voters[x] > MINIMUM_REGISTERED_VOTERS], [votes[x] / voters[x] for x in ages if voters[x] > MINIMUM_REGISTERED_VOTERS], color)
    else:
        plt.plot([x for x in ages if voters[x] > MINIMUM_REGISTERED_VOTERS], [votes[x] / voters[x] for x in ages if voters[x] > MINIMUM_REGISTERED_VOTERS])

if __name__ == '__main__':
    voters = read_voters(VOTER_FILE)
    votes = read_votes(VOTE_FILE)
    vote_count = organize_votes(voters, votes)
    voter_count = organize_voters(voters)
    for county in voter_count:
        print(f'plotting {county} county')
        plot_age_distribution(voter_count[county], vote_count[county])
    plt.xlabel(f'Age (less than {MINIMUM_REGISTERED_VOTERS} registered voters are hidden)')
    plt.ylabel('Voter turnout (votes / registered voters)')
    plt.title(f'Oklahoma Voter Turnout vs. Age ({len(voter_count)} of {len(voter_count)} counties; each line = 1 county)')
    plt.show()


