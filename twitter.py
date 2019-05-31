from TwitterSearch import TwitterSearchOrder, TwitterSearch

class Twitter:
    keywords = None

    def __init__(self, keywords):
        self.keywords = keywords

    def getByKeywords(self):
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        # tso.set_result_type('popular') # Most popular tweets are shown
        tso.set_keywords(self.keywords) # let's define all words we would like to have a look for
        tso.set_language('pt') # we want to see German tweets only
        tso.set_include_entities(False) # and don't give us all those entity information
        tso.remove_link_filter()

        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key = 'hfPWsuE7sGnNryclpperIlAqI',
            consumer_secret = 'eihapGVIBQamG67virPL2Y3AOhXWwHDNTnjG8RDqS45QZnaMLl',
            access_token = '714219592269303808-kHYN3Kro1ZJ6aYkmhTQeQrcZQM3xwPV',
            access_token_secret = 'yu0WI6BidK29Kcivt5r09Xk541kH6Q4RxRT7HB0DoOTWB'
        )

        # this is where the fun actually starts :)
        return ts.search_tweets_iterable(tso)