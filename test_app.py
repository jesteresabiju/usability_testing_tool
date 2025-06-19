import unittest
from app import app, tasks, current_index, results

class UsabilityToolTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.secret_key = 'test_secret_key'
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Start Testing', response.data)

    def test_task_page(self):
        global current_index, results
        current_index = 0
        results.clear()
    
        # Start from home page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
        # Start the test (simulate clicking start button)
        response = self.client.get('/task', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Perform the task', response.data)

    def test_summary_page(self):
        global results
        results.clear()
        results.extend([{
            'task': 'Example task',
            'time_taken': 5,
            'success': True,
            'start_time': 1748865600,
            'end_time': 1748865605
        } for _ in range(len(tasks))])

        response = self.client.get('/summary')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Usability Test Summary', response.data)

    def test_download_csv(self):
        global results
        results.clear()
        results.extend([{
            'task': 'Example task',
            'time_taken': 5,
            'success': True,
            'start_time': 1748865600,
            'end_time': 1748865605
        } for _ in range(len(tasks))])

        response = self.client.get('/download')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content_type.startswith('text/csv'))

    def test_submit_task(self):
        global current_index, results
        current_index = 0
        results.clear()

        for _ in range(len(tasks)):
            data = {
                'success': 'y',
                'start_time': 1748865600,
                'end_time': 1748865605
            }
            response = self.client.post('/task', data=data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Usability Test Summary', response.data)


if __name__ == '__main__':
    unittest.main()
