import json
import os
import win32com.client as win32

#PAIRS_FILE = 'generated_pairs1.json'

# Load the participants data (the same as in the first part)
participants = {
    'Group1': {
        'Isaac Adkins': {'division': 'Regimental Watches', 'email': 'Isaac.H.Adkins@uscga.edu'},
        'Abraham Al-Khalili': {'division': 'Wellness and Readiness', 'email': 'Abraham.K.AlKhalili@uscga.edu'},
        'Raniah Andrianjafimahery': {'division': 'External Event Logistics', 'email': 'Raniah.B.Andrianjafimahery@uscga.edu'},
        'Tessa Breitbart': {'division': 'Family Weekend', 'email': 'Tessa.G.Breitbart@uscga.edu'},
        'Thomas Butler': {'division': 'External Event Communications', 'email': 'Thomas.D.Butler@uscga.edu'},
        'Ramon Cruz': {'division': 'Morale', 'email': 'Ramon.M.Cruz@uscga.edu'},
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
        'Sandra Kirvelevicius': {'division': 'Family Weekend', 'email': 'Sandra.H.Kirvelevicius@uscga.edu'},
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
        'Christopher Sledjeski': {'division': 'Parents and Alumni Associations', 'email': 'Christopher.J.Sledjeski@uscga.edu'},
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
