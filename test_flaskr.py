# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import json
import os
import unittest
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Actor, Movie

# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency's test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        #self.assistant_token = os.environ['assistant_token']
        
        self.assistant_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBZUmIwcUJsX3hCZVQtZXJ3aEdSUyJ9.eyJpc3MiOiJodHRwczovL3Rlc3Q0NjAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNzMyYTc3MmE2YjJkMDA2YWVjMDgwYiIsImF1ZCI6ImRyaW5rIiwiaWF0IjoxNjE4MjIzNjQyLCJleHAiOjE2MTgyMzA4NDIsImF6cCI6IjFuZlIyODAxVEhMRFZ6MmhDeWlXcDVDc3RIc1hoZXpoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.ob8H_16uGq2ALXK3NzB19044emjx7WSY7RL2QuFcZYU8iIhtQm1dVHeNLK36AFoZRCRsH_oe2QkZWA6M8lI8CLxDbbpAbpXJBqTzoolPhLMafh6TNXwM-13PO4y6Oi9Hi7gKWcNgapD_AMfGZ2gFHi-LZw2zqPLuj1UeeSSDr_lu9TldtDN1CWV5AoCpzC9XjNZCTZ7rkKJHYOPmN3mQEJ1XhniSnaK96hlribRdsqpDEWc85e3cBF_D7v9G1VZHfGHA5TqEEHn34oVmX65psttmw1JOyB3F_x3-Cpe1Kk2T88hDFPU3Gyhf__6oB0WqT8ueu4BneT6P5Ls_88Eslg"
        self.director_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBZUmIwcUJsX3hCZVQtZXJ3aEdSUyJ9.eyJpc3MiOiJodHRwczovL3Rlc3Q0NjAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNzMyZDY2OTEwYjZkMDA3MTk4NjgyZCIsImF1ZCI6ImRyaW5rIiwiaWF0IjoxNjE4MjIzMjk1LCJleHAiOjE2MTgyMzA0OTUsImF6cCI6IjFuZlIyODAxVEhMRFZ6MmhDeWlXcDVDc3RIc1hoZXpoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.mgotSXqYHyJnSzQ2k7WgDhLjWhKh0epPNzVq1ilV-qDMUfmQbxPevOFmIJ0WOlVpMT0xzbcFPAbklMGLK8plX77Qx2C7_0ChH1MPhzdKkbBE9G2ailag7cmO2Ic8KwP3gmsQr24-22MMd9yYSLUe9oQ91rgZVAnPzo27g1WY_C0wDud5ZLO_wCRYKLRGQQwhPcRfX9CKJ0IA3kZal2KvXd1kauvjekVEAM2HaIu0Rg38_dxqeQwHKQnZdduLhUdmG7feyVmM6oI72KsGUwCNMEfklnwAqrKAc9XLn2YnaODS9-ZQnF8N5i2GItWIw4O0XbnqJiDPXNJinm7B3-HZAg"
        self.producer_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBZUmIwcUJsX3hCZVQtZXJ3aEdSUyJ9.eyJpc3MiOiJodHRwczovL3Rlc3Q0NjAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNzMyZGEzODNlYjcwMDA3MTUzMzUxZSIsImF1ZCI6ImRyaW5rIiwiaWF0IjoxNjE4MjIzMTcwLCJleHAiOjE2MTgyMzAzNzAsImF6cCI6IjFuZlIyODAxVEhMRFZ6MmhDeWlXcDVDc3RIc1hoZXpoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.Q7TV-ygj8mPhvVfIH7yHyQM1id9iOZr1OGFg1B9Etr9RGV-f-rMk8ceg6Gbs5jhkpcFDy5ZxzYrlBn25l0bG4BUhm-zxLFrxxiBzXO_huurT4ygCzu6JNzyKOa-NyyapA6b9wQ1-RdtS31GE7KDBO2lbhrS6MTNNXd1LePMAmAsY1c3gbCSVAJdl0G2VrsdXd-U-Yx00_0NfBtip1kqRmJBjfu7vo9CgxUBM3Rpjfwvj3RjBNVcpgmYefb9FGTVgMPcRNWLKd7MxZ82Mknc1gUfuFGgcM2she39I7SfE61QqAeuwYO2aCUmuaEWwZHSrcxAOkO3OV1aIaFc_pp5JoA"
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('DATABASE_URL_TEST')
        if not self.database_path:
            self.database_name = "agency_test"
            self.database_path = f"postgres://postgres:postgres@localhost:5432/{self.database_name}"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    #########################################################
    # test of get actors with token of assistant role
    def test_get_actors_with_token(self):
        # Insert dummy actor into database.
        actor = Actor(name="Eslam zaki", age="25", gender="male")
        actor.insert()

        res = self.client().get('/actors',headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))

    ########################################################
    #test get actors without token 
    def test_get_actors(self):
        # Insert dummy actor into database.
        actor = Actor(name="Eslam zaki", age="25", gender="male")
        actor.insert()

        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

    ############################################################
    #test of get movies with token of assistant role
    def test_get_movies_with_token(self):
        # Insert dummy actor into database.
        movie = Movie(title="Diesl a", release="may 29, 2016")
        movie.insert()

        res = self.client().get('/movies',headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        movies = Movie.query.all()
        self.assertEqual(len(data['movies']), len(movies))
    
    ######################################################
    #test get movies without token
    def test_get_movies(self):
        # Insert dummy actor into database.
        movie = Movie(title="Diesl a2", release="may 29, 2016")
        movie.insert()
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)
  
    #####################################################
    #test add new actor using producer role
    def test_create_new_actor(self):
        new_actor_data = {
            'name': "New Eslam",
            'age': "New  age .",
            'gender': "New actor gender Eslam."
        } 

        res = self.client().post('/actors', data=json.dumps(new_actor_data), headers={'Content-Type': 'application/json',
                    'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], new_actor_data['name'])
        self.assertEqual(data['actor']['age'], new_actor_data['age'])
        self.assertEqual(data['actor']['gender'], new_actor_data['gender'])
    #########################################################
    #test create new actor with out age
    def test_create_actor_missing_age(self):
        new_actor_data = {
            'name': "Testing a new actor with missing data.",
            'gender': "male"
        } 

        res = self.client().post('/actors', data=json.dumps(new_actor_data), headers={'Content-Type': 'application/json',
        'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertFalse(data['success'])
    ############################################################
    #test create movie with producer token
    def test_create_movie(self):
        new_movie_data = {
            'title': "New movie",
            'release': "New movie",
        }

        res = self.client().post('/movies', data=json.dumps(new_movie_data), headers={'Content-Type': 'application/json',
         'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], new_movie_data['title'])
        self.assertEqual(data['movie']['release'], new_movie_data['release'])

    ################################################################
    #create movie with missed data
    def test_create_movie_with_missing_data(self):
        new_movie_data = {
            'title': "Testing a new movie with missing data."
        } 

        res = self.client().post('/movies', data=json.dumps(new_movie_data), headers={'Content-Type': 'application/json','Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertFalse(data['success'])

    ###############################################################
    # test update actor age
    def test_update_actor(self):
        actor = Actor(name="Anne Hathaway", age="50", gender="female")
        actor.insert()

        actor_data_patch = {
            'age': '37'
        } 

        res = self.client().patch(
            f'/actors/%s' % (actor.id),
            data=json.dumps(actor_data_patch),
            headers={'Content-Type': 'application/json','Authorization': "Bearer {}".format(self.producer_token)}
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], actor.name)
        self.assertEqual(data['actor']['age'], actor_data_patch['age'])
        self.assertEqual(data['actor']['gender'], actor.gender)

    ##########################################################################
    #update actor that is not in database table of actors
    def test_update_unfound_actor(self):
        actor_data_patch = {
            'age': '1'
        } 

        res = self.client().patch('/actors/9999', data=json.dumps(actor_data_patch), headers={'Content-Type': 'application/json', 'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

    #######################################################################
    #test delete actor using producer role
    def test_delete_actor(self):
        actor = Actor(name="Eslam Monbo", age="12", gender="female")
        actor.insert()
 
        res = self.client().delete(f'/actors/%s' % actor.id,headers={ 'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], actor.id)

    #######################################################################
    #test delete not found actor
    def test_should_not_delete_existing_actor_if_not_found(self):
        res = self.client().delete('/actors/9999',headers={ 'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])
    #######################################################################
    #test update movie using producer role
    def test_should_update_existing_movie_data(self):
        movie = Movie(title="Invisible Man", release="March 20, 1998")
        movie.insert()

        movie_data_patch = {
            'release': 'March 20, 2020'
        } 

        res = self.client().patch(
            f'/movies/%s' % (movie.id),
            data=json.dumps(movie_data_patch),
            headers={'Content-Type': 'application/json','Authorization': "Bearer {}".format(self.producer_token)}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], movie.title)
        self.assertEqual(data['movie']['release'], movie_data_patch['release'])
    ###################################################################################
    # test update not found movie
    def test_update_movie(self):
        movie_title = {
            'title': 'Foo'
        } 

        res = self.client().patch('/movies/9999', data=json.dumps(movie_title), headers={'Content-Type': 'application/json','Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])
    ###################################################################################
    #test delete movie
    def test_should_delete_existing_movie(self):
        movie = Movie(title="Invisible Man", release="March 20, 2020")
        movie.insert()

        res = self.client().delete(f'/movies/%s' % movie.id,headers={'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_id'], movie.id)

    ###########################################################################
    #test delete not found movie
    def test_update_movie_not_found(self):
        res = self.client().delete('/movies/9999',headers={'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])
    #################################################################################
    #test assistant try to delete actor 
    def test_assistant_delete_actor(self):
        actor = Actor(name="Eslam Monbo", age="12", gender="female")
        actor.insert()
        res = self.client().delete(f'/actors/%s' % actor.id,headers={ 'Authorization': "Bearer {}".format(self.assistant_token)})
        #for bidden action
        self.assertEqual(res.status_code, 403)
    ################################################################################    
    #test director try to delete actor 
    def test_director_delete_actor(self):
        actor = Actor(name="Eslam Monbo2", age="12", gender="female")
        actor.insert()
        res = self.client().delete(f'/actors/%s' % actor.id,headers={ 'Authorization': "Bearer {}".format(self.director_token)})
        #for bidden action
        self.assertEqual(res.status_code, 200)

    ################################################################################
    #test director try to delete movie 
    def test_director_delete_movie(self):
        movie = Movie(title="ESLAM Man", release="March 20, 2020")
        movie.insert()
        res = self.client().delete(f'/movies/%s' % movie.id,headers={'Authorization': "Bearer {}".format(self.director_token)})
        #for bidden action
        self.assertEqual(res.status_code, 403)
    #################################################################################
    #test producer try to delete movie
    def test_producer_delete_movie(self):
        movie = Movie(title="ESLAM Man2", release="March 20, 2020")
        movie.insert()
        res = self.client().delete(f'/movies/%s' % movie.id,headers={'Authorization': "Bearer {}".format(self.producer_token)})
        self.assertEqual(res.status_code, 200)        





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
