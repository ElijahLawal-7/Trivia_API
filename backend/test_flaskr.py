import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category,DB_USER

DB_NAME_TEST = os.getenv('DBNAMETEST')


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_NAME_TEST
        self.database_path = "postgresql://{}@{}/{}".format(
            DB_USER, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "What is the fact of knowing something?",
                             "answer": "Science", "difficulty": "3", "category": "1"}

        self.quiz = {'previous_questions': [],
                     'quiz_category': {'type': 'Science', 'id': '1'}}
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories_success(self):
        response = self.client().get('/categories')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['categories'])

    def test_get_categories_error(self):
        response = self.client().get('/categories/1')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Resources not found')


    def test_get_questions_success(self):
        response = self.client().get('/questions?page=1')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['questions'])
        self.assertTrue(response_data['total_questions'])
        self.assertEqual(response_data['current_category'], 'Science')
        self.assertTrue(response_data['categories'])

    def test_get_questions_error(self):
        response = self.client().get('/questions?page=100')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Resources not found')


    def test_delete_questions_success(self):
        response = self.client().delete('/questions/6')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_delete_questions_error(self):
        response = self.client().delete('/questions/100')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Resources not found')


    def test_get_questions_by_category_success(self):
        response = self.client().get('/categories/5/questions')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['questions'])
        self.assertTrue(response_data['total_questions'])
        self.assertEqual(response_data['current_category'],Category.query.filter_by(id=5).one().type)

    def test_get_questions__by_category_error(self):
        response = self.client().get('/categories/100/questions')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Resources not found')


    def test_post_question_success(self):
        response = self.client().post('/questions', json=self.new_question)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_post_question_error(self):
        response = self.client().post('/questions')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Bad Request')


    def test_search_question_success(self):
        response = self.client().post(
            '/questions', json={'searchTerm': 'what'})
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['questions'])
        self.assertTrue(response_data['total_questions'])
        self.assertTrue(response_data['current_category'])

    def test_search_question_error(self):
        response = self.client().post('/questions')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Bad Request')


    def test_post_quizzes_success(self):
        response = self.client().post('/quizzes', json=self.quiz)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200, 'Here 1')
        self.assertTrue(response_data['question'], 'Here 2')
        self.assertTrue(response_data['total_questions'], 'Here 3')
        self.assertTrue(response_data['question']['question'], 'Here 4')

    def test_post_quizzes_error(self):
        response = self.client().post('/quizzes')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 400, 'There 1')
        self.assertEqual(response_data['success'], False, 'There 2')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
