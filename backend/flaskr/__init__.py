import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
import sys
from models import setup_db, Question, Category, db
from sqlalchemy import func

QUESTIONS_PER_PAGE = 10


# paginate questions
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format for question in selection]
    current_question = questions[start:end]

    return current_question


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

    @app.route('/api/categories', methods=['GET', 'POST'])
    @cross_origin()
    def handle_categories():
        try:
            if request.method == 'GET':
                try:
                    selection = Category.query.order_by('id').all()
                    result = [item.format for item in selection]
                    if not result:
                        abort(400)
                    return jsonify({
                        'success': True,
                        'categories': result,
                        'total_categories': len(Category.query.all())
                    })
                except():
                    abort(500)

            if request.method == 'POST':
                error = False

                data = request.get_json()

                new_category = Category(
                    type=data.get('type', None),
                )

                if not new_category.type:
                    abort(400)

                # check if existed
                duplicate_category = Category.query.filter(Category.type == new_category.type).all()

                if bool(duplicate_category):
                    abort(409)

                try:
                    db.session.add(new_category)
                    db.session.commit()
                except():
                    error = True
                    print(sys.exc_info())
                    abort(400)

                selection = Category.query.order_by('id').all()
                result = [item.format for item in selection]

                return jsonify({
                    'success': True,
                    'created': new_category.id,
                    'category created': new_category.type,
                    'categories': result,
                    'total_categories': len(Category.query.all())
                }), 201

        except():
            abort(500)

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    @app.route('/api/questions', methods=['GET'])
    @cross_origin()
    def get_all_questions():
        try:
            selection = Question.query.order_by('id').all()
            result = [item.format for item in selection]
            page = request.args.get('page')

            if page:
                paginated_result = paginate_questions(request, selection)
            else:
                paginated_result = result

            categories = Category.query.order_by('id').all()
            format_categories = [item.format for item in categories]

            return jsonify({
                'success': True,
                'questions': paginated_result,
                'total_questions': len(selection),
                'current_category': None,
                'categories': format_categories
            })
        except():
            return abort(500)

    '''
    Get questions by id
    '''

    @app.route('/api/questions/<int:question_id>', methods=['GET'])
    @cross_origin()
    def get_question_by_id(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)
            result = question.format
            return jsonify({
                'success': True,
                'question': result
            })
        except():
            abort(400)

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    @cross_origin()
    def delete_question_by_id(question_id):
        try:
            question = Question.query.get(question_id)

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by('id').all()
            result = [item.format for item in selection]
            paginate_result = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question.id,
                'questions': paginate_result,
                'total_questions': len(selection)
            })

        except():
            abort(422)

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route('/api/questions', methods=['POST'])
    @cross_origin()
    def add_question():
        error = False
        # Declare and empty data dictionary to hold all retrieved variables
        data = request.get_json()

        # set question variable equal to corresponding model class,
        # ready for adding to the session
        new_question = Question(
            question=data.get('question', None),
            answer=data.get('answer', None),
            difficulty=data.get('difficulty', None),
            category=data.get('category', None)
        )

        if not new_question.question:
            abort(400)

        new_question_list = new_question.format

        del new_question_list['id']

        for key in list(new_question_list):
            if new_question_list[key] is None:
                abort(400)

        try:
            db.session.add(new_question)
            db.session.commit()
        except():
            error = True
            print(sys.exc_info())
            abort(400)

        selection = Question.query.order_by('id').all()
        paged_questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'created': new_question.id,
            'questions': paged_questions,
            'total_questions': len(selection)
        }), 201

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    @app.route('/api/questions/search', methods=['POST'])
    @cross_origin()
    def search_questions():
        try:
            body = request.get_json()
            search_term = body.get('search', None)

            if body == {}:
                abort(422)

            # question search
            if search_term is not None:
                search = "{}".format(search_term.lower())

                search_results = Question.query.filter(
                    Question.question.ilike('%' + search + '%')).all()

                formatted_search_results = [question.format for question in search_results]

                if search_results is None:
                    abort(404)

                paginated_results = paginate_questions(request, search_results)

                return jsonify({
                    'success': True,
                    'questions': paginated_results,
                    'total_questions': len(search_results)
                }), 200
        except():
            abort(400)

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/api/categories/<int:category_id>/questions', methods=['GET'])
    @cross_origin()
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(
                Question.category == str(category_id)).all()

            category = Category.query.get(str(category_id))

            get_all_cat = Category.query.order_by('id').all()
            formatted_category = [item.format for item in get_all_cat]

            if category_id < 1 or category is None:
                abort(404)

            if questions is None:
                total_questions = 0
                paginated_questions = []
            else:
                total_questions = [question.format for question in questions]
                paginated_questions = paginate_questions(
                    request, questions)

            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(total_questions),
                'current_category': Category.query.get(str(category_id)).format,
                'categories': formatted_category
            })

        except():
            abort(500)

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @app.route('/api/play_quizzes', methods=['POST'])
    @cross_origin()
    def play_quiz():
        try:
            body = request.get_json()

            if body.get('quiz_category') is None or body.get('previous_questions') is None:
                abort(422)

            quiz_category_id = body.get('quiz_category', None)['id']
            previous_questions = body.get('previous_questions', None)

            if quiz_category_id == 0:
                questions = Question.query.order_by(func.random()).all()
            else:
                questions = Question.query. \
                    filter(
                    Question.category == quiz_category_id). \
                    order_by(func.random()).all()

            formatted_questions = [question.format for question in questions]
            available_questions = []
            for q in formatted_questions:
                if len(previous_questions) == 0:
                    available_questions.append(q)
                elif len(previous_questions) >= 0:
                    found = q['id'] not in previous_questions
                    if found is True:
                        available_questions.append(q)

            if len(available_questions) > 0:
                return jsonify({
                    'success': True,
                    'question': available_questions[0]
                })
            else:
                return jsonify({
                    'success': True,
                    'question': None
                })
        except():
            abort(422)

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def not_processable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(405)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 450,
            "message": "no such method"
        }), 405

    @app.errorhandler(409)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 409,
            "message": "resource existed"
        }), 409

    return app

# Inspired by https://github.com/czarjulius
# Inspired by  https://github.com/GerrardE
