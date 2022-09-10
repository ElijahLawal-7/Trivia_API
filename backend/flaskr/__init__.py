import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db
from sqlalchemy.sql.expression import func
from utils import get_random_question, format_questions
QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):

    # create and configure the app

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, DELETE')
        return response

    # Endpoint to select questions based on pagination

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        category_array = {}
        current_category_name = ''
        start = (page - 1) * 10
        end = start + 10
        questions = Question.query.all()
        category_list = Category.query.all()
        questions_count = Question.query.count()

        # Get Current Category

        currunt_cat_query = \
            db.session.query(Question).order_by(Question.id.desc()).first()
        current_cat_id = currunt_cat_query.category
        for x in category_list:
            category_array[x.id] = x.type
            if current_cat_id == x.id:
                current_category_name = x.type
        return jsonify({
            'questions': format_questions(questions)[start:end],
            'total_questions': questions_count,
            'categories': category_array,
            'current_category': current_category_name,
        })

    # Endpoint to delete questions using question ID

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def detele_question(question_id):
        Question.query.filter(Question.id == question_id).delete()
        db.session.commit()
        return jsonify({'success': True, "message": "question deleted"})

    # Endpoint to select categories

    @app.route('/categories', methods=['GET'])
    def get_category_list():
        category_list = Category.query.all()
        category_array = {}
        for x in category_list:
            category_array[x.id] = x.type
        return jsonify({'categories': category_array})

    # Endpoint to add a new question

    @app.route('/questions', methods=['POST'])
    def add_new_question():
        client_data = request.get_json()
        question = client_data['question']
        answer = client_data['answer']
        difficulty = client_data['difficulty']
        category = client_data['category']
        question_data = Question(question=question, answer=answer,
                                 difficulty=difficulty,
                                 category=category)
        db.session.add(question_data)
        db.session.commit()
        return jsonify({'success': True, 'message': 'question recorded'})

    # Endpoint to search a question

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        data = request.get_json()
        search_term = data['searchTerm']
        category_array = []
        current_category_name = ''
        search_condition = '%{0}%'.format(search_term)
        search_question = Question.query.filter(
            Question.question.ilike(search_condition)).all()
        category_list = Category.query.all()
        questions_count = Question.query.filter(
            Question.question.ilike(search_condition)).count()

        # Get current category

        currunt_cat_query = \
            db.session.query(Question).order_by(Question.id.desc()).first()
        current_cat_id = currunt_cat_query.category
        for x in category_list:
            category_array.append(x.type)
            if x.id == current_cat_id:
                current_category_name = x.type
        return jsonify({
            'questions': format_questions(search_question),
            'total_questions': questions_count,
            'categories': category_array,
            'current_category': current_category_name,
        })

    # Endpoint for selecting questions based on categories

    @app.route('/categories/<int:category_id>/questions', methods=['GET'
                                                                   ])
    def get_question_by_category(category_id):

        category_array = []
        questions = Question.query.filter(Question.category
                                          == category_id).all()
        questions_count = Question.query.filter(Question.category
                                                == category_id).count()
        category_list = Category.query.all()
        for x in category_list:
            category_array.append(x.type)
        return jsonify({
            'questions': format_questions(questions),
            'total_questions': questions_count,
            'categories': category_array,
            'current_category': category_id,
        })

    # Endpoint for quiz - selecting one random question which is not in the
    # previous question list

    @app.route('/quizzes', methods=['POST'])
    def question_quiz():
        data = request.get_json()
        previous_questions = data['previous_questions']
        quiz_category = data['quiz_category']['id']
        if quiz_category == 0:
            question_data = Question.query.order_by(func.random()).all()
        else:
            question_data = Question.query.filter(
                Question.category == quiz_category).order_by(
                func.random()).all()
        question = Question.query.get(10)
        questions_count = Question.query.filter(Question.category
                                                == quiz_category).count()
        current_question = get_random_question(
            question_data, previous_questions, questions_count)

        return current_question

    # Error handler for 422 - when the request can't be processed

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({'success': False, 'error': 422,
                'message': 'unable to process the request'}), 422)

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({'success': False, 'error': 404,
                'message': 'The requested resource is not found in this server'
                         }), 404)

    # Errorhandler for 404 - when the requested resource is not found in the
    # server

    @app.errorhandler(405)
    def not_found(error):
        return (jsonify({'success': False, 'error': 405,
                'message': 'The requested Method is not allowed'}), 405)

    # Errorhandler for 400 - when bad input detected or when the input data is
    # in wrong format

    @app.errorhandler(400)
    def not_found(error):
        return (jsonify({'success': False, 'error': 400,
                'message': 'Bad input detected'}), 400)
    return app
