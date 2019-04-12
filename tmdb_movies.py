import urllib.request
import urllib.parse
import json
import time
from unidecode import unidecode
import os

MY_DIR = os.path.dirname(os.path.realpath(__file__))

# Your tmdb API key
API_KEY = ''

# Rate limit
# per https://developers.themoviedb.org/3/getting-started/request-rate-limiting
# The rate limit is over a 10s interval, max of 40 requests.
# Every 10 seconds, the requests are cleared.
# So just make sure to pause for at least 1/4s after each iteration if you
# are going to do >10 requests.
RATE_LIMIT_IN_SECONDS = 0.3

# constants representing tmdb url components
TMDB_URL_BASE = ''
TMDB_URL_API_KEY = ''
TMDB_URL_ENG = ''
TMDB_URL_MOVIE = ''
TMDB_URL_PERSON = ''
TMDB_URL_CREDITS = ''
TMDB_URL_FIND = ''
TMDB_URL_EXT = ''

def init_properties_dict(prop_fname):
    """
    read a properties file and put it into a dictionary.
    return the dictionary
    """
    props = dict()
    with open(prop_fname) as inf:
        for line in inf:
            if len(line.strip())==0 or line.strip()[0]=='#':
                continue
            line_data = line.strip().split('=')
            prop_key = line_data[0]
            prop_value = line_data[1]
            if prop_value.lower() in {'true', 'false'}:
                prop_value = True if  prop_value.tolower() == 'true' else False
            if prop_value.isnumeric():
                prop_value = int(prop_value)
            if prop_value.replace('.','').isnumeric():
                prop_value = float(prop_value)


            props[prop_key]=prop_value
    return props


def init_from_properties_file(fname=MY_DIR+'/'+'tmdb.properties'):
    """
    init the constants we need from the properties file
    """
    global API_KEY
    global RATE_LIMIT_IN_SECONDS
    global TMDB_URL_BASE
    global TMDB_URL_API_KEY
    global TMDB_URL_ENG
    global TMDB_URL_MOVIE
    global TMDB_URL_PERSON
    global TMDB_URL_CREDITS
    global TMDB_URL_FIND
    global TMDB_URL_EXT

    props = init_properties_dict(fname)

    API_KEY = props['API_KEY']
    RATE_LIMIT_IN_SECONDS = props['RATE_LIMIT_IN_SECONDS']

    # constants representing tmdb url components
    TMDB_URL_BASE = props['TMDB_URL_BASE']
    TMDB_URL_ENG = props['TMDB_URL_ENG']
    TMDB_URL_MOVIE = props['TMDB_URL_MOVIE']
    TMDB_URL_PERSON = props['TMDB_URL_PERSON']
    TMDB_URL_CREDITS = props['TMDB_URL_CREDITS']
    TMDB_URL_FIND = props['TMDB_URL_FIND']
    TMDB_URL_EXT = props['TMDB_URL_EXT']

    TMDB_URL_API_KEY = f'api_key={API_KEY}'

def build_tmdb_url_movies(tmdb_id):
    """
    Assemble the pieces to construct the tmdb url for movies with tmdb_id as
    parameter.
    given tmdb_id
    returns a string of the tmdb url
    """
    url = f'{TMDB_URL_BASE}/' + \
        f'{TMDB_URL_MOVIE}/' + \
        f'{tmdb_id}?' + \
        f'{TMDB_URL_API_KEY}&{TMDB_URL_ENG}'
    return url

def build_tmdb_url_movie_credits(tmdb_id):
    """
    TODO: build the url to retrieve a movie's movie credits from tmdb
    ref: https://developers.themoviedb.org/3/movies/get-movie-credits
    """
    pass

def build_tmdb_url_actors(tmdb_id):
    """
    TODO: build the url to retrieve actor movie credits from tmdb
    ref: https://developers.themoviedb.org/3/people/get-person-movie-credits
    """
    pass


def get_movie_details_by_tmdb_id(tmdb_id):
    """
    take in the tmdb id and then look up and retrieve
    the movie detail information from tmdb
    """

    # retrieve the data
    url = build_tmdb_url_movies(tmdb_id)
    response_as_json = urllib.request.urlopen(url).read()
    result_object = json.loads(response_as_json)


#   TODO get any desired properties of the movie here
    movie_id = result_object['id']
    title = unidecode(result_object['title'])



#   Then add it to movie_details tuple here :
    movie_details = (movie_id, title)


    return movie_details



#
#  MAIN
#

if __name__ == '__main__':


    init_from_properties_file()
    movie_ids = [ 406997 , 77786, 9944 ]
    for movie_id in movie_ids:
        foo  =get_movie_details_by_tmdb_id(movie_id)

        # Rate limiter
        time.sleep(RATE_LIMIT_IN_SECONDS)
        print(foo)
