import json
import os
import random
import win32com.client as win32  # For sending emails via Outlook

# Define file path for storing historical pairs
PAIRS_FILE = 'previous_pairs1c2c.json'

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

        # Start email body with a standard message
        mail.Body = f"Greetings,\n\nMeeting between: {', '.join(pair)}."

        # Add special message for groups of three
        if len(pair) == 3:
            mail.Body += "\nPlease allow the upperclass to determine how the meeting will be between 3 people."

        # Add closing statement
        mail.Body += "\nAccountability Spreadsheet: https://cgacademy.sharepoint.com/:x:/s/ECHOCompany940/EeL6sZhf6D1Oj_UxH1uhyBEBXoEx6iT-3K5eLl2aXG7QWw?e=veKHXg\n\nVery Respectfully,\nEcho Mentoring Program"

        mail.To = email_recipients  # Set recipient emails
        mail.Send()  # Send the email


# Run the pairing function
pairs = create_pairs(participants)

# Send email to each pair
#send_email(pairs)

# Display the results
print("Pairs:")
for pair in pairs:
    pair_emails = [participants['Group1'].get(name, participants['Group2'].get(name))['email'] for name in pair]
    print(f"{pair}: {pair_emails}")
