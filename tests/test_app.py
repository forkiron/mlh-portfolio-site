# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>thomas lenh · portfolio</title>" in html
        # TODO Add more tests relating to the home page
        assert "viggle" in html
        assert "university of waterloo" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # TODO Add more tests relating to the /api/timeline_post GET and POST apis
        # Posting a new timeline
        response = self.client.post("/api/timeline_post", data={
            "name": "Jane Choi", 
            "email": "jane@example.com", 
            "content": "Hello, I was here:)"
        })

        assert response.status_code == 200 
        assert response.is_json
        post_json = response.get_json()
        assert post_json["name"] == "Jane Choi"
        assert post_json["email"] == "jane@example.com"
        assert post_json["content"] == "Hello, I was here:)"

        # confirm it's posted and showing 
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200 
        json = response.get_json()
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "Jane Choi"

        # TODO Add more tests relating to the timeline page
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>timeline · thomas lenh</title>" in html

    def test_malformed_timeline_post(self): 
        #POST request missing name 
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html
        
        # POST request with empty content 
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html 

        # POST request with malformed email 
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400 
        html = response.get_data(as_text=True)
        assert "Invalid email" in html 