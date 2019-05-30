from chat import InterativeChat

aylin = InterativeChat("Aylin")

aylin.hello()

while(True):
    reply = aylin.waitAnswer()

    aylin.reply(reply)