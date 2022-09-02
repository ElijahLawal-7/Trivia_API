import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, User
from settings import DATABASE_NAME_2, DATABASE_PORT, DATABASE_OWNER, DATABASE_PASSWORD
import math
import random

BASE_URL = '/api/v0.1.0'
QUESTIONS_PER_PAGE = 3


def get_questions_by_category_id(category_id):
    questions = Question.query.filter(
        Question.category == category_id).all()

    return questions


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.trivia)

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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_200_returned_on_get_categories(self):
        ''' Test to confirm the list of categories was returned successfully '''
        res = self.client().get(f'{BASE_URL}/categories')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_400_returned_on_invalid_post_categories_request(self):
        ''' Test to confirm that the valid response was returned on passing invalid parameters for the post categories request '''
        res = self.client().post(f'{BASE_URL}/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_422_returned_for_passing_an_empty_category_value_on_create_category_post_request(self):
        ''' Test to confirm that the valid response was returned on passing invalid parameters for the post categories request '''
        res = self.client().post(
            f'{BASE_URL}/categories', json={"category": ""})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_409_returned_on_existing_category_named_passed_on_category_create_post_request(self):
        ''' Test to confirm that a 409 error is returned indicating that the category already exists and as such, the provided category conflicts with an existing one
        '''
        last_category = Category.query.order_by(
            Category.id.desc()).first().format()['type']
        res = self.client().post(
            f'{BASE_URL}/categories', json={"category": last_category})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'conflict')

    def test_201_returned_on_valid_category_create_post_request(self):
        ''' Test to confirm that a category is added successfully '''
        test_category = 'Test Category '
        last_category = Category.query.order_by(
            Category.id.desc()).first().format()['type']
        new_category = test_category if test_category not in last_category else last_category

        try:
            length = len(test_category) if test_category in new_category else len(
                last_category)
            count = int(new_category[length:])
            new_category = f'{new_category[:length]}{count + 1}'
        except:
            new_category = f'{new_category}1'

        res = self.client().post(
            f'{BASE_URL}/categories', json={"category": new_category})
        data = json.loads(res.data)
        returned_category = Category.query.order_by(Category.id.desc()).first()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['message'], "created")
        self.assertEqual(data['success'], True)
        self.assertEqual(new_category, returned_category.format()['type'])

    def test_400_returned_on_invalid_update_rating_request(self):
        ''' Test to confirm that the valid response was returned on passing passing invalid parameters for the update question rating request '''
        random_id = random.randrange(1, 1001)
        res = self.client().patch(
            f"{BASE_URL}/questions/{random_id}", json={"rating": None})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_200_returned_valid_update_rating_request(self):
        ''' Test to confirm that a questions rating was successfully updated '''
        case = Question.query.order_by(Question.id).first().format()
        initial_rating = case['rating']
        new_rating = 0

        if initial_rating >= 0 and initial_rating < 5:
            new_rating = int(initial_rating) + 1
        elif initial_rating == 5:
            new_rating = int(initial_rating) - 1
        elif initial_rating < 0:
            new_rating = 1

        res = self.client().patch(
            f"{BASE_URL}/questions/{case['id']}", json={"rating": new_rating})
        data = json.loads(res.data)
        updated_rating = Question.query.order_by(
            Question.id).first().format()['rating']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(initial_rating, updated_rating)

    def test_get_questions(self):
        ''' Test to confirm the list of questions was returned successfully '''
        res = self.client().get(f'{BASE_URL}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 0)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_returned_on_out_of_bounds_questions_page_number(self):
        ''' Test to confirm that the valid response was returned on passing invalid page argument for the get questions request '''
        question_count = Question.query.count()
        max_page = math.ceil(question_count/QUESTIONS_PER_PAGE)
        page = random.randrange(max_page+1, 1001)
        res = self.client().get(f'{BASE_URL}/questions?page={page}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_200_returned_on_valid_questions_page_number(self):
        ''' Test to confirm the list of questions was returned successfully on passing a valid page argument '''
        question_count = Question.query.count()
        max_page = math.ceil(question_count/QUESTIONS_PER_PAGE)
        page = random.randrange(1, max_page+1)
        res = self.client().get(f'{BASE_URL}/questions?page={page}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 0)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_422_returned_on_non_existent_question_id_delete_request(self):
        ''' Test to confirm that the valid response was returned on passing a question id that doesn't exist in the database for the delete question request '''
        question_id = 1
        questions = Question.query.order_by(Question.id).all()

        for question in questions:
            if not question_id == question.format()['id']:
                break
            else:
                question_id = question.id + 1

        invalid_question = Question.query.filter(
            Question.id == question_id).first()
        res = self.client().delete(f'{BASE_URL}/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")
        self.assertEqual(invalid_question, None)

    def test_200_returned_on_valid_question_id_delete_request(self):
        ''' Test to confirm that a valid response was returned for a successful question delete '''
        question_id = Question.query.order_by(
            Question.id.desc()).first().format()['id']

        deleted_question = Question.query.filter(
            Question.id == question_id).first()
        res = self.client().delete(f'{BASE_URL}/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], deleted_question.format()['id'])

    def test_400_returned_on_invalid_questions_post_request(self):
        ''' Test to confirm that the valid response was returned on passing passing invalid parameters for the post question request '''
        res = self.client().post(
            f'{BASE_URL}/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_404_returned_on_zero_search_results_found(self):
        ''' Test to confirm that the valid response was returned when no result could be found for questions search request '''
        search_term = '1two3four5six7eight9ten'
        res = self.client().post(
            f'{BASE_URL}/questions', json={"search_term": search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_422_returned_for_passing_an_empty_search_value_on_search_post_request(self):
        ''' Test to confirm that the valid response was returned on passing an empty search value for questions search request '''
        res = self.client().post(
            f'{BASE_URL}/questions', json={"search_term": ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_200_returned_on_valid_search_questions_request(self):
        ''' Test to confirm that the valid response was returned on successful question search request '''
        questions = Question.query.all()
        question = questions[random.randrange(0, len(questions))]
        question_length = len(question.format()['question'])
        lower_range = random.randrange(0, math.floor(question_length/2))
        upper_range = random.randrange(math.floor(
            question_length/2) + 1, question_length)
        # The search term is a slice of a random question in the database
        search_term = question.format()['question'][lower_range:upper_range]

        res = self.client().post(
            f'{BASE_URL}/questions', json={"search_term": search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 0)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_400_returned_on_invalid_question_create_post_request(self):
        ''' Test to confirm that the valid response was returned on passing passing invalid parameters for the post question request '''
        res = self.client().post(
            f'{BASE_URL}/questions', json={
                "question": "",
                "answer": "",
                "category": 0,
                "difficulty": 0
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_409_returned_on_existing_question_passed_on_question_create_post_request(self):
        ''' Test to confirm that a 409 error is returned indicating that the question already exists and as such, the provided question conflicts with an existing one
        '''
        last_question = Question.query.order_by(
            Question.id.desc()).first().format()
        parameters = {
            "question": last_question['question'],
            "answer": last_question['answer'],
            "category": last_question['category'],
            "difficulty": last_question['difficulty'],
            "rating": last_question['rating']
        }
        res = self.client().post(
            f'{BASE_URL}/questions', json=parameters)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'conflict')

    def test_201_returned_on_valid_question_create_post_request(self):
        ''' Test to confirm that the valid response was returned on successful post question request '''
        parameters = {
            "question": "What side effect does dynamic phototherapy have on a patient's vision?",
            "answer": "Night vision",
            "category": 1,
            "difficulty": 5,
            "rating": 5
        }
        res = self.client().post(f'{BASE_URL}/questions', json=parameters)
        data = json.loads(res.data)
        question = Question.query.order_by(Question.id.desc()).first().format()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "created")
        self.assertEqual(parameters['question'], question['question'])
        self.assertEqual(parameters['answer'], question['answer'])
        self.assertEqual(parameters['category'], question['category'])
        self.assertEqual(parameters['difficulty'], question['difficulty'])

    def test_404_returned_due_to_category_id_out_of_bounds_on_get_questions_by_category_request(self):
        ''' Test to confirm that the valid response was returned on passing passing invalid parameters for the post question request '''
        max_id = Category.query.count()
        category_id = random.randrange(max_id+1, 1001)
        res = self.client().get(
            f'{BASE_URL}/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_200_returned_on_valid_get_questions_by_category_request(self):
        ''' Test to confirm the list of questions filtered by the provided category was returned successfully '''
        categories = Category.query.order_by(Category.id).all()

        category_ids = []

        for category in categories:
            id = category.format()['id']
            if get_questions_by_category_id(category_id=id):
                category_ids.append(id)

        category_id = category_ids[random.randrange(0, len(category_ids))]

        res = self.client().get(
            f'{BASE_URL}/categories/{category_id}/questions')
        data = json.loads(res.data)
        category = Category.query.get(category_id).format()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], category['id'])

    def test_404_returned_on_invalid_get_quizzes_request(self):
        ''' Test to confirm that the valid response was returned when no result could be returned for the get quizzes request '''
        id = 1
        while get_questions_by_category_id(id):
            id = id+1
        res = self.client().post(f'{BASE_URL}/quizzes', json={
            "quiz_category": {
                "id": id
            },
            "previous_questions": []
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_400_returned_on_invalid_get_quizzes_request(self):
        ''' Test to confirm that the valid response was returned on passing passing invalid parameters for the post question request '''
        res = self.client().post(f'{BASE_URL}/quizzes', json={
            "quiz_category": {},
            "previous_questions": None
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_200_returned_on_valid_get_quizzes_request(self):
        ''' Test to confirm that a matching the rules of the quiz was returned successfully '''
        # Retrieve all available categories
        categories = Category.query.order_by(Category.id).all()

        returned_categories = {}
        # Save all categories that have questions assigned to them
        for category in categories:
            if get_questions_by_category_id(category_id=category.format()['id']):
                returned_categories[str(category.format()['id'])] = category.format()[
                    'type']

        valid_category_ids = []
        for key in returned_categories.keys():
            valid_category_ids.append(int(key))

        valid_category_id = valid_category_ids[random.randrange(
            0, len(valid_category_ids))]

        current_category = {
            "id": valid_category_id,
            "type": returned_categories[str(valid_category_id)]
        }

        questions = Question.query.filter(
            Question.category == valid_category_id).all()

        all_question_ids = [question.format()['id'] for question in questions]

        previous_questions = []
        for i in range(random.randint(0, len(questions))):
            id = all_question_ids[random.randrange(
                0, len(all_question_ids)) if len(all_question_ids) > 1 else 0]
            if id not in previous_questions:
                previous_questions.append(id)

        res = self.client().post(f'{BASE_URL}/quizzes', json={
            "quiz_category": current_category,
            "previous_questions": previous_questions
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('question' in data)
        if data['question']:
            self.assertTrue(data['question'])
            self.assertTrue(data['question']['id'] not in previous_questions)
            self.assertEqual(data['question']['category'], valid_category_id)
        else:
            self.assertEqual(len(data['question']), 0)

    def test_422_returned_for_passing_an_empty_username_value_on_create_user_post_request(self):
        ''' Test to confirm that the valid response was returned on passing invalid parameters for the post users request '''
        res = self.client().post(
            f'{BASE_URL}/users', json={"username": ""})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_409_returned_on_existing_username_passed_on_user_create_post_request(self):
        ''' Test to confirm that a 409 error is returned indicating that the user already exists and as such, the provided username conflicts with an existing one
        '''
        last_username = User.query.order_by(
            User.id.desc()).first().format()['username']
        res = self.client().post(
            f'{BASE_URL}/users', json={"username": last_username})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'conflict')

    def test_201_returned_on_valid_user_create_post_request_without_score(self):
        ''' Test to confirm that a user is added successfully without an initial score value passed '''
        test_username = 'Test User '
        last_username = User.query.order_by(
            User.id.desc()).first().format()['username']
        new_username = test_username if test_username not in last_username else last_username

        try:
            length = len(test_username) if test_username in new_username else len(
                last_username)
            count = int(new_username[length:])
            new_username = f'{new_username[:length]}{count + 1}'
        except:
            new_username = f'{new_username}1'

        res = self.client().post(
            f'{BASE_URL}/users', json={"username": new_username})
        data = json.loads(res.data)

        returned_user = User.query.order_by(User.id.desc()).first()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['message'], "created")
        self.assertEqual(data['success'], True)
        self.assertEqual(new_username, returned_user.format()['username'])

    def test_201_returned_on_valid_user_create_post_request_with_score(self):
        ''' Test to confirm that a user is added successfully with an initial score '''
        score = random.randrange(0, 1001)
        test_username = 'Test User '
        last_username = User.query.order_by(
            User.id.desc()).first().format()['username']
        new_username = test_username if test_username not in last_username else last_username

        try:
            length = len(test_username) if test_username in new_username else len(
                last_username)
            count = int(new_username[length:])
            new_username = f'{new_username[:length]}{count + 1}'
        except:
            new_username = f'{new_username}1'

        res = self.client().post(
            f'{BASE_URL}/users', json={
                "username": new_username,
                "score": score
            })
        data = json.loads(res.data)

        returned_user = User.query.order_by(User.id.desc()).first()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['message'], "created")
        self.assertEqual(data['success'], True)
        self.assertEqual(new_username, returned_user.format()['username'])
        self.assertEqual(score, returned_user.format()['score'])

    def test_400_returned_on_invalid_update_score_request(self):
        ''' Test to confirm that the valid response was returned on passing passing invalid parameters for the update user score request '''
        random_id = random.randrange(1, 1001)
        res = self.client().patch(
            f"{BASE_URL}/users/{random_id}", json={"score": None})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_200_returned_valid_update_score_request(self):
        ''' Test to confirm that a user score was successfully updated '''
        case = User.query.order_by(User.id).first().format()
        initial_score = case['score']
        new_score = 1

        res = self.client().patch(
            f"{BASE_URL}/users/{case['id']}", json={"score": new_score})
        data = json.loads(res.data)
        updated_score = User.query.order_by(
            User.id).first().format()['score']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(initial_score, updated_score)

    def test_200_returned_on_get_users(self):
        ''' Test to confirm the list of users was returned successfully '''
        res = self.client().get(f'{BASE_URL}/users')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['users'])


        # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
