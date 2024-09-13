import json
import os
import win32com.client as win32

#PAIRS_FILE = 'generated_pairs1.json'

# Load the participants data (the same as in the first part)
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
