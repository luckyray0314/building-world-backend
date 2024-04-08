import unittest
from unittest.mock import Mock
from ..apps.app import create_app
from ..db.models import Deals, db


class TestDeals(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.init_app(app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_insert(self):
        deal = Deals(name='Deal 1', counterpartie=1)
        response = self.app.post('/deals', json=deal.__dict__)
        self.assertEqual(response.status_code, 401)

        with self.app.session_transaction() as session:
            session['user_id'] = 1
            session['navbar'] = {'pipeline_id': 1}
        response = self.app.post('/deals', json=deal.__dict__)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Deals.query.count(), 1)

    def test_update(self):
        deal = Deals(name='Deal 1', counterpartie=1)
        db.session.add(deal)
        db.session.commit()

        response = self.app.put(f'/deals/{deal.id}', json={'name': 'Deal 2'})
        self.assertEqual(response.status_code, 401)

        with self.app.session_transaction() as session:
            session['user_id'] = 1
            session['navbar'] = {'pipeline_id': 1}
        response = self.app.put(f'/deals/{deal.id}', json={'name': 'Deal 2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Deals.query.filter_by(name='Deal 2').count(), 1)

    def test_delete(self):
        deal = Deals(name='Deal 1', counterpartie=1)
        db.session.add(deal)
        db.session.commit()

        response = self.app.delete(f'/deals/{deal.id}')
        self.assertEqual(response.status_code, 401)

        with self.app.session_transaction() as session:
            session['user_id'] = 1
            session['navbar'] = {'pipeline_id': 1}
        response = self.app.delete(f'/deals/{deal.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Deals.query.count(), 0)

    def test_set_failed(self):
        deal = Deals(name='Deal 1', counterpartie=1)
        db.session.add(deal)
        db.session.commit()

        response = self.app.post(f'/deals/{deal.id}/set_failed')
        self.assertEqual(response.status_code, 401)

        with self.app.session_transaction() as session:
            session['user_id'] = 1
            session['navbar'] = {'pipeline_id': 1}
        response = self.app.post(f'/deals/{deal.id}/set_failed')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Deals.query.filter_by(status=1).count(), 1)

    def test_set_completed(self):
        deal = Deals(name='Deal 1', counterpartie=1)
        db.session.add(deal)
        db.session.commit()

        response = self.app.post(f'/deals/{deal.id}/set_completed')
        self.assertEqual(response.status_code, 401)

        with self.app.session_transaction() as session:
            session