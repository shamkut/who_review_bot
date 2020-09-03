from googletrans import Translator


class Translate:

    def __init__(self, lang, cfg_dict):
        self.dict = cfg_dict
        self.lang = lang
        self.translator = Translator()

    def get(self, phrase):
        if self.lang == "en":
            return phrase
        else:
            res = self.dict.get(phrase)
            if not res:
                res = self.translator.translate(phrase, src="en", dest=self.lang).text
                self.dict[phrase] = res
            return res
