import pickle
import json
import utils as _utils
from flask import Flask, request, Response, render_template
from functools import lru_cache
import warnings


app = Flask(__name__)


def get_form_input(form_field: str) -> str:
    """
    Extract a specific field from a post request form
    :param form_field:
    :return: the value in the form field
    """
    return request.form[form_field]


class GameSim():
    """
    Game similarity object
    """
    def __init__(self, game_id, top_n=5, lsh_file=_utils.LSH_SAVENAME):
        self.game_id = game_id
        self.top_n = top_n
        self.lsh_file = lsh_file
        self.is_game = True
        self.lsh = self.load_lsh()
        try:

            # if getting OpenSSL errors, this uninstall solution works:
            # https://github.com/pyca/pyopenssl/issues/728
            with warnings.catch_warnings():
                # boardgamegeek has a deprecation warning so we'll suppress
                # that for now
                warnings.simplefilter("ignore", DeprecationWarning)
                self.game_data = _utils.get_game_data(game_id=self.game_id)
                self.game_title = self.game_data.name
        except Exception as e:
            self.is_game = False

    def load_lsh(self):
        """
        Load the LSH forest object built using `lsh_train.py`
        :param fname: filename (with path) to the saved forest object
        :return: lsh forest object
        """
        with open(self.lsh_file, 'rb') as f:
            lsh = pickle.load(f)
        return lsh


    def get_game_hash(self):
        """
        Extract the game tokens and compute its hash
        :return: game hash
        """
        game_fields = _utils.extract_game_fields(self.game_data)
        game_tokens = _utils.process_tokens(game_fields)
        return _utils.compute_sim_hash(game_tokens)


    def clean_game_list(self):
        """
        LSH returns the input game as an item if it's in there, we want to
        remove that
        :param game_list: list of game suggestions
        :return: list of games
        """
        if str(self.game_id) in self.similar_games:
            return [game for game in self.similar_games if str(self.game_id) not
                    in game]
        else:
            return self.similar_games[:-1]

    @lru_cache(maxsize=64)
    def get_similar_games(self):
        """
        Get a list of games that are similar to the input game
        :param game_id: BoardGameGeek game ID
        :return:
        """
        self.game_hash = self.get_game_hash()
        # extract the similar games and remove the input title
        self.similar_games = self.lsh.query(self.game_hash, self.top_n+1)
        # clean up and return results
        return self.clean_game_list()


@app.route('/', methods=['GET'])
def index(name=None):
    """
    Main landing page
    :param name:
    :return:
    """
    return render_template('bgsim_form.html', name=name)


def format_return(input_game, similar_games):
    formatted_out = {'Input Game': input_game}
    for i, g in enumerate(similar_games):
        formatted_out[i + 1] = g
    return formatted_out


@app.route("/bg_similarity", methods=['GET', 'POST'])
def main():
    try:
        game_id = int(get_form_input('bgg_id'))
        top_n = int(get_form_input('top_n'))
        game_finder = GameSim(game_id, top_n)

        if game_finder.is_game:
            input_game = f"{game_finder.game_title} (id:{game_id})"
            similar_games = game_finder.get_similar_games()
            output = format_return(input_game, similar_games)
            return Response(json.dumps(output),
                            headers={
                                "Access-Control-Allow-Origin": "*"
                            },
                            status=200)
        else:
            return Response(
                f"Couldn't execute similarity check on [{game_id}]. Is this a valid game id?",
                200
            )
    except Exception as e:
        return Response(f"Couldn't execute similarity check on [{game_id}] - {e}",
                        200)

if __name__ == '__main__':
    app.run(debug=False)

'''
TODO
- write blog post
- look up adding a domain name to the project or hosting it on personal site?
  - maybe call api gateway from my site?
'''