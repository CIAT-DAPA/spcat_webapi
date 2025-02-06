import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from api import app
from ormgap import Project
from mongoengine import connect

class ProjectsEndpointTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test database and API client"""
        connect('test_gap_analysis', host='mongomock://localhost')
        Project.drop_collection()
        
        # Create test projects
        cls.project1 = Project(name='Project Alpha', ext_id='PA123').save()
        cls.project2 = Project(name='Project Beta', ext_id='PB456').save()
        cls.project3 = Project(name='Project Gamma', ext_id='PG789').save()

        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        Project.drop_collection()

    def test_get_projects(self):
        """Test GET /api/v1/projects endpoint"""
        response = self.app.get('/api/v1/projects')
        
        # Check response status
        self.assertEqual(response.status_code, 200)
        
        # Verify response data
        self.assertEqual(len(response.json), 3)
        self.assertEqual(response.json[0]['name'], 'Project Alpha')
        self.assertEqual(response.json[1]['name'], 'Project Beta')
        self.assertEqual(response.json[2]['name'], 'Project Gamma')


if __name__ == '__main__':
    unittest.main()
