import json
import os
import random

PAIRS_FILE = 'generated_pairs2.json'

# Participants data with emails included
participants = {
    'Group1': {
        'Matthew Abate': {'division': 'Morale', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Solomon Ashby': {'division': 'Company Watches and Logs', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Cleveland Brown': {'division': 'External Event Operations', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'MacKenzie Bucki': {'division': 'Parents and Alumni Associations', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Gillian Cascio': {'division': 'External Event Communications', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Brandon Chhoeung': {'division': 'Family Weekend', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Alejandro Christopher': {'division': 'External Event Logistics', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Dominic Gilbert': {'division': 'Training and Logistics', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Senan Gorman': {'division': 'Training and Logistics', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Ashley Hickman': {'division': 'External Event Planning', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Margarita Hillon': {'division': 'Ethics Forum', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Rohan Iyer': {'division': 'Command', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Hunter Jennings': {'division': 'Wellness and Readiness', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Hannah Laudenslager': {'division': 'Ethics Forum', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Ryan Lista': {'division': 'Watch Office/Quarterdeck', 'email': 'Rohan.S.Iyer@uscga.edu'},
    },
    'Group2': {
        'Brian Akalski': {'division': 'Morale', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Leomar Ayala-Irizarry': {'division': 'Training and Logistics', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Laila Baameur': {'division': 'Morale', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Bridget Bartz': {'division': 'Internal Communications', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Sarah Bell': {'division': 'Wellness and Readiness', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Tyler Bissett': {'division': 'RISO', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Matthew Clarke': {'division': 'Ethics Forum', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Julia Conneely': {'division': 'Drill', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Elliot Cowles': {'division': 'OID', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Leanara Dukat': {'division': 'Ethics Forum', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Benajamin Dush': {'division': 'External Event Logistics', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Micheal Edwards': {'division': 'Regimental Watches', 'email': 'Rohan.S.Iyer@uscga.edu'},
    }
}

def load_all_previous_pairs():
    """Load all previously stored pairs from the file."""
    if os.path.exists(PAIRS_FILE):
        with open(PAIRS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_pairs(pairs):
    """Save generated pairs to the file."""
    with open(PAIRS_FILE, 'w') as f:
        json.dump(pairs, f)

def create_pairs(participants):
    group1 = list(participants['Group1'].items())
    group2 = list(participants['Group2'].items())

    random.shuffle(group1)
    random.shuffle(group2)

    pairs = []
    unpaired_group1 = []
    unpaired_group2 = []

    for person1, details1 in group1:
        matched = False
        for i, (person2, details2) in enumerate(group2):
            if details1['division'] != details2['division']:
                pair = (person1, person2)
                pairs.append(pair)
                group2.pop(i)
                matched = True
                break
        if not matched:
            unpaired_group1.append(person1)

    unpaired_group2 = [person2 for person2, _ in group2]

    # Adding unpaired participants to existing pairs
    for unpaired in unpaired_group1 + unpaired_group2:
        for i, pair in enumerate(pairs):
            if len(pair) == 2:
                person1, person2 = pair
                if (participants['Group1'].get(unpaired, {}).get('division') != participants['Group2'][person2]['division']
                        and participants['Group2'].get(unpaired, {}).get('division') != participants['Group1'][person1]['division']):
                    pairs[i] = (*pair, unpaired)
                    break

    save_pairs(pairs)
    return pairs

# Generate the pairs
pairs = create_pairs(participants)
print("Pairs have been generated and saved. You can now manually edit the pairs if needed.")
