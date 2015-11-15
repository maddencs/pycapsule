import sys
sys.path.append('/home/cory/projects/pycapsule')
sys.path.append('..')
from pycapsule import PyCapsule
import unittest
from config import auth
import test_data
import json
import xml.etree.ElementTree as ET

POTATO_ID = '92637038'

class TestOrganisationMethods(unittest.TestCase):
    pc = PyCapsule('pycapsule', test_data.auth)


    def test_organisation_get(self):
        self.maxDiff = None

        # Testing getting a PyCapsuleObject back
        potato = self.pc.organisations.get(id=POTATO_ID)
        self.assertEqual(potato.name, 'Google Inc') 

        # Testing getting getting xml back 
        xml_potato = self.pc.organisations.get(id=POTATO_ID, return_type='xml')
        xml_potato = ET.fromstring(xml_potato)
        self.assertEqual(xml_potato.find('name').text, 'Google Inc')

        #Testing getting JSON back
        json_potato = self.pc.organisations.get(id=POTATO_ID, return_type='json')
        self.assertEqual(json_potato['organisation']['name'], 'Google Inc')


    def test_organisations_filter(self):
        # Testing getting list of PyCapsuleObjects
        r = self.pc.organisations.filter(name='Google')
        self.assertGreater(len(r['organisation']), 0)
        self.assertTrue('Google Inc' in r['organisation'][0].name)

        # Testing getting XML back
        r = self.pc.organisations.filter(name='Google Inc', return_type='xml')
        r = ET.fromstring(r)
        r = list(filter(lambda x: x.tag != 'person', r))
        name = r[0].find('name').text
        self.assertTrue('Google Inc' in name)

        # Testing getting JSON back
        r = self.pc.organisations.filter(name='Google', return_type='json')
        self.assertTrue('Google Inc' in r['parties']['organisation'][0]['name'])


    def test_organisations_all(self):
        all_orgs = self.pc.organisations.all(return_type='json')
        self.assertGreater(len(all_orgs['parties']), 0)


    def test_organisations_update(self):
        potato = self.pc.organisations.get(id=POTATO_ID)
        potato.update(data='<organisation><name>Dancing Lasagna</name></organisation>', data_type='xml')
        potato = self.pc.organisations.get(id=POTATO_ID)
        self.assertEqual(potato.name, 'Dancing Lasagna')
        potato.update(data='<organisation><name>Google Inc</name></organisation>', data_type='xml')
        

    def test_organisation_add(self):
        import re
        with open('mountain_view.xml') as f:
            location = self.pc.organisations.add(f.read(), data_type='xml')
            self.assertTrue(re.match('https://[\w\d]*.[\w\d]*.com/api/party/\d*', location))


    def test_organisation_delete(self):
        org = self.pc.organisations.all()['organisation'][0]
        org_id = org.id
        org.delete()
        same_org = self.pc.organisations.get(id=org_id)
        self.assertEqual(same_org, None)


class TestPersonMethods(unittest.TestCase):
    pc = PyCapsule('pycapsule', test_data.auth)

    def test_person_get(self):
        #Testing getting PyCapsuleObject
        party = self.pc.parties.get(id=87828377)
        self.assertEqual(party.firstName, 'Cory')

        #Testing getting XML
        party = self.pc.parties.get(id=87828377, return_type='xml')
        party = ET.fromstring(party)
        self.assertEqual(party.find('firstName').text, 'Cory')

        #Testing getting JSON
        party = self.pc.parties.get(id=87828377, return_type='json')
        self.assertEqual(party['person']['firstName'], 'Cory')


    def test_person_filter(self):
        # Testing getting list of PyCapsuleObjects
        r = self.pc.parties.filter(firstName='Cory')
        self.assertGreater(len(r['person']), 0)
        self.assertEqual('Cory', r['person'][0].firstName)

        # Testing getting XML back
        r = self.pc.parties.filter(name='Cory', return_type='xml')
        r = ET.fromstring(r)
        r = list(filter(lambda x: x.tag != 'organisation', r))
        name = r[0].find('firstName').text
        self.assertEqual(name, 'Cory')

        # Testing getting JSON back
        r = self.pc.parties.filter(name='Cory', return_type='json')
        self.assertEqual('Cory', r['parties']['person']['firstName'])


    def test_person_all(self):
        all_people = self.pc.parties.all(return_type='json')
        self.assertGreater(len(all_people['parties']['person']), 0)


    def test_person_update(self):
        party = self.pc.parties.get(id=87828377)
        party.update(data='<person><firstName>John</firstName></person>', data_type='xml')
        party = self.pc.parties.get(id=87828377)
        self.assertEqual(party.firstName, 'John')
        party.update(data='<person><firstName>Cory</firstName></person>', data_type='xml')
        

    def test_person_add(self):
        import re
        with open('schmidt.xml') as f:
            location = self.pc.parties.add(f.read(), data_type='xml')
            self.assertTrue(re.match('https://[\w\d]*.[\w\d]*.com/api/party/\d*', location))


    def test_organisation_delete(self):
        person = self.pc.parties.all()['person'][1]
        print(person.__dict__)
        person_id = person.id
        person.delete()
        same_person = self.pc.parties.get(id=person_id)
        self.assertEqual(same_person, None)

        


    

if __name__ == '__main__':
    unittest.main()
