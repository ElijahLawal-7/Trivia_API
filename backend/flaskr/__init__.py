import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# A function to format and paginate list into a group of QUESTIONS_PER_PAGE
def paginate_query(request, query):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = QUESTIONS_PER_PAGE + start

    formatted_questions = [question.format() for question in query]
    returned_questions = formatted_questions[start:end]

    return returned_questions

# A funtion to format all_categories
def format_categories():
    # Getting all categories from the database
    all_categories = Category.query.order_by(Category.id).all()

    # Formatting all categories as a JSON object.
    formatted_categories = [category.format()
                            for category in all_categories]

    #  Converting the list of objects to a single object.
    categories = {}
    for category in formatted_categories:
        categories.update(category)

    return categories

# Creating a Flask Application
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # Basic CORS setup
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add("Allow-Control-Allow-Headers",
                             "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET,PUT,POST,DELETE,OPTIONS")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_all_categories():

        # A function call to format all categories
        format_categories()

        # If there are no categories, abort.
        if len(format_categories()) == 0:
            abort(404)
        else:
            return jsonify({
                'categories': format_categories()
            })

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
    @app.route('/questions', methods=['GET'])
    def get_questions():
        # Getting all question from the database
        all_questions = Question.query.order_by(Question.id).all()

        # Paginating question in group of QUESTIONS_PER_PAGE (10)
        questions = paginate_query(request, all_questions)

        # A function call to format all categories
        format_categories()

        # Getting the current category
        current_category = Category.query.filter_by(id=1).one()

        # Checking if there is/are questions
        if len(questions) == 0:
            abort(404)

        return jsonify({
            'questions': questions,
            'total_questions': len(all_questions),
            'current_category': current_category.type,
            'categories': format_categories()

        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            # Querying the database using the given question id
            question = Question.query.filter_by(id=question_id).one_or_none()

            # Checking if question exist
            if question:
                # Deleting a question by calling the delete method
                question.delete()

                return jsonify({
                    'success': True
                })
            else:
                abort(404)
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    # HERE

    @app.route('/questions', methods=['POST'])
    def create_question():
        # Getting the request body
        body = request.get_json()

        # Fetching details from the body to create a new question
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)

        # Fetching details from the body to search for question(s)
        searched_question = body.get('searchTerm', None)

        try:
            # Checking if the client aim to search for questions
            if searched_question:
                matched_questions = Question.query.filter(
                    Question.question.ilike(f'%{searched_question}%')).all()

                formatted_matched_questions = paginate_query(
                    request, matched_questions)

                # Getting the current category
                category_id = formatted_matched_questions[0]['category']

                current_category = Category.query.filter_by(
                    id=category_id).one_or_none()

                return jsonify({
                    'questions': formatted_matched_questions,
                    'total_questions': len(matched_questions),
                    'current_category': current_category.type
                })

            else:  # This will be executed if the client aim to create a new question
                new_question = Question(
                    question=question, answer=answer, difficulty=difficulty, category=category)

                # Creating a new question by calling the insert  method
                new_question.insert()

                return jsonify({
                    'success': True
                })
        except:
            abort(400)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    # Combined with the previous post method

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        # Querying the database
        questions = Question.query.filter_by(category=category_id).all()

        # Checking if there are questions fo the selected category
        if len(questions) == 0:
            abort(404)

        # Formathing and paginating questions of the selected category
        formatted_questions = paginate_query(request, questions)

        # Getting the current category
        current_category = Category.query.filter_by(id=category_id).one()

        return jsonify({
            'questions': formatted_questions,
            'total_questions': len(questions),
            'current_category': current_category.type
        })

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

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        try:
            # Getting the request body details
            previous_question = request.get_json()['previous_questions']
            category = request.get_json()['quiz_category']

            # Checking if a catetegory or all categories are selected.
            if int(category['id']) == 0:
                questions = Question.query.order_by(Question.id).all()
            else:
                questions = Question.query.filter_by(
                    category=category['id']).all()

            # Checking if there are previous questions
                # This will be executed the first time as there are no previous questions yet
            if len(previous_question) == 0:
                data = {
                    'id': questions[0].id,
                    'question': questions[0].question,
                    'difficulty': questions[0].difficulty,
                    'category': questions[0].category,
                    'answer': questions[0].answer,
                }
                # This will be executed after the first time as there are now previous question.
            else:
                new_questions = []
                for question in questions:
                    if question.id in previous_question:
                        continue
                    new_questions.append({
                        'id': question.id,
                        'question': question.question,
                        'difficulty': question.difficulty,
                        'category': question.category,
                        'answer': question .answer,
                    })
                # Generating a random number between 0 and length of new questions
                random_number = random.randint(0, len(new_questions) - 1)
                data = new_questions[random_number]

            return jsonify({
                'question': data,
            })

        except:
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
