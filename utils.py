import boardgamegeek as bgg
from datasketch import MinHash
import warnings
warnings.simplefilter("ignore", category=DeprecationWarning)

GAME_FEATURES = [
    'categories',
    'mechanics',
    'families',
    'max_players',
    'expansion',
    'designers',
    'publishers',
    'expansions',
    'yearpublished',
    'minplaytime',
    'maxplaytime',
    'minage',
    'stats',
    'ranks'
]

SIMILARITY_FIELDS = [
    'categories',
    'mechanics',
    'families',
    'designers',
    'publishers',
    'minage',
    'minplaytime',
    'maxplaytime',
    'max_players'
]

INPUT_FIELDS = ['bgg_id', 'top_n']
HASH_REZ = 128
LSH_SAVENAME = "./game_hash_forest.pkl"

def get_bgg_client():
    """
    This will return a bgg client
    :return: bgg client object
    """
    return bgg.BGGClient(disable_ssl=True)


def get_game_data(game_name=None, game_id=None, method=u'best-rank'):
    """
    Get a boardgame's data from BoardGameGeek given a client
    :param bgg_client: a client connection to BoadGameGeek
    :param game_name: name of the game, exactly as it appears on BGG (hard
    to use)
    :param game_id: ID of the board game
    :param method: method to use when there's a conflict of games via name
    :return: the retrieved game object
    """
    bgg_client = get_bgg_client()
    if game_name and game_id:
        raise Exception('Specify only a name or id')
    elif game_name:
        game = bgg_client.game(name=game_name, choose=method)
        return game
    elif game_id:
        game = bgg_client.game(game_id=game_id, choose=method)
        return game
    else:
        raise Exception('No Game Specified')


def extract_game_fields(game_data, fields=SIMILARITY_FIELDS):
    return {field: getattr(game_data, field) for field in fields}


def process_tokens(game_data):
    output_tokens = []
    for feature in SIMILARITY_FIELDS:
        if isinstance(game_data[feature], list):
            output_tokens.extend(game_data[feature])
        else:
            output_tokens.extend([game_data[feature]])
    return output_tokens


def compute_sim_hash(tokens):
    lshf_hash = MinHash(num_perm=HASH_REZ)
    for word in tokens:
        try:
            lshf_hash.update(str(word).encode('utf-8'))
        except AttributeError as e:
            print(tokens)
            print(str(e))
    return lshf_hash

