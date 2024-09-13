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
    'Group2': {
        'Samantha Barr': {'division': 'OID', 'email': 'Samantha.E.Barr@uscga.edu'},
        'Jacob Bennett': {'division': 'Ethics Forum', 'email': 'Jacob.R.Bennett@uscga.edu'},
        'Jacob Braud': {'division': 'External Event Logistics', 'email': 'Jacob.M.Braud@uscga.edu'},
        'Sertonius Brown': {'division': 'Drill', 'email': 'Sertonius.O.Brown@uscga.edu'},
        'Zoey Cascio': {'division': 'External Event Communications', 'email': 'Zoey.A.Cascio@uscga.edu'},
        'Ezekiel Christian': {'division': 'OID', 'email': 'Ezekiel.N.Christian@uscga.edu'},
        'Ella Demand': {'division': 'Family Weekend', 'email': 'Ella.G.Demand@uscga.edu'},
        'Quinn Draper': {'division': 'Wellness and Readiness', 'email': 'Quinn.A.Draper@uscga.edu'},
        'Elias Duncan': {'division': 'External Event Communications', 'email': 'Elias.G.Duncan@uscga.edu'},
        'Hannah Edwards': {'division': 'Regimental Watches', 'email': 'Hannah.E.Edwards@uscga.edu'},
        'Sarah Evans': {'division': 'External Event Logistics', 'email': 'Sarah.E.Evans@uscga.edu'},
        'Ryanna Alyanna Flores': {'division': 'Wellness and Readiness', 'email': 'RyannaAlyanna.Flores.PH@uscga.edu'},
        'Isaak Fowkes': {'division': 'Watch Office/Quarterdeck', 'email': 'Isaak.W.Fowkes@uscga.edu'},
        'Lauren Granquist': {'division': 'Training and Logistics', 'email': 'Lauren.J.Granquist@uscga.edu'},
        'Tyler Henderson': {'division': 'RISO', 'email': 'Tyler.P.Henderson@uscga.edu'},
        'Connor Hernandez': {'division': 'Training and Logistics', 'email': 'Connor.O.Hernandez@uscga.edu'},
        'Jay Herndon': {'division': 'External Event Operations', 'email': 'Jay.P.Herndon@uscga.edu'},
        'Emily Holcomb': {'division': 'Ethics Forum', 'email': 'Emily.M.Holcomb@uscga.edu'},
        'Colin Jensen': {'division': 'Family Weekend', 'email': 'Colin.E.Jensen@uscga.edu'},
        'Madeline Kibler': {'division': 'Drill', 'email': 'Madeline.E.Kibler@uscga.edu'},
        'Jason Manzo': {'division': 'Family Weekend', 'email': 'Jason.R.Manzo@uscga.edu'},
        'Jonah McFarland': {'division': 'Internal Communications', 'email': 'Jonah.B.McFarland@uscga.edu'},
        'Zachary McGowen': {'division': 'Parents and Alumni Associations', 'email': 'Zachary.O.McGowen@uscga.edu'},
        'Riley Middleton': {'division': 'Morale', 'email': 'Riley.A.Middleton@uscga.edu'},
        'Thuy Nguyen': {'division': 'Company Watches and Logs', 'email': 'Thuy.P.Nguyen@uscga.edu'},
        'Nathaniel Nocerito': {'division': 'Character Development', 'email': 'Nathaniel.W.Nocerito@uscga.edu'},
        'William Pearson': {'division': 'Morale', 'email': 'William.J.Pearson@uscga.edu'},
        'Oliver Perry': {'division': 'External Event Planning', 'email': 'Oliver.M.Perry@uscga.edu'},
        'Mason Phillips': {'division': 'Company Watches and Logs', 'email': 'Mason.W.Phillips@uscga.edu'},
        'Hannah Pukish': {'division': 'RISO', 'email': 'Hannah.A.Pukish@uscga.edu'},
        'Nolan Roasa': {'division': 'External Event Planning', 'email': 'Nolan.J.Roasa@uscga.edu'},
        'Samuel Sauers': {'division': 'External Event Operations', 'email': 'Samuel.C.Sauers@uscga.edu'},
        'Zoe Schilke': {'division': 'Character Development', 'email': 'Zoe.G.Schilke@uscga.edu'},
        'Gwen Slaughter': {'division': 'Watch Office/Quarterdeck', 'email': 'Gwen.F.Slaughter@uscga.edu'},
        'Christopher Sledjeski': {'division': 'Parents and Alumni Associations','email': 'Christopher.J.Sledjeski@uscga.edu'},
        'Ty Tamborino': {'division': 'Regimental Watches', 'email': 'Ty.C.Tamborino@uscga.edu'},
        'Keegan Thompson': {'division': 'Internal Communications', 'email': 'Keegan.G.Thompson@uscga.edu'},

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
