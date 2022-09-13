import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, all_questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in all_questions]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response


    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.type).all()

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        })

    # Add capability to create new categories.
    @app.route("/categories", methods=['POST'])
    def store_category():
        body = request.get_json()

        if 'type' not in body:
            abort(422)

        category_type = body.get('type')

        try:
            category = Category(type=category_type)
            category.insert()

            return jsonify({
                'success': True,
                'created': category.id,
            })

        except:
            abort(422)



    @app.route('/questions')
    def list_questions():
        all_questions = Question.query.all()
        questions = paginate_questions(request, all_questions)

        if len(questions) == 0:
            abort(404)
        all_categories = Category.query.all()
        categories = {category.id: category.type for category in all_categories}

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(all_questions),
            'categories': categories,
            'current_category': None
        })


    @app.route("/questions/<question_id>", methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)

    @app.route("/questions", methods=['POST'])
    def store_question():
        body = request.get_json()

        if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
            abort(422)

        get_difficulty = body.get('difficulty')
        get_category = body.get('category')
        get_question = body.get('question')
        get_answer = body.get('answer')

        try:
            question = Question(question=get_question, answer=get_answer,
                                difficulty=get_difficulty, category=get_category)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id,
            })

        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_keyword = body.get('searchTerm', None)

        if search_keyword:
            search_results = Question.query.filter(
                Question.question.ilike(f'%{search_keyword}%')).all()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in search_results],
                'total_questions': len(search_results),
                'current_category': None
            })
        abort(404)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_question_categories(category_id):

        try:
            questions = Question.query.filter(
                Question.category == str(category_id)).all()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
                'current_category': category_id
            })
        except:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def quiz():

        try:
            body = request.get_json()
            if 'previous_questions' not in body and 'quiz_category' not in body:
                abort(422)

            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            if (quiz_category['id'] == 0):
                questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
            else:
                questions = Question.query.filter_by(category=quiz_category['id']).filter(Question.id.notin_((previous_questions))).all()

            random_new_question = questions[random.randrange(0, len(questions))].format()

            return jsonify({
                'success': True,
                'question': random_new_question
            })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app

