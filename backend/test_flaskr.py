import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'tosinakinyele', 'psql', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'New question',
            'answer': 'New answer',
            'category': 3,
            'difficulty': 2
        }

        self.quiz = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Art',
                'id': 1,
            }
        }

        self.new_category = {
            'type': 'Biosciences',
        }
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

    def test_get_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        if data['total_categories'] == 0:
            self.assertFalse(data['categories'])
            self.assertFalse(data['total_categories'])
        else:
            self.assertTrue(data['categories'])
            self.assertTrue(data['total_categories'])

    def test_get_false_route(self):
        res = self.client().get('/youuu')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        if data['total_questions'] == 0:
            self.assertFalse(data['questions'])
            self.assertFalse(data['total_questions'])
        else:
            self.assertTrue(data['categories'])
            self.assertTrue(data['questions'])
            self.assertTrue(data['total_questions'])

    def test_get_questions_beyond_limit(self):
        res = self.client().get('/api/questions?page=999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

    def test_get_question(self):
        res = self.client().get('/api/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_question_not_found(self):
        res = self.client().get('/api/questions/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    def test_get_category_not_found(self):
        res = self.client().get('/api/categories/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    def test_create_new_category(self):
        res = self.client().post('/api/categories', json=self.new_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_new_category_duplicate(self):
        res = self.client().post('/api/categories', json=self.new_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 409)
        self.assertTrue(data['message'])

    def test_create_new_category_incorrect(self):
        res = self.client().post('/api/categories', json={'question': 'Test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertTrue(data['message'])

    def test_get_category_questions(self):
        res = self.client().get('/api/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 4)
        self.assertEqual(data['total_questions'], 4)

    def test_get_category_questions_not_found(self):
        res = self.client().get('/api/categories/99987699/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    def test_create_new_question(self):
        res = self.client().post('/api/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_new_question_incorrect(self):
        res = self.client().post('/api/questions', json={'question': 'Test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertTrue(data['message'])

    def test_search_for_questions(self):
        res = self.client().post('/api/questions/search', json={'search': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 2)
        self.assertEqual(data['total_questions'], 2)

    def test_search_for_questions_no_results(self):
        res = self.client().post('/api/questions/search', json={'search': 'zombie'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    def test_delete_question(self):
        last = Question.query.order_by(Question.id.desc()).first()
        res = self.client().delete(f'/api/questions/{last.id}')
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == last.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_not_found(self):
        res = self.client().delete(f'/api/questions/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    def test_post_quizzes(self):
        res = self.client().post('/api/play_quizzes', json=self.quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['question'])
        self.assertTrue(data['question']['answer'])
        self.assertTrue(data['question']['difficulty'])
        self.assertTrue(data['question']['category'])

    def test_post_quizzes_incorrect(self):
        res = self.client().post('/api/play_quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertTrue(data['message'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
