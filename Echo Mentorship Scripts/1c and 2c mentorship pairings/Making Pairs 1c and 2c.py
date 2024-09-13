import json
import os
import random
import win32com.client as win32  # For sending emails via Outlook

# Define file path for storing historical pairs
PAIRS_FILE = 'previous_pairs1c2c.json'

# Participants data with emails included
participants = {
    'Group1': {
        'Matthew Abate': {'division': 'Morale', 'email': 'Matthew.A.Abate@uscga.edu'},
        'Solomon Ashby': {'division': 'Company Watches and Logs', 'email': 'Solomon.H.Ashby@uscga.edu'},
        'Cleveland Brown': {'division': 'External Event Operations', 'email': 'Cleveland.E.Brown@uscga.edu'},
        'MacKenzie Bucki': {'division': 'Parents and Alumni Associations', 'email': 'MacKenzie.M.Bucki@uscga.edu'},
        'Gillian Cascio': {'division': 'External Event Communications', 'email': 'Gillian.H.Cascio@uscga.edu'},
        'Brandon Chhoeung': {'division': 'Family Weekend', 'email': 'Brandon.P.Chhoeung@uscga.edu'},
        'Alejandro Christopher': {'division': 'External Event Logistics', 'email': 'Alejandro.J.Christopher@uscga.edu'},
        'Dominic Gilbert': {'division': 'Training and Logistics', 'email': 'Dominic.S.Gilbert@uscga.edu'},
        'Senan Gorman': {'division': 'Training and Logistics', 'email': 'Senan.M.Gorman@uscga.edu'},
        'Ashley Hickman': {'division': 'External Event Planning', 'email': 'Ashley.D.Hickman@uscga.edu'},
        'Margarita Hillon': {'division': 'Ethics Forum', 'email': 'Margarita.D.Hillon@uscga.edu'},
        'Rohan Iyer': {'division': 'Command', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Hunter Jennings': {'division': 'Wellness and Readiness', 'email': 'Hunter.R.Jennings@uscga.edu'},
        'Hannah Laudenslager': {'division': 'Ethics Forum', 'email': 'Hannah.J.Laudenslager@uscga.edu'},
        'Ryan Lista': {'division': 'Watch Office/Quarterdeck', 'email': 'Ryan.D.Lista@uscga.edu'},
        'Fiona McCartin': {'division': 'External Event Operations', 'email': 'Fiona.K.McCartin@uscga.edu'},
        'Nicholas Monahan': {'division': 'Command', 'email': 'Nicholas.L.Monahan@uscga.edu'},
        'Daniel Nusraty': {'division': 'Internal Communications', 'email': 'Daniel.Y.Nusraty@uscga.edu'},
        'Miquel Penella': {'division': 'OID', 'email': 'Miquel.J.Penella@uscga.edu'},
        'Siamack Porter': {'division': 'Company Watches and Logs', 'email': 'Siamack.S.Porter@uscga.edu'},
        'Isabel Robey': {'division': 'Command', 'email': 'Isabel.A.Robey@uscga.edu'},
        'Ian Roeder': {'division': 'RISO', 'email': 'Ian.S.Roeder@uscga.edu'},
        'Emily Scharnitzky': {'division': 'Drill', 'email': 'Emily.A.Scharnitzky@uscga.edu'},
        'Ensen Sgaglio': {'division': 'Command', 'email': 'Ensen.W.Sgaglio@uscga.edu'},
        'Aidan Shaw': {'division': 'Drill', 'email': 'Aidan.W.Shaw@uscga.edu'},
        'Marcella Silberger': {'division': 'Character Development', 'email': 'Marcella.R.Silberger@uscga.edu'},
        'Laura Slovensky': {'division': 'Regimental Watches', 'email': 'Laura.M.Slovensky@uscga.edu'},
        'Delaney Taplin-Patterson': {'division': 'Morale', 'email': 'Delaney.M.TaplinPatterson@uscga.edu'},
        'Riley Thorburn': {'division': 'Family Weekend', 'email': 'Riley.S.Thorburn@uscga.edu'},
        'Grace Tomisek': {'division': 'Command', 'email': 'Grace.E.Tomisek@uscga.edu'},
        'Kobi Weiland': {'division': 'OID', 'email': 'Kobi.Q.Weiland@uscga.edu'},
        'Kai-Hung Yang': {'division': 'Wellness and Readiness', 'email': 'Kai-Hung.C.Yang@uscga.edu'},
    },
    'Group2': {
        'Brian Akalski': {'division': 'Morale', 'email': 'Brian.M.Akalski@uscga.edu'},
        'Leomar Ayala-Irizarry': {'division': 'Training and Logistics', 'email': 'Leomar.Y.Ayala-Irizarry@uscga.edu'},
        'Laila Baameur': {'division': 'Morale', 'email': 'Laila.S.Baameur@uscga.edu'},
        'Bridget Bartz': {'division': 'Internal Communications', 'email': 'Bridget.A.Bartz@uscga.edu'},
        'Sarah Bell': {'division': 'Wellness and Readiness', 'email': 'Sarah.L.Bell@uscga.edu'},
        'Tyler Bissett': {'division': 'RISO', 'email': 'Tyler.M.Bissett@uscga.edu'},
        'Matthew Clarke': {'division': 'Ethics Forum', 'email': 'Matthew.A.Clarke@uscga.edu'},
        'Julia Conneely': {'division': 'Drill', 'email': 'Julia.C.Conneely@uscga.edu'},
        'Elliot Cowles': {'division': 'OID', 'email': 'Elliot.Z.Cowles@uscga.edu'},
        'Leanara Dukat': {'division': 'Ethics Forum', 'email': 'Leanara.E.Dukat@uscga.edu'},
        'Benajamin Dush': {'division': 'External Event Logistics', 'email': 'Benjamin.S.Dush@uscga.edu'},
        'Micheal Edwards': {'division': 'Regimental Watches', 'email': 'Micheal.L.Edwards@uscga.edu'},
        'Nathan Fitt': {'division': 'External Event Operations', 'email': 'Nathan.R.Fitt@uscga.edu'},
        'Bryan Garza': {'division': 'Watch Office/Quarterdeck', 'email': 'Bryan.Garza@uscga.edu'},
        'Jacob Hardy': {'division': 'Character Development', 'email': 'Jacob.W.Hardy@uscga.edu'},
        'Maddox Holmes-Selby': {'division': 'Command', 'email': 'Maddox.H.Holmes-Selby@uscga.edu'},
        'Tara Jessen': {'division': 'Company Watches and Logs', 'email': 'Tara.E.Jessen@uscga.edu'},
        'Andrew Kehias': {'division': 'Parents and Alumni Associations', 'email': 'Andrew.J.Kehias@uscga.edu'},
        'Charlie Klinger': {'division': 'Watch Office/Quarterdeck', 'email': 'Charlie.J.Klinger@uscga.edu'},
        'Gabriella Kraus-Rivera': {'division': 'Command', 'email': 'Gabriella.C.Kraus-Rivera@uscga.edu'},
        'Lucinae Lazaryan': {'division': 'Family Weekend', 'email': 'Lucinae.A.Lazaryan@uscga.edu'},
        'Michael Leone': {'division': 'External Event Planning', 'email': 'Michael.A.Leone@uscga.edu'},
        'Puti\'on Palacios Camacho': {'division': 'RISO', 'email': 'Puti\'on.P.PalaciosCamacho@uscga.edu'},
        'Raymond Priddy': {'division': 'Company Watches and Logs', 'email': 'Raymond.J.Priddy@uscga.edu'},
        'Charles Romano': {'division': 'Regimental Watches', 'email': 'Charles.R.Romano@uscga.edu'},
        'Christian Short': {'division': 'Family Weekend', 'email': 'Christian.J.Short@uscga.edu'},
        'Kai Shuster': {'division': 'External Event Communications', 'email': 'Kai.P.Shuster@uscga.edu'},
        'William Spada': {'division': 'Internal Communications', 'email': 'William.D.Spada@uscga.edu'},
        'Alexis Taylor': {'division': 'Command', 'email': 'Alexis.M.Taylor@uscga.edu'},
        'Charlie Throne': {'division': 'Drill', 'email': 'Charlie.N.Throne@uscga.edu'},
        'Jackson Triepke': {'division': 'Command', 'email': 'Jackson.A.Triepke@uscga.edu'},
        'Hannah Van Cise': {'division': 'Command', 'email': 'Hannah.E.VanCise@uscga.edu'},
        'Hannah Warnke': {'division': 'Training and Logistics', 'email': 'Hannah.J.Warnke@uscga.edu'},
    }
}


def load_all_previous_pairs():
    """Load all previously stored pairs from the file."""
    if os.path.exists(PAIRS_FILE):
        with open(PAIRS_FILE, 'r') as f:
            return json.load(f)
    return []


def save_all_pairs(all_pairs):
    """Save all pairs to the file."""
    with open(PAIRS_FILE, 'w') as f:
        json.dump(all_pairs, f)


def create_pairs(participants):
    group1 = list(participants['Group1'].items())
    group2 = list(participants['Group2'].items())

    # Load all historical pairs
    all_previous_pairs = load_all_previous_pairs()
    used_pairs = set(tuple(sorted(pair)) for pair in all_previous_pairs)

    random.shuffle(group1)  # Shuffle group1 to ensure random pairings
    random.shuffle(group2)  # Shuffle group2 to ensure random pairings

    pairs = []
    unpaired_group1 = []
    unpaired_group2 = []

    # Initial pairing process
    for person1, details1 in group1:
        matched = False
        for i, (person2, details2) in enumerate(group2):
            if details1['division'] != details2['division']:
                pair = tuple(sorted([person1, person2]))
                if pair not in used_pairs:
                    pairs.append((person1, person2))
                    group2.pop(i)  # Remove the paired person from group2 to avoid duplicate pairing
                    matched = True
                    used_pairs.add(pair)  # Add to used pairs
                    break
        if not matched:
            unpaired_group1.append(person1)

    # Any remaining people in group2 are unpaired
    unpaired_group2 = [person2 for person2, _ in group2]

    # Add unpaired participants to existing pairs to create groups of three
    for unpaired in unpaired_group1 + unpaired_group2:
        added = False
        for i, pair in enumerate(pairs):
            if len(pair) == 2:  # Only add to pairs of two
                person1, person2 = pair
                details1 = participants['Group1'].get(person1) or participants['Group2'].get(person1)
                details2 = participants['Group1'].get(person2) or participants['Group2'].get(person2)
                if participants['Group1'].get(unpaired) and details2['division'] != participants['Group1'][unpaired]['division'] and details1['division'] != participants['Group1'][unpaired]['division']:
                    pairs[i] = (*pairs[i], unpaired)
                    added = True
                    break
                elif participants['Group2'].get(unpaired) and details2['division'] != participants['Group2'][unpaired]['division'] and details1['division'] != participants['Group2'][unpaired]['division']:
                    pairs[i] = (*pairs[i], unpaired)
                    added = True
                    break
        if not added:
            pairs.append((unpaired,))  # If unable to match, leave as a single unpaired participant

    # Save current pairs to historical list
    all_previous_pairs.extend(pairs)
    save_all_pairs(all_previous_pairs)

    return pairs


def send_email(pairs):
    # Initialize Outlook application
    outlook = win32.Dispatch('outlook.application')

    for pair in pairs:
        emails = [participants['Group1'].get(name, participants['Group2'].get(name))['email'] for name in pair]
        email_recipients = "; ".join(emails)  # Join emails with a semicolon

        # Create a new mail item
        mail = outlook.CreateItem(0)
        mail.Subject = "Mentorship: Random Assignment"
        mail.Body = f"Greetings,\n\nYour meeting is with: {', '.join(pair)}. \n\nAccountability Spreadsheet: \n\nVery Respectfully,\nEcho Mentoring Program"
        mail.To = email_recipients  # Set recipient emails



# Run the pairing function
pairs = create_pairs(participants)

# Send email to each pair


# Display the results
print("Pairs:")
for pair in pairs:
    pair_emails = [participants['Group1'].get(name, participants['Group2'].get(name))['email'] for name in pair]
    print(f"{pair}: {pair_emails}")
