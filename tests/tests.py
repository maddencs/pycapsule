import sys
sys.path.append('/home/cory/projects/pycapsule')
from pycapsule import PyCapsule
import unittest
from config import auth
import test_data
import json

POTATO_ID = '87910401'

class TestOrganisationMethods(unittest.TestCase):
    def test_get_organisation(self):
        pc = PyCapsule('pycapsule', test_data.auth)
        potato = pc.organisations.get(id=POTATO_ID)
        self.assertEqual(potato.name, 'Dancing Potatoes')
        xml_potato = pc.organisations.get(id=POTATO_ID, return_type='xml')
        self.assertEqual(xml_potato, test_data.dancing_potatoes_xml)
        json_potato = pc.organisations.get(id=POTATO_ID, return_type='json')
        self.assertEqual(sorted(json_potato.items()), sorted(test_data.dancing_potatoes_json.items()))


if __name__ == '__main__':
    unittest.main()
