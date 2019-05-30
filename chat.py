from models.conversation import Conversations

class InterativeChat:
    conversation = None

    clerk = 'Clerk'

    def __init__(self, clerk):
        self.clerk = clerk
        self.conversation = Conversations()

    def hello(self):
        print("Olá! sou " + self.clerk + ", como posso ajudar?")

    def reply(self, message):
        print(self.clerk+": "+message)

    def waitAnswer(self):
        answer = input("You: ")
        reply = self.conversation.newAnswer(answer)
        return reply