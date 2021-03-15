import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor
from flask_cors import CORS


class Movie_testCase(unittest.TestCase):
    """This class represents the trivia test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "movie"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', '16760', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.exec = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlV3eWF3RFVGd0pOMFNXSVBlX2J2YiJ9.eyJpc3MiOiJodHRwczovL21vdmllLW1hbmFnZXItYXJkZXNoaXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNGRiZDZmYTI2MGY0MDA2YTc4NDZlNyIsImF1ZCI6Im1vdmllIiwiaWF0IjoxNjE1NzQ4MjAxLCJleHAiOjE2MTU3NTU0MDEsImF6cCI6IkwwZEIyRTJGRHJtMnR0TUdqZ3FnVEZxNTY2NEhkcXI0Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.hY5vSszAoqMn9JtuTowtxfybkOyYEFwFFRb2LBqv3st-xZdVpO06Cf1y8OrEBAniGLYKDAC1UWeBdn70vBs-7GPm_z9EwWU0SybqYU9Jj5sitRn-ebpxZYyRw6Y-IIIrSWRubMBmXBOuNqQpRbyxonmMudBPXRsYg0bi7MBYoB4ewi2Mhrw_Bhhct73mTe97GCkzhy85Xnqfx_2mppnFJDJbHOWmCBst9dw52g8ECiwQued7eSk53HHdZ3drLOzRnx0A60Q5_aFSoWysxaUMgtjiAHndSH8XcxH2rUGesTNvyeOoXPECtTgeEwIEKPpNrhgD3A7JJDiZ0Tll2Rx2bw'

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # .........................GET:/actors
    def test_get_actors(self):
        res = self.client().get(
            '/actors', headers={'Authorization': 'Bearer ' + self.exec})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actors'])

    def test_authError_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
# ........................GET:/movies............................

    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers={'Authorization': 'Bearer ' + self.exec})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_authError_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

# .....................PATCH:/actors..................

    def test_patch_actors(self):
        res = self.client().patch(
            '/actors/2',
            json={"name": "aj"},
            headers={'Authorization': 'Bearer ' + self.exec})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_authError_patch_actor(self):
        res = self.client().patch('/actors/3', json={"gender": "female"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

# .....................PATCH:/movies..................

    def test_patch_movies(self):
        res = self.client().patch(
            '/movies/1',
            json={
                "movie": "frogz",
                "release_date": 20201010
            },
            headers={'Authorization': 'Bearer ' + self.exec})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_authError_patch_movie(self):
        res = self.client().patch('/movies/3', json={"movie": "homz"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

# ....................Delete:/actors..........................

    def test_delete_actors(self):
        res = self.client().delete(
            '/actors/2', headers={'Authorization': 'Bearer ' + self.exec})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_sent_requesting_delete_actors_without_auth_header(self):
        res = self.client().delete('/actors/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # ...............Delete:/movies.................
    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/2', headers={'Authorization': 'Bearer ' + self.exec})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_AuthError_delete_movie(self):
        res = self.client().delete('/actors/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # ................Post:/actors................
    def test_post_actors(self):
        res = self.client().post(
            '/actors',
            json={
                "name": "allen",
                "age": 40,
                "gender": "male"
            },
            headers={'Authorization': 'Bearer ' + self.exec})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_authError_post_actor(self):
        res = self.client().post('/actors',
                                 json={
                                     "name": "brad",
                                     "age": 60,
                                     "gender": "male"
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


# .....................Post:/movies..........................

    def test_post_movies(self):
        res = self.client().post(
            '/movies',
            json={
                "movie": "once upon a time",
                "release_date": 20100510
            },
            headers={'Authorization': 'Bearer ' + self.exec})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_authError_post_movie(self):
        res = self.client().post('/movies',
                                 json={
                                     "movie": "sepration",
                                     "release_date": 20100404
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

if __name__ == "__main__":
    unittest.main()