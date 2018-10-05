import unittest
from bg_similarity import app


class BGSimilarityTests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        app.config['TESTING'] = True
        # executed after each test
    def tearDown(self):
        pass
    ###############
    #### tests ####
    ###############
    def test_main(self):
        test_payload = {
            'bgg_id': '173064',
            'top_n': '5'
        }
        response = self.app.post(
            '/bg_similarity',
            data=test_payload
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
