import json
import os
import win32com.client as win32

PAIRS_FILE = 'generated_pairs.json'

# Load the participants data (the same as in the first part)
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
        'Fiona McCartin': {'division': 'External Event Operations', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Nicholas Monahan': {'division': 'Command', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Daniel Nusraty': {'division': 'Internal Communications', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Miquel Penella': {'division': 'OID', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Siamack Porter': {'division': 'Company Watches and Logs', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Isabel Robey': {'division': 'Command', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Ian Roeder': {'division': 'RISO', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Emily Scharnitzky': {'division': 'Drill', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Ensen Sgaglio': {'division': 'Command', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Aidan Shaw': {'division': 'Drill', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Marcella Silberger': {'division': 'Character Development', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Laura Slovensky': {'division': 'Regimental Watches', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Delaney Taplin-Patterson': {'division': 'Morale', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Riley Thorburn': {'division': 'Family Weekend', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Grace Tomisek': {'division': 'Command', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Kobi Weiland': {'division': 'OID', 'email': 'Rohan.S.Iyer@uscga.edu'},
        'Kai-Hung Yang': {'division': 'Wellness and Readiness', 'email': 'Rohan.S.Iyer@uscga.edu'}


    },
    'Group2':
        {
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
            'Nathan Fitt': {'division': 'External Event Operations', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Bryan Garza': {'division': 'Watch Office/Quarterdeck', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Jacob Hardy': {'division': 'Character Development', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Maddox Holmes-Selby': {'division': 'Command', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Tara Jessen': {'division': 'Company Watches and Logs', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Andrew Kehias': {'division': 'Parents and Alumni Associations', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Charlie Klinger': {'division': 'Watch Office/Quarterdeck', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Gabriella Kraus-Rivera': {'division': 'Command', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Lucinae Lazaryan': {'division': 'Family Weekend', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Michael Leone': {'division': 'External Event Planning', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Puti\'on Palacios Camacho': {'division': 'RISO', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Raymond Priddy': {'division': 'Company Watches and Logs', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Charles Romano': {'division': 'Regimental Watches', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Christian Short': {'division': 'Family Weekend', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Kai Shuster': {'division': 'External Event Communications', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'William Spada': {'division': 'Internal Communications', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Alexis Taylor': {'division': 'Command', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Charlie Throne': {'division': 'Drill', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Jackson Triepke': {'division': 'Command', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Hannah Van Cise': {'division': 'Command', 'email': 'Rohan.S.Iyer@uscga.edu'},
            'Hannah Warnke': {'division': 'Training and Logistics', 'email': 'Rohan.S.Iyer@uscga.edu'}


    }
}

def load_pairs():
    """Load the pairs from the file."""
    if os.path.exists(PAIRS_FILE):
        with open(PAIRS_FILE, 'r') as f:
            return json.load(f)
    else:
        print("No pairs file found. Please generate pairs first.")
        return []

def send_email(pairs):
    outlook = win32.Dispatch('outlook.application')

    for pair in pairs:
        emails = [participants['Group1'].get(name, participants['Group2'].get(name))['email'] for name in pair]
        email_recipients = "; ".join(emails)

        mail = outlook.CreateItem(0)
        mail.Subject = "Echo Mentorship: Random Assignment"
        mail.Body = f"Greetings,\n\nMeeting between: {', '.join(pair)}."

        if len(pair) == 3:
            mail.Body += "\nPlease allow the upperclass to determine how the meeting will be conducted between three people."

        mail.Body += "\nAccountability Spreadsheet: https://cgacademy.sharepoint.com/:x:/s/ECHOCompany940/EeL6sZhf6D1Oj_UxH1uhyBEBXoEx6iT-3K5eLl2aXG7QWw?e=YK0WOO\n\nVery Respectfully,\nEcho Mentoring Program"
        mail.To = email_recipients
        mail.Send()

# Load the pairs and send emails
pairs = load_pairs()
if pairs:
    send_email(pairs)
    print("Emails have been sent.")
else:
    print("No pairs to send emails to.")
