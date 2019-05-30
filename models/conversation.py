from mongo import Mongo
import Algorithmia

client = Algorithmia.client('sim4F6YzBeA50zxpy6Ef0vYhcPs1')

class Conversations:
    mongo = None

    answer = ""
    reply = ""
    rating = 0
    affiliation = None

    def __init__(self):
        self.mongo = Mongo().init()

    def newAnswer(self, answer, trees):
        translation = self.translateAnswer(answer)
        tags = self.getTags(translation)

        check = False
        bestReply = { "rating": 0 }

        replies = []

        for __tag in tags:
            _find = self.getFind(__tag)
            _replies = self.mongo["dev"]["conversations"].find(_find)
            for _reply in _replies:
                replies.append(_reply)
        
        if len(replies) > 0:
            for reply in replies:
                if reply["rating"] > 0:
                    check = True
                    if reply["rating"] > bestReply["rating"]:
                        bestReply = reply
                    
            if check:
                return tags, bestReply["reply"]
            else:
                return [], self.registerDbAndReturnNotReply(answer, translation, tags)
        else:
            return [], self.registerDbAndReturnNotReply(answer, translation, tags)

    def translateAnswer(self, answer, textLanguageFrom="pt"):
        algo = client.algo('translation/YandexTranslate/0.1.2')
        return algo.pipe({
            "to":"en",
            "from": textLanguageFrom,
            "text": answer
            }).result[0]

    def getTags(self, translation):
        algo = client.algo('nlp/AutoTag/1.0.1')
        return algo.pipe(translation).result

    def getFind(self, tag):
        find = {}
        find["tags"] = {}
        find["tags"]["$all"] = []
        find["tags"]["$all"].append(tag)

        return find

    def registerDbAndReturnNotReply(self, answer, translation, tags):
        _id = self.mongo["dev"]["conversations"].insert_one({
                "answer": answer,
                "rating": 0,
                "translation": translation,
                "tags": tags
            }).inserted_id
        return "Eu não sei responder essa pergunta"
