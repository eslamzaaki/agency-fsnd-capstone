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
        
        self.assistant_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBZUmIwcUJsX3hCZVQtZXJ3aEdSUyJ9.eyJpc3MiOiJodHRwczovL3Rlc3Q0NjAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNzMyYTc3MmE2YjJkMDA2YWVjMDgwYiIsImF1ZCI6ImRyaW5rIiwiaWF0IjoxNjE4MjMxMTMyLCJleHAiOjE2MTgyMzgzMzIsImF6cCI6IjFuZlIyODAxVEhMRFZ6MmhDeWlXcDVDc3RIc1hoZXpoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.Akp4VeHv23lTFtWeedNg2kjygE-I8u13W--_u5fMN-jIADibu-h-Pm3lecYW4XDmNzfGkE5dZlSVmcXXbnZaEXtCAPjtJVLJzSXy8q8mxZu4PVk557KiQ5aIkw0RTmmcNmpBfufCYbw9nTGW4Q5HOgFKyPabSPhBZGTL3Jvj8RS-N6JYBa29yebes7fZIECe67FC1w_YDNoFf30qh6h1D3IxbTrObjCjVsDFeo4snJtflcpa-lkJm-V82R0-xf_LBfHSLNMnBdGlfHBGA55EigqoUGI5Um_V_Ai7qeFQdJJ4MUB5P_262T4_sLgPjMKc951YHc6qm4QCg-1zMak9Tw"
        self.director_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBZUmIwcUJsX3hCZVQtZXJ3aEdSUyJ9.eyJpc3MiOiJodHRwczovL3Rlc3Q0NjAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNzMyZDY2OTEwYjZkMDA3MTk4NjgyZCIsImF1ZCI6ImRyaW5rIiwiaWF0IjoxNjE4MjMxMjQ0LCJleHAiOjE2MTgyMzg0NDQsImF6cCI6IjFuZlIyODAxVEhMRFZ6MmhDeWlXcDVDc3RIc1hoZXpoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.dgXu6A23m5lUpyLqzoHSvWeqSC0LGLP_2MHeqydy0k3GtfXYhqPr5OpCxtMQHYOguDHIVaOJD5JeA1Hv2qeL23y03DdVCSB0rwNXawDqHcd0jt2uDuVJxvG5WetBxYXrrX6ZSbqST4HLxfKgAFHiIMBqCUHWzsBsJJX5u82XionydfO0DXg6ij42I1MpWTQrKtz5iiGuRziH2DDPJVXvoc8CvDa6SF4C3pfCBfwXS0XvISXnf2cOjntjApTXUUz-fBMWk09yiGe3BHY4qFlZqQPO7xQG4ma9tOYmlnqph2sQuI6C8NeCjmsjMG0bk9e8BHMuAE7_KewG9IxwKO6lkQ"
        self.producer_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBZUmIwcUJsX3hCZVQtZXJ3aEdSUyJ9.eyJpc3MiOiJodHRwczovL3Rlc3Q0NjAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNzMyZGEzODNlYjcwMDA3MTUzMzUxZSIsImF1ZCI6ImRyaW5rIiwiaWF0IjoxNjE4MjMxMzIyLCJleHAiOjE2MTgyMzg1MjIsImF6cCI6IjFuZlIyODAxVEhMRFZ6MmhDeWlXcDVDc3RIc1hoZXpoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.YSRlNhdn_lo1Pfo999owp2Xw8Hd1KAk1EaU6sSIxUNoedUKxgs-0mtPFv5fRCoFysqg94_Mxnk7pTGRLLOqj0kaRzIq_51nmkWPSG3RRQxXwU1AzTffuqhepUrBljEb7pcY6zw_R0Ol77KX4tKqOz49bSIyFMnIs9ZFZIbuXlBXYpOszvCjFkxc9rvJxh3139YpKInWUoUB8Ra8WuiDh_lPJIcOF4EigLBszIP3V1gwWGE6lyh_EXM_SMG6j8w_UzvtbeVhQCHA2tzOH36TNlIV-dLKVSMOSiN74dVXKSvdgdoz5ZpuTeD66Aa1cWADKtkoQC24WllxB6Rr2Zc4IMA"
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('DATABASE_URL_TEST')
        if not self.database_path:
            self.database_name = "agency_test"
            self.database_path = f"postgresql://postgres:postgres@localhost:5432/{self.database_name}"
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
