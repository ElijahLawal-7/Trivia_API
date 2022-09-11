import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):

    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'postgres'
        self.database_path = \
            'postgresql://postgres:@{}/{}'.format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create all tables

            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""

        pass

    def test_get_random_question(self):
        res = self.client().post('/quizzes',
                                 json={'previous_questions': [],
                                       'quiz_category': {'type': 'Geography',
                                                         'id': '3'}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_get_category_list(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])

    def test_delete_question(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertEqual(data['message'], "question deleted")

    def test_add_new_question(self):
        res = self.client().post(
            '/questions',
            json={
                'question': "test",
                'answer': "test",
                "difficulty": 2,
                "category": 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertEqual(data['message'], "question recorded")

    def test_search_questions(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': "searchTerm"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data), 4)

    def test_get_question_by_category(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data), 4)

# Make the tests conveniently executable


if __name__ == '__main__':
    unittest.main()
