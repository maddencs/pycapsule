import sys
sys.path.append('/home/cory/projects/pycapsule')
sys.path.append('../')
from pycapsule import PyCapsule
import unittest
from config import auth
import test_data
import json
import xml.etree.ElementTree as ET

POTATO_ID = '87910401'

class TestOrganisationMethods(unittest.TestCase):
    pc = PyCapsule('pycapsule', test_data.auth)

    def test_get_organisation(self):
        self.maxDiff = None
        potato = self.pc.organisations.get(id=POTATO_ID)
        self.assertEqual(potato.name, 'Dancing Potatoes')
        xml_potato = self.pc.organisations.get(id=POTATO_ID, return_type='xml')
        xml_potato = ET.fromstring(xml_potato)
        self.assertEqual(xml_potato.find('name').text, ET.XML(test_data.dancing_potatoes_xml).find('name').text)
        json_potato = self.pc.organisations.get(id=POTATO_ID, return_type='json')
        self.assertEqual(json_potato['organisation']['name'], test_data.dancing_potatoes_json['organisation']['name'])
        r = self.pc.organisations.all(return_type='json')
        self.assertGreater(len(r['parties']), 0)
        r = self.pc.organisations.filter()
        print(r)

    def test_add_organisation(self):
        pass

        
    

if __name__ == '__main__':
    unittest.main()
