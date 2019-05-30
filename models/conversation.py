from mongo import Mongo
import Algorithmia
client = Algorithmia.client('sim4F6YzBeA50zxpy6Ef0vYhcPs1')

# input = "Oi, tudo bem?"
# client = Algorithmia.client('sim4F6YzBeA50zxpy6Ef0vYhcPs1')
# algo = client.algo('SummarAI/Summarizer/0.1.3')
# algo.set_options(timeout=300) # optional
# print(algo.pipe(input).result)

# client = Algorithmia.client('sim4F6YzBeA50zxpy6Ef0vYhcPs1')
# algo = client.algo('translation/GoogleTranslate/0.1.1')
# input = {
#   "files": [
#     [
#       "doc1",
#       algo.pipe({
#   "action": "translate",
#   "text": "Oi, como vai?"
#       }).result["translation"]
#     ],
#     [
#       "doc2",
#       algo.pipe({
#   "action": "translate",
#   "text": "Ola, vocẽ está bem ?"
#       }).result["translation"]
#     ],
#     [
#       "doc3",
#       algo.pipe({
#   "action": "translate",
#   "text": "não quero mais respostas!"
#       }).result["translation"]
#     ]
#   ]
# }
# print(input)
# algo = client.algo('PetiteProgrammer/TextSimilarity/1.0.0')
# algo.set_options(timeout=300) # optional
# print(algo.pipe(input).result)

class Conversations:
    mongo = None

    answer = ""
    reply = ""
    rating = 0
    affiliation = None

    def __init__(self):
        self.mongo = Mongo().init()

    def newAnswer(self, answer):
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
                return bestReply["reply"]
            else:
                return self.registerDbAndReturnNotReply(answer, translation, tags)
        else:
            return self.registerDbAndReturnNotReply(answer, translation, tags)

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
