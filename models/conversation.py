from mongo import Mongo

class Conversations:
    mongo = None

    answer = ""
    reply = ""
    rating = 0
    affiliation = None

    def __init__(self):
        self.mongo = Mongo().init()

    def newAnswer(self, answer):
        check = False
        bestReply = { "rating": 0 }

        replies = self.mongo["dev"]["conversations"].find({ "answer": answer })
        if replies.count() > 0:
            for reply in replies:
                if reply["rating"] > 0:
                    check = True
                    if reply["rating"] > bestReply["rating"]:
                        bestReply = reply
                    
            if check:
                return bestReply["reply"]
            else:
                return "Eu não sei responder essa pergunta"
        else:
            _id = self.mongo["dev"]["conversations"].insert_one({
                "answer": answer,
                "rating": 0
            }).inserted_id
            return "Eu não sei responder essa pergunta"
