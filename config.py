import os
import json

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(BASE_FOLDER, "config")


class Config:

    def __init__(self):
        with open(os.path.join(RESOURCE_DIR, "review.json")) as f:
            d = json.loads(f.read())
        self.token = d.get("token")
        self.review_question = d.get("review_question")
        self.button_title = d.get("button_title")
