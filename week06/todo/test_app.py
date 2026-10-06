import unittest
import os
import sqlite3
from app import app
from contextlib import closing
class TodoAppTestCase(unittest.TestCase):
    def setUp(self):
        import app as app_module
        self.original_db = app_module.DATABASE
        self.test_db = 'test_database.db'
        app_module.DATABASE = self.test_db
        
        self.app = app.test_client()
        self.app.testing = True
        
        with closing(sqlite3.connect(self.test_db)) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL
                )
            ''')
            conn.commit()

    def tearDown(self):
        import app as app_module
        app_module.DATABASE = self.original_db
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_get_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_valid_title(self):
        response = self.app.post('/add', data={'title': 'Test Task'}, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        response = self.app.get('/')
        self.assertIn(b'Test Task', response.data)

    def test_add_exact_100_chars(self):
        title = 'a' * 100
        response = self.app.post('/add', data={'title': title}, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        response = self.app.get('/')
        self.assertIn(title.encode(), response.data)

    def test_add_empty_string(self):
        # SPEC says 200 OK, but current app.py uses redirect (302)
        # I will write test according to SPEC (200)
        response = self.app.post('/add', data={'title': ''}, follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def test_add_whitespace_only(self):
        response = self.app.post('/add', data={'title': '   '}, follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def test_add_too_long(self):
        title = 'a' * 101
        response = self.app.post('/add', data={'title': title}, follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def test_add_order(self):
        self.app.post('/add', data={'title': 'first-item'})
        self.app.post('/add', data={'title': 'second-item'})
        response = self.app.get('/')
        pos_second = response.data.find(b'second-item')
        pos_first = response.data.find(b'first-item')
        self.assertTrue(pos_second < pos_first)


    def test_toggle_existing_id(self):
        self.app.post('/add', data={'title': 'Toggle Task'})
        response = self.app.post('/toggle/1', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        
        # Check if toggled (from False to True)
        response = self.app.get('/')
        self.assertIn(b'class="completed"', response.data)

    def test_toggle_nonexistent_id(self):
        response = self.app.post('/toggle/999', follow_redirects=False)
        self.assertEqual(response.status_code, 404)


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TodoAppTestCase)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if result.wasSuccessful():
        print(f"모든 테스트 통과 ({result.testsRun}개)")
    else:
        print("\n테스트 실패:")
        for failure in result.failures:
            print(f"Failure: {failure[0]}\n{failure[1]}")
        for error in result.errors:
            print(f"Error: {error[0]}\n{error[1]}")

if __name__ == '__main__':
    run_tests()
