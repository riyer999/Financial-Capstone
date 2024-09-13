import json
import os
import random
import win32com.client as win32  # For sending emails via Outlook

# Define file path for storing historical pairs
PAIRS_FILE = 'previous_pairs2c3C.json'

# Participants data with emails included
participants = {
    'Group1': {
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

    },
    'Group2': {
        'Isaac Adkins': {'division': 'Regimental Watches', 'email': 'Isaac.H.Adkins@uscga.edu'},
        'Abraham Al-Khalili': {'division': 'Wellness and Readiness', 'email': 'Abraham.K.AlKhalili@uscga.edu'},
        'Raniah Andrianjafimahery': {'division': 'External Event Logistics', 'email': 'Raniah.B.Andrianjafimahery@uscga.edu'},
        'Tessa Breitbart': {'division': 'Family Weekend', 'email': 'Tessa.G.Breitbart@uscga.edu'},
        'Thomas Butler': {'division': 'External Event Communications', 'email': 'Thomas.D.Butler@uscga.edu'},
        'Ramon Cruz': {'division': 'Family Weekend', 'email': 'Ramon.M.Cruz@uscga.edu'},
        'Jack Cura': {'division': 'Training and Logistics', 'email': 'Jack.R.Cura@uscga.edu'},
        'Blake Delevan': {'division': 'Drill', 'email': 'Blake.W.Delevan@uscga.edu'},
        'Alex Denaroso': {'division': 'Ethics Forum', 'email': 'Alex.S.Denaroso@uscga.edu'},
        'Xavier DiGennaro': {'division': 'Watch Office/Quarterdeck', 'email': 'Xavier.R.DiGennaro@uscga.edu'},
        'Jackson Dorsey': {'division': 'External Event Planning', 'email': 'Jackson.A.Dorsey@uscga.edu'},
        'Levi Edmonds': {'division': 'Company Watches and Logs', 'email': 'Levi.A.Edmonds@uscga.edu'},
        'Max Eisenbeiser': {'division': 'RISO', 'email': 'Max.J.Eisenbeiser@uscga.edu'},
        'Jake Fish': {'division': 'Character Development', 'email': 'Jake.L.Fish@uscga.edu'},
        'Conner FitzMaurice': {'division': 'External Event Operations', 'email': 'Conner.F.FitzMaurice@uscga.edu'},
        'Julia Gallinger': {'division': 'Regimental Watches', 'email': 'Julia.E.Gallinger@uscga.edu'},
        'Piper Garrett': {'division': 'Ethics Forum', 'email': 'Piper.R.Garrett@uscga.edu'},
        'Charles Gimber': {'division': 'RISO', 'email': 'Charles.E.Gimber@uscga.edu'},
        'Jordan Jansen': {'division': 'Internal Communications', 'email': 'Jordan.C.Jansen@uscga.edu'},
        'Sandra Kirvelevicius': {'division': 'Morale', 'email': 'Sandra.H.Kirvelevicius@uscga.edu'},
        'Katie Kogler': {'division': 'Parents and Alumni Associations', 'email': 'Katie.E.Kogler@uscga.edu'},
        'Catherine Mahoney': {'division': 'External Event Planning', 'email': 'Catherine.M.Mahoney@uscga.edu'},
        'Nicholas Marck': {'division': 'External Event Logistics', 'email': 'Nicholas.W.Marck@uscga.edu'},
        'Savannah McBrayer': {'division': 'Morale', 'email': 'Savannah.A.McBrayer@uscga.edu'},
        'Cole Miller': {'division': 'Training and Logistics', 'email': 'Cole.R.Miller@uscga.edu'},
        'Ivan Nicolai': {'division': 'Parents and Alumni Associations', 'email': 'Ivan.R.Nicolai@uscga.edu'},
        'Alexis Pape': {'division': 'Character Development', 'email': 'Alexis.F.Pape@uscga.edu'},
        'Seth Pettis': {'division': 'OID', 'email': 'Seth.O.Pettis@uscga.edu'},
        'Anabelle Pezzullo': {'division': 'Drill', 'email': 'Anabelle.C.Pezzullo@uscga.edu'},
        'Kirsten Heather Reyes': {'division': 'Wellness and Readiness', 'email': 'KirstenHeather.A.Reyes@uscga.edu'},
        'Elyssia Reyna': {'division': 'External Event Operations', 'email': 'Elyssia.L.Reyna@uscga.edu'},
        'Gavin Russiello-Tous': {'division': 'Company Watches and Logs', 'email': 'Gavin.C.RussielloTous@uscga.edu'},
        'Taylor Schnatz': {'division': 'Internal Communications', 'email': 'Taylor.L.Schnatz@uscga.edu'},
        'Charles Smith': {'division': 'External Event Communications', 'email': 'Charles.M.Smith@uscga.edu'},
        'Owen Wetter': {'division': 'OID', 'email': 'Owen.O.Wetter@uscga.edu'},
    }
}
'''commenting out so that I do not accidentally send it out

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

    # Adding unpaired participants to existing pairs
    for unpaired in unpaired_group1:
        added = False
        for i, pair in enumerate(pairs):
            person2 = pair[1]
            details2 = participants['Group2'][person2]
            if participants['Group1'][unpaired]['division'] != details2['division']:
                pairs[i] = (*pairs[i], unpaired)
                added = True
                break
        if not added:
            unpaired_group2.append(unpaired)  # Keep as unpaired if unable to find a match

    for unpaired in unpaired_group2:
        added = False
        for i, pair in enumerate(pairs):
            person1 = pair[0]
            details1 = participants['Group1'][person1]
            if participants['Group2'][unpaired]['division'] != details1['division']:
                pairs[i] = (*pairs[i], unpaired)
                added = True
                break
        if not added:
            unpaired_group1.append(unpaired)  # Keep as unpaired if unable to find a match

    # Save current pairs to historical list
    all_previous_pairs.extend(pairs)
    save_all_pairs(all_previous_pairs)

    return pairs, unpaired_group1, unpaired_group2


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
        mail.Send()  # Send the email


# Run the pairing function
pairs, unpaired_group1, unpaired_group2 = create_pairs(participants)

# Send email to each pair
send_email(pairs)

# Display the results
print("Pairs:")
for pair in pairs:
    pair_emails = [participants['Group1'].get(name, participants['Group2'].get(name))['email'] for name in pair]
    print(f"{pair}: {pair_emails}")

print("\nUnpaired in Group 1:")
for name in unpaired_group1:
    print(f"{name}: {participants['Group1'][name]['email']}")

print("\nUnpaired in Group 2:")
for name in unpaired_group2:
    print(f"{name}: {participants['Group2'][name]['email']}")
'''