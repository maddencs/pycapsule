import sys
sys.path.append('/home/cory/projects/pycapsule')
sys.path.append('..')
from pycapsule import PyCapsule
import unittest
from config import auth
import test_data
import json
import xml.etree.ElementTree as ET

POTATO_ID = '87910401'

class TestOrganisationMethods(unittest.TestCase):
    pc = PyCapsule('pycapsule', test_data.auth)

    def test_organisation_get(self):
        self.maxDiff = None
        # Testing getting a PyCapsuleObject back
        potato = self.pc.organisations.get(id=POTATO_ID)
        self.assertEqual(potato.name, 'Dancing Potatoes') 
        # Testing getting getting xml back 
        xml_potato = self.pc.organisations.get(id=POTATO_ID, return_type='xml')
        xml_potato = ET.fromstring(xml_potato)
        self.assertEqual(xml_potato.find('name').text, ET.XML(test_data.dancing_potatoes_xml).find('name').text)
        #Testing getting JSON back
        json_potato = self.pc.organisations.get(id=POTATO_ID, return_type='json')
        self.assertEqual(json_potato['organisation']['name'], test_data.dancing_potatoes_json['organisation']['name'])

    def test_organisations_filter(self):
        # Testing getting list of PyCapsuleObjects
        r = self.pc.organisations.filter(name='Dancing')
        self.assertGreater(len(r['organisations']), 0)
        self.assertTrue('Dancing' in r['organisations'][0].name)
        # Testing getting XML back
        r = self.pc.organisations.filter(name='Dancing', return_type='xml')
        r = ET.fromstring(r)
        r = list(filter(lambda x: x.tag != 'person', r))
        name = r[0].find('name').text
        self.assertTrue('Dancing' in name)
        # Testing getting JSON back
        r = json.loads(self.pc.organisations.filter(name='Dancing', return_type='json').decode('utf-8'))
        self.assertTrue('Dancing' in r['parties']['organisation'][0]['name'])

    def test_organisations_all(self):
        all_orgs = self.pc.organisations.all(return_type='json')
        self.assertGreater(len(all_orgs['parties']), 0)

    def test_organisations_update(self):
        potato = self.pc.organisations.get(id=POTATO_ID)
        potato.update(data='<organisation><name>Dancing Lasagna</name></organisation>', data_type='xml')
        potato = self.pc.organisations.get(id=POTATO_ID)
        self.assertEqual(potato.name, 'Dancing Lasagna')
        potato.update(data='<organisation><name>Dancing Potatoes</name></organisation>', data_type='xml')
        
    def test_organisation_add(self):
        import re
        with open('mountain_view.xml') as f:
            location = self.pc.organisations.add(f.read(), data_type='xml')
            self.assertTrue(re.match('https://[\w\d]*.[\w\d]*.com/api/party/\d*', location))

    def test_organisation_delete(self):
        """
        NOT PASSING
        """
        org = self.pc.organisations.all()['organisations'][0]
        print(org)
        org_id = org.id
        org.delete()
        same_org = self.pc.organisations.get(id=org_id)
        self.assertEqual(same_org, None)


        
    

if __name__ == '__main__':
    unittest.main()
