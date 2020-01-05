import rpyc


class FilterService(rpyc.Service):
    def __init__(self):
        super().__init__()
        self.bad_words = ["dick", "pussy", "fuck", "faggot", "cock", "shit", "penis", "vagina", "vag"]

    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass

    def exposed_filter_sentence(self, sentence):
        strings = sentence.split(' ')

        for s in strings:
            if s in self.bad_words:
                sentence = sentence.replace(s, '*' * len(s))

        return sentence


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(FilterService(), hostname="localhost", port=18861)
    t.start()