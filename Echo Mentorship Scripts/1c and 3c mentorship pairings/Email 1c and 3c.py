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
        'Isaac Adkins': {'division': 'Regimental Watches', 'email': 'Isaac.H.Adkins@uscga.edu'},
        'Abraham Al-Khalili': {'division': 'Wellness and Readiness', 'email': 'Abraham.K.AlKhalili@uscga.edu'},
        'Raniah Andrianjafimahery': {'division': 'External Event Logistics','email': 'Raniah.B.Andrianjafimahery@uscga.edu'},
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
