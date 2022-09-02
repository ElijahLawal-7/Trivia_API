import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import math
import random

from models import setup_db, Question, Category, User

QUESTIONS_PER_PAGE = 3
BASE_URL = '/api/v0.1.0'
error = 0
question_count = 0


def set_error_code(code):
    global error
    error = code


def get_error_code():
    global error
    return error


def get_paginated_questions(page=1, q_per_page=QUESTIONS_PER_PAGE, search_term=None, category_id=None):
    global question_count

    query = Question.query

    if search_term is not None:
        query = query.filter(Question.question.ilike(f'%{search_term}%'))
        if query.count() == 0:
            return None

    if category_id is not None and not category_id == 0:
        query = query.filter(Question.category == category_id)
        if query.count() == 0:
            return None

    question_count = query.count()

    query = query.order_by(Question.id).offset(
        (page-1)*q_per_page).limit(q_per_page).all()

    return query


def get_categories(for_quiz=False):
    categories = Category.query.order_by(Category.id).all()

    formatted_categories = {}

    for category in categories:
        if for_quiz:
            if get_paginated_questions(category_id=category.format()['id']) is not None:
                formatted_categories[str(category.format()['id'])] = category.format()[
                    'type']
        else:
            formatted_categories[str(category.format()['id'])] = category.format()[
                'type']

    return formatted_categories


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"{BASE_URL}/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route(f"{BASE_URL}/categories")
    def retrieve_categories():
        try:
            categories = get_categories(
                for_quiz=request.args.get("quiz", False, type=bool))

            return jsonify({
                "success": True,
                "categories": categories
            })
        except:
            abort(500)

    @app.route(f'{BASE_URL}/categories', methods=['POST'])
    def create_category():
        try:
            try:
                set_error_code(400)
                incoming_category = request.get_json()['category']
                if incoming_category == '':
                    set_error_code(422)
                    raise
            except:
                raise

            category = Category.query.filter(
                Category.type.ilike(str(incoming_category))).first()

            if category is None:
                new_category = Category(type=request.get_json()['category'])
                new_category.insert()

                return (jsonify({
                    "status_code": 201,
                    "success": True,
                    "message": "created"
                }), 201)
            else:
                set_error_code(409)
                raise
        except:
            abort(get_error_code())

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route(f'{BASE_URL}/questions')
    def retrieve_questions():
        try:
            page = request.args.get('page', 1, type=int)
            questions = get_paginated_questions(
                page=page)

            if not questions:
                raise

            return_questions = []
            for question in questions:
                return_questions.append(question.format())
            return jsonify({
                "success": True,
                "questions": return_questions,
                "total_questions": question_count,
                "categories": get_categories(),
                "current_category": 0
            })
        except:
            abort(404)
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route(f'{BASE_URL}/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()

            return jsonify({
                "success": True,
                "deleted_id": question.format()['id'],
            })
        except:
            abort(422)

    @app.route(f'{BASE_URL}/questions', methods=['POST'])
    def create_or_search_questions():
        if request.get_json() and "search_term" in request.get_json():
            """
            @TODO:
            Create a POST endpoint to get questions based on a search term.
            It should return any questions for whom the search term
            is a substring of the question.

            TEST: Search by any phrase. The questions list will update to include
            only question that include that string within their question.
            Try using the word "title" to start.
            """
            if request.get_json()["search_term"] == '':
                abort(422)
            try:
                search_term = request.get_json()["search_term"]
                page = request.args.get('page', 1, type=int)
                questions = get_paginated_questions(
                    search_term=search_term, page=page)

                if not questions:
                    raise

                return_questions = []
                for question in questions:
                    return_questions.append(question.format())
                return jsonify({
                    "success": True,
                    "questions": return_questions,
                    "total_questions": question_count,
                    "current_category": 0
                })
            except:
                abort(404)
        else:
            """
            @TODO:
            Create an endpoint to POST a new question,
            which will require the question and answer text,
            category, and difficulty score.

            TEST: When you submit a question on the "Add" tab,
            the form will clear and the question will appear at the end of the last page
            of the questions list in the "List" tab.
            """
            set_error_code(400)
            try:
                data = request.get_json()
                try:
                    question = data['question']
                    answer = data['answer']
                    category = int(data['category'])
                    difficulty = int(data['difficulty'])
                    rating = int(data['rating'])
                except:
                    raise

                if not (question and answer and category and difficulty):
                    raise

                case_question = Question.query.filter(
                    Question.question.ilike(str(question))).first()

                if case_question is None:
                    new_question = Question(
                        question=question,
                        answer=answer,
                        category=category,
                        difficulty=difficulty,
                        rating=rating
                    )
                    new_question.insert()

                    return (jsonify({
                        "status_code": 201,
                        "success": True,
                        "message": "created"
                    }), 201)
                else:
                    set_error_code(409)
                    raise
            except:
                abort(get_error_code())

    @app.route(f'{BASE_URL}/questions/<int:id>', methods=['PATCH'])
    def update_rating(id):
        set_error_code(500)
        try:
            question = Question.query.get(id)

            try:
                question.rating = int(request.get_json()['rating'])
            except:
                set_error_code(400)
                raise

            question.update()
            return jsonify({
                "success": True
            })
        except:
            abort(get_error_code())

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route(f'{BASE_URL}/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        try:
            page = request.args.get('page', 1, type=int)
            questions = get_paginated_questions(
                category_id=category_id, page=page)

            if not questions:
                raise

            return_questions = []
            for question in questions:
                return_questions.append(question.format())
            return jsonify({
                "success": True,
                "questions": return_questions,
                "total_questions": question_count,
                "current_category": Category.query.get(category_id).format()['id']
            })
        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.    

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route(f'{BASE_URL}/quizzes', methods=['POST'])
    def load_quiz():
        set_error_code(500)
        try:
            try:
                # Confirm that the request has the right parameters then assign it to variables
                category_id = request.get_json()['quiz_category']['id']
                previous_questions = request.get_json()['previous_questions']
            except:
                set_error_code(400)
                raise

            # Guard to return a 404 error if the category provided does not have questions assigned to it
            test_question = Question.query.filter(
                Question.category == category_id).first()
            if test_question is None and category_id != 0:
                set_error_code(404)
                raise

            # Guard to return an empty dictionary if the amount of questions already attempted is equal to the amount of questions available for that category, or more than, due to an error in the client's request
            if not category_id == 0 and Question.query.filter(Question.category == category_id).count() <= len(previous_questions):
                return jsonify({
                    "success": True,
                    "question": {},
                })

            # Attempt to retrieve questions based on the category id provided
            upper_range = Question.query.order_by(
                Question.id.desc()).first().format()['id'] + 1

            q = None
            while q is None or q.format()['id'] in previous_questions:
                rand_id = random.randrange(1, upper_range)
                q = Question.query.get(rand_id) if category_id == 0 else Question.query.filter(
                    Question.id == rand_id, Question.category == category_id).first()

            return jsonify({
                "success": True,
                "question": q.format(),
            })
        except:
            abort(get_error_code())

    @app.route(f'{BASE_URL}/users')
    def get_users():
        try:
            users = User.query.order_by(User.id).all()
            return_users = [user.format() for user in users]

            return jsonify({
                "success": True,
                "users": return_users
            })
        except:
            abort(500)

    @app.route(f'{BASE_URL}/users/<int:id>', methods=['PATCH'])
    def update_user_score(id):
        try:
            user = User.query.get(id)
            user.score = user.score + int(request.get_json()['score'])
            user.update()
            return jsonify({
                "success": True,
                "score": user.score
            })
        except:
            abort(400)

    @app.route(f'{BASE_URL}/users', methods=['POST'])
    def create_user():
        set_error_code(500)
        try:
            try:
                set_error_code(400)
                incoming_username = request.get_json()['username']
                if incoming_username == '':
                    set_error_code(422)
                    raise
            except:
                raise

            user = User.query.filter(
                User.username.ilike(str(incoming_username))).first()

            if user is None:
                new_user = User(username=request.get_json()['username'], score=int(request.get_json()[
                                'score']) if 'score' in request.get_json() else 0)
                new_user.insert()

                return (jsonify({
                    "status_code": 201,
                    "success": True,
                    "message": "created"
                }), 201)
            else:
                set_error_code(409)
                raise
        except:
            abort(get_error_code())

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 400,
                    "message": "bad request",
                }
            ),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 404,
                    "message": "resource not found",
                }
            ),
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 405,
                    "message": "method not allowed"
                }
            ),
            405,
        )

    @app.errorhandler(409)
    def conflict(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 409,
                    "message": "conflict",
                }
            ),
            409,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "unprocessable",
                }
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 500,
                    "message": "internal server error"
                }
            ),
            500,
        )

    return app
