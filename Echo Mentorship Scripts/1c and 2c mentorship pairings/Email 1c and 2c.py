import json
import os
import win32com.client as win32

#PAIRS_FILE = 'generated_pairs1.json'

# Load the participants data (the same as in the first part)
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
    'Group2':
        {
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
