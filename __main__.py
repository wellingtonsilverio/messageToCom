from chat import InterativeChat

aylin = InterativeChat("Aylin")
trees = []

aylin.hello()

while(True):
    _trees, reply = aylin.waitAnswer(trees)

    for _tree in _trees:
        trees.append(_tree)

    aylin.reply(reply)