import os
import json

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(BASE_FOLDER, "config")


class Config:

    def __init__(self):
        with open(os.path.join(RESOURCE_DIR, "review.json")) as f:
            cfg = json.loads(f.read())
        self.token = cfg.get("token")
        # for translation
        self.lang = cfg.get("language", "en")
        self.dict = self.get_dict(cfg)

    def get_dict(self, cfg):
        d = cfg.get("dict", {})
        res = {}
        for x, y in d.items():
            if y.get(self.lang):
                res[x] = y.get(self.lang)
        return res
