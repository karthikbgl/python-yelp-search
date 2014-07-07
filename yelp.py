import json
import oauth2
import requests


class YelpSearch(object):
    """
    API Class to authenticate, and request
    the YELP API.
    """

    def __init__(self, token, token_secret, 
                consumer_key, consumer_secret, 
                *args, **kwargs):

        #API configurations
        self.API_HOST         = 'api.yelp.com'
        #The following are unused for now.
        self.API_SEARCH_PATH      = '/v2/search/'
        #self.BUSINESS_PATH    = '/v2/business/'        

        #Defaults 
        self.DEFAULT_SEARCH_LIMIT  = kwargs.get('search_limit', 5)

        #Required consumer key settings
        self.TOKEN           = token
        self.TOKEN_SECRET    = token_secret
        self.CONSUMER_KEY    = consumer_key
        self.CONSUMER_SECRET = consumer_secret


    def sign_request(self, url_params={}):
        """
        Prepares OAuth authentication and signs the request
        """

        url = 'http://{0}{1}'.format(self.API_HOST, self.API_SEARCH_PATH)
        consumer = oauth2.Consumer(self.CONSUMER_KEY, self.CONSUMER_SECRET)

        params = {
            'oauth_token'        : self.TOKEN,
            'oauth_nonce'        : oauth2.generate_nonce(),
            'oauth_timestamp'    : oauth2.generate_timestamp(),
            'oauth_consumer_key' : self.CONSUMER_KEY
        }

        if url_params:
            params.update(url_params)

        oauth_request = oauth2.Request('GET', url, params)

        token = oauth2.Token(self.TOKEN, self.TOKEN_SECRET)

        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
        signed_url = oauth_request.to_url()

        return signed_url


    def get_response(self, url_params=None):
        """
         sends the request to the API.

        Args:
            host (str): The domain host of the API.
            path (str): The path of the API after the domain.
            url_params (dict): An optional set of query parameters in the request.

        Returns:
            a response object for the request.

        """

        signed_url = self.sign_request(url_params)

        response = requests.get(signed_url)

        if response.status_code != 200:
            print "Error: %s - %s" % (response.status_code, response.content)

        return response


    def find(self, term, location, limit=None):
        """
        Query the Search API by a search term and location.

        Args:
            term (str): The search term passed to the API.
            location (str): The search location passed to the API.

        Returns:
            dict: The JSON response from the request.
        """

        limit = limit or self.DEFAULT_SEARCH_LIMIT

        url_params = {
            'term': term,
            'location': location,
            'limit': limit,
        }

        return self.get_response(url_params)
